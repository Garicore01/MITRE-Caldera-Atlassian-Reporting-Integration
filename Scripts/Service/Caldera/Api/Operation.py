"""
Author: 	Gari Arellano
Date:		11-03-2025
Project: 	Atlassian
Filename:	Operation.py
Description:
  This class is a subclass of CalderaApi class, whereby it is one of the groups of endpoints in 
  the Caldera API, and it is used to interact with the operations endpoint.
"""

import aiohttp
import json
import uuid
from .Models.OperationModel import OperationModel
from .Models.AdversaryModel import AdversaryModel
from .CalderaApi import CalderaApi
from datetime import datetime, timedelta
import logging

logger = logging.getLogger('test_report')

class Operation(CalderaApi):
    def __init__(self, server, api_key):
      logger.info("Initializing Operation class")
      super().__init__(server, api_key)
      self._endpoint = "/operations"
      logger.info(f"Operation endpoint set to: {self._endpoint}")
    
    # PRE: True
    # POST: Returns the endpoint of the operation
    def getEndpoint(self):
      return self._endpoint

    # PRE: <operationId> is a string that represents the id of the operation
    # POST: Returns the report of the operation with id = <operationId>
    async def get_inform(self, operationId):
        logger.info(f"Requesting operation report for ID: {operationId}")
        try:
            result = await self.__get_operation_results("report", operationId)
            logger.info(f"Successfully retrieved report for operation {operationId}")
            return result
        except Exception as e:
            logger.error(f"Error getting operation report for ID {operationId}: {str(e)}")
            raise

    # PRE: <operationId> is a string that represents the id of the operation
    # POST: Returns the event-logs of the operation with id = <operationId>
    async def get_event_logs(self, operationId):
        logger.info(f"Requesting event logs for operation ID: {operationId}")
        try:
            result = await self.__get_operation_results("event-logs", operationId)
            logger.info(f"Successfully retrieved event logs for operation {operationId}")
            return result
        except Exception as e:
            logger.error(f"Error getting event logs for operation ID {operationId}: {str(e)}")
            raise
        
    # PRE: <typeOfResult> is a string that can be "report" or "event-logs"
    #      <operationId> is a string that represents the id of the operation
    # POST: Returns the <typeOfResult> of the operation with id = <operationId>    
    async def __get_operation_results(self, typeOfResult, operationId):
      url = self.getUrl() + self.getEndpoint() + f"/{operationId}/{typeOfResult}"
      logger.debug(f"Making request to URL: {url}")
      async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
              url, 
              headers=self.getHeaders(),
              data=json.dumps({"enable_agent_output": True})
              ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.debug(f"Successfully received response for {typeOfResult} of operation {operationId}")
                return result
        except aiohttp.ClientError as e:
            logger.error(f"Request error for {typeOfResult} of operation {operationId}: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error for {typeOfResult} of operation {operationId}: {str(e)}")
            raise
    
    # PRE: True
    # POST: Returns all operations in the caldera server
    async def __get_new_operations(self):
      url = self.getUrl() + self.getEndpoint()
      logger.debug(f"Requesting all operations from URL: {url}")
      async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
              url, 
              headers=self.getHeaders(),
              data=json.dumps({"enable_agent_output": True})
              ) as response:
                response.raise_for_status()
                result = await response.json()
                logger.info(f"Successfully retrieved {len(result)} operations")
                return result
        except aiohttp.ClientError as e:
            logger.error(f"Request error getting operations: {str(e)}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error getting operations: {str(e)}")
            raise        


    # PRE: True
    # POST: Returns a list of dictionaries with the operation id and name of the operations
    async def get_new_id_operations(self):
      operations_json = await self.__get_new_operations()
      recent_operation_ids = []
      for operation in operations_json:
        operation_info = {"id": operation['id'], "name": operation['name']}
        if operation_info not in recent_operation_ids:
          recent_operation_ids.append(operation_info)
      return recent_operation_ids

    # PRE: <operationId> is a string that represents the id of the operation
    # POST: Deletes the operation with id = <operationId>
    async def delete_operation(self, operationId):
       url = self.getUrl() + self.getEndpoint() + f"/{operationId}"
       logger.debug(f"Deleting operation with ID: {operationId}")
       async with aiohttp.ClientSession() as session:
        try:
            async with session.delete(
              url, 
              headers=self.getHeaders()
            ) as response:
                response.raise_for_status()
                logger.info(f"Successfully deleted operation {operationId}")
                return True
        except aiohttp.ClientError as e:
            logger.error(f"Error deleting operation {operationId}: {str(e)}")
            raise

    # PRE: True
    # POST: Returns a list of dictionaries with the operation id and name of the operations
    #       that have been seen in the last 24 hours
    #       The list is in the format [{operation_id: operation_name}, ...]
    async def get_last_24_hours_new_id_operations(self):
      logger.info("Getting new operation IDs from the last 24 hours")
      try:
          operations_json = await self.__get_new_operations()
          recent_operation_ids = []
          
          current_time = datetime.utcnow()
          time_24_hours_ago = current_time - timedelta(hours=24)
          
          for operation in operations_json:
              start_time = operation.get('start')
              if start_time:
                  try:
                      last_seen = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")
                      
                      if last_seen >= time_24_hours_ago:
                          operation_info = {"id": operation['id'], "name": operation['name']}
                          if operation_info not in recent_operation_ids:
                              recent_operation_ids.append(operation_info)
                          break
                  except (ValueError, TypeError) as e:
                      logger.error(f"Error parsing timestamp for operation {operation.get('id', 'unknown')}: {str(e)}")
                      continue
          
          logger.info(f"Found {len(recent_operation_ids)} recent operations")
          return recent_operation_ids
      except Exception as e:
          logger.error(f"Error getting new operation IDs: {str(e)}")
          raise
      
    