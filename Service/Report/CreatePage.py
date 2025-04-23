"""
Author: 	Gari Arellano
Date:		  21-03-2025
Project: 	Atlassian
Filename:	CreatePage.py
Description:
  This file contains the CreatePage class which is used to create a page in the Confluence 
  space.
"""
from requests.auth import HTTPBasicAuth
import json
import aiohttp

class CreatePage:
    def __init__(self, url, email, token):
       self.url = url
       # It has to be the Aiohttp BasicAuth object because aiohttp need this kind of
       # object to make the authentication
       self.auth = aiohttp.BasicAuth(email, token) 

    # PRE: <space_id> is a string that represents the space id
    #      <title> is a string that represents the title of the page
    #      <parent_id> is a string that represents the parent id of the page
    #      <body> is a string that represents the body of the page. This is the HTML content
    # POST: Returns a JSON object with the response of the created page on Confluence server
    async def create(self, space_id, title, parent_id, body):
      headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
      }
      payload = json.dumps({
        "spaceId": space_id,
        "status": "current",
        "title": title,
        "parentId": parent_id,
        "body": {
           "representation": "storage",
           "value": body
        }
      }) 
      # With connector=aiohttp.TCPConnector(ssl=False) we are ignoring the SSL certificate
      async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Use aiohttp to make an asynchronous request
        async with session.request(
           "POST",
           self.url,
           headers=headers,
           auth=self.auth,
           data=payload
        ) as response:
          if response.status == 200:
            print("Page created successfully")
            return await response.json()
          else:
            print(f"Failed to create page: {response.status}")
            return await response.text()
          
    # PRE: <page_id> is a string that represents the id of the page
    #      <file_path> is a string that represents the path of the file
    # POST: Returns a JSON object with the response of the uploaded file on Confluence server
    #       This method is used to upload the PDF file to the page
    #       that was created before
    async def upload_pdf(self, page_id, file_path):
      url = f"{self.url}/rest/api/content/{page_id}/child/attachment"
      headers = {
        "X-Atlassian-Token": "no-check",
        "Accept": "application/json"
      }
      with open(file_path, 'rb') as file:
        async with aiohttp.ClientSession() as session:
          async with session.post(url, headers=headers, auth=self.auth, data=file) as response:
            if response.status == 200:
              print("PDF uploaded successfully")
              return await response.json()
            else:
              print(f"Failed to upload PDF: {response.status}")
              return await response.text()

    # PRE: <page_id> is a string that represents the id of the page
    #      <title> is a string that represents the title of the page
    #      <file_name> is a string that represents the name of the file
    # POST: Returns a JSON object with the response of the updated page on Confluence server
    #       This method is used to update the page with the PDF view-macro
    #       that was uploaded before        
    async def update_page(self, page_id, title, file_name):
      headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
      }
      payload = json.dumps({
        "id": page_id,
        "status": "current",
        "title": title,
        "version": {
          "number": 2,
          "message": "Update page",
        },
        "body": {
           "representation": "storage",
           "value": f"<ac:structured-macro ac:name=\"view-file\"><ac:parameter ac:name=\"name\"\
                    >{file_name}.pdf</ac:parameter></ac:structured-macro>",
        }
      }) 
       # With connector=aiohttp.TCPConnector(ssl=False) we are ignoring the SSL certificate
      async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        # Use aiohttp to make an asynchronous request
        async with session.request(
           "PUT",
           self.url,
           headers=headers,
           auth=self.auth,
           data=payload
        ) as response:
          if response.status == 200:
            print("Page update successfully")
            return await response.json()
          else:
            print(f"Failed to update page: {response.status}")
            return await response.text()