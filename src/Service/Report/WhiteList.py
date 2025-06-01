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
import logging

logger = logging.getLogger('test_report')

class WhiteList:
    def __init__(self):
        logger.info("Initializing WhiteList class")
        load_dotenv()
        self.__token = os.getenv("gitlab_token")
        self.__url = os.getenv("gitlab_url")
        self.__zip_filename = "whitelist_repo.zip"
        # repository must exist in the same directory as the script
        self.__output_dir = "repository"
        self.__name_dir = "caldera-whitelist-master"
        logger.info("WhiteList initialized successfully")

    # PRE: True
    # POST: Initializes the report by downloading the whitelists from Confluence.
    #       This method is called before creating the report to ensure that the whitelists are
    #       available for the report generation.
    async def initialize(self):
        logger.info("Initializing report creation")
        try:
            await self.download_whitelists()
            logger.info("Whitelists downloaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing report: {str(e)}")
            return False
    
    
    # PRE: True.
    # POST: Downloads the zip file from the specified URL and saves it to the local directory.
    async def __download_zip(self):
        logger.info("Starting whitelist repository download")
        try:
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
                        logger.info(f"Whitelist repository downloaded successfully to {self.__zip_filename}")
                    else:
                        error_text = await response.text()
                        logger.error(f"Failed to download whitelist repository. Status: {response.status}, Error: {error_text}")
                        raise Exception(f"Failed to download whitelist repository: {error_text}")
        except Exception as e:
            logger.error(f"Error downloading whitelist repository: {str(e)}")
            raise
    # PRE: True.
    # POST: Extracts the zip file to the specified output directory.
    def __extract_zip(self):
        logger.info(f"Extracting whitelist repository to {self.__output_dir}")
        try:
            with zipfile.ZipFile(self.__zip_filename, 'r') as zip_ref:
                zip_ref.extractall(self.__output_dir)
            # Remove the zip file after extraction
            os.remove(self.__zip_filename)
            logger.info("Whitelist repository extracted successfully")
        except Exception as e:
            logger.error(f"Error extracting whitelist repository: {str(e)}")
            raise

    # PRE: True.
    # POST: Downloads the zip file and extracts it to the specified output directory.
    async def download_whitelists(self):
        logger.info("Starting whitelist download process")
        try:
            await self.__download_zip()
            self.__extract_zip()
            logger.info("Whitelist download process completed successfully")
        except Exception as e:
            logger.error(f"Error in whitelist download process: {str(e)}")
            raise

    # PRE: <ability_id> is a string that represents the ability ID.
    #      <group> is a string that represents the group name.
    #      <last_seen> is a string that represents the last seen date.
    # POST: Returns True if the ability_id is in the whitelist of the group, False otherwise.
    def is_in_whitelist(self, ability_id, group):
        logger.debug(f"Checking if ability {ability_id} is in whitelist for group {group}")
        # Check if the group has a whitelist
        # Ensure we're in the original directory
        original_dir = os.getcwd()
        
        # Check if output directory exists, if not create it
        if not os.path.exists(self.__output_dir):
            logger.warning(f"Output directory '{self.__output_dir}' does not exist")
            logger.warning("Please call download_whitelists() first")
            os.chdir(original_dir)  # Return to original directory
            return False
            
        os.chdir(self.__output_dir)
        if os.path.exists(self.__name_dir):
            os.chdir(self.__name_dir)
            # Check if the group has a whitelist
            if os.path.exists(group):
                logger.debug(f"Group '{group}' has a whitelist")
                # Check if the ability_id is in the whitelist
                with open(f"{group}", "r") as f:
                    logger.debug(f"Searching for '{ability_id}' in whitelist of '{group}'")
                    lines = f.readlines()
                    for line in lines:
                        if line.strip() == ability_id:
                            logger.debug(f"Ability {ability_id} found in whitelist for group {group}")
                            # Return to original directory before returning result
                            os.chdir(original_dir)
                            return True
        
        # Return to original directory before returning result
        os.chdir(original_dir)
        logger.debug(f"Ability {ability_id} not found in whitelist for group {group}")
        return False
