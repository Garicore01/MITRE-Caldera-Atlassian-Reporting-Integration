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
import logging

logger = logging.getLogger('test_report')

class CreatePage:
    def __init__(self, url, email, token):
       logger.info("Initializing CreatePage class")
       self.url = url
       # It has to be the Aiohttp BasicAuth object because aiohttp need this kind of
       # object to make the authentication
       self.auth = aiohttp.BasicAuth(email, token) 
       logger.info("CreatePage initialized successfully")

    # PRE: <space_id> is a string that represents the space id
    #      <title> is a string that represents the title of the page
    #      <parent_id> is a string that represents the parent id of the page
    #      <body> is a string that represents the body of the page. This is the HTML content
    # POST: Returns a JSON object with the response of the created page on Confluence server
    async def create(self, space_id, title, parent_id, body):
      logger.info(f"Creating new page with title: {title}")
      logger.debug(f"Space ID: {space_id}, Parent ID: {parent_id}")
      
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
      try:
          async with aiohttp.ClientSession(
              connector=aiohttp.TCPConnector(ssl=False) # Ignore the SSL certificate
          ) as session:
              # Use aiohttp to make an asynchronous request
              async with session.post(
                 self.url,
                 headers=headers,
                 auth=self.auth,
                 data=payload
              ) as response:
                  if response.status == 200:
                      logger.info(f"Page '{title}' created successfully")
                      return await response.json()
                  else:
                      error_text = await response.text()
                      logger.error(
                          f"Failed to create page '{title}'. "
                          f"Status: {response.status}. "
                          f"Error: {error_text}."
                      )
                      return error_text
      except Exception as e:
          logger.error(f"Error creating page '{title}': {str(e)}")
          raise
          