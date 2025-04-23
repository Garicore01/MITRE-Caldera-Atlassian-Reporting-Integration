"""
Author: 	Gari Arellano
Date:		  15-04-2025
Project: 	Atlassian
Filename:	Whitelist.py
Description:
    The scripts read the config file and get the whitelist of the Caldera clients
    from Confluence.
"""

import os
from dotenv import load_dotenv
import aiohttp
import zipfile
import ssl

class WhiteList:
    def __init__(self):
        load_dotenv()
        self.__token = os.getenv("gitlab_token")
        self.__url = os.getenv("gitlab_url")
        self.__zip_filename = "whitelist_repo.zip"
        # repository must exist in the same directory as the script
        self.__output_dir = "repository"
        self.__name_dir = "caldera-whitelist-master"

    # PRE: True.
    # POST: Downloads the zip file from the specified URL and saves it to the local directory.
    async def __download_zip(self):
        async with aiohttp.ClientSession() as session:
            # Create an unverified SSL context to ignore certificate verification
            # This is because the server uses a self-signed certificate
            # and we don't want to verify it
            ssl_context = ssl._create_unverified_context()
            async with session.get(self.__url, headers={"Authorization": 
                                                        f"Bearer {self.__token}"},
                                                        ssl=ssl_context) as response:
                if response.status == 200:
                    content = await response.read()
                    with open(self.__zip_filename, "wb") as f:
                        f.write(content)
                    print(f"✅ Archivo '{self.__zip_filename}' descargado correctamente.")
                else:
                    print(f"❌ Error {response.status}: {await response.text()}")
    # PRE: True.
    # POST: Extracts the zip file to the specified output directory.
    def __extract_zip(self):
        with zipfile.ZipFile(self.__zip_filename, 'r') as zip_ref:
            zip_ref.extractall(self.__output_dir)
        # Remove the zip file after extraction
        os.remove(self.__zip_filename)
        print(f"✅ Repositorio extraído en '{self.__output_dir}'")

    # PRE: True.
    # POST: Downloads the zip file and extracts it to the specified output directory.
    async def download_whitelists(self):
        await self.__download_zip()
        self.__extract_zip()

    # PRE: <ability_id> is a string that represents the ability ID.
    #      <group> is a string that represents the group name.
    #      <last_seen> is a string that represents the last seen date.
    # POST: Returns True if the ability_id is in the whitelist of the group, False otherwise.
    def is_in_whitelist(self, ability_id, group):
        # Check if the group has a whitelist
        # Ensure we're in the original directory
        original_dir = os.getcwd()
        
        # Check if output directory exists, if not create it
        if not os.path.exists(self.__output_dir):
            print(f"🔄 Creating directory '{self.__output_dir}'")
            os.makedirs(self.__output_dir)
            
            # If the directory was just created, the repository isn't downloaded yet
            print(f"⚠️ Repository not found. Please call download_whitelists() first.")
            os.chdir(original_dir)  # Return to original directory
            return False
            
        os.chdir(self.__output_dir)
        if os.path.exists(self.__name_dir):
            os.chdir(self.__name_dir)
            # Check if the group has a whitelist
            if os.path.exists(group):
                print(f"✅ El grupo '{group}' tiene una whitelist.")
                # Check if the ability_id is in the whitelist
                with open(f"{group}", "r") as f:
                    print(f"✅ Buscando '{ability_id}' en la whitelist de '{group}'")
                    lines = f.readlines()
                    for line in lines:
                        if line.strip() == ability_id:
                            # Return to original directory before returning result
                            os.chdir(original_dir)
                            return True
        
        # Return to original directory before returning result
        os.chdir(original_dir)
        return False
