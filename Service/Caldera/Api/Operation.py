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

class Operation(CalderaApi):
    def __init__(self, server, api_key):
      super().__init__(server, api_key)
      self._endpoint = "/operations"
    
    # PRE: True
    # POST: Returns the endpoint of the operation
    def getEndpoint(self):
      return self._endpoint

    # PRE: <operationId> is a string that represents the id of the operation
    # POST: Returns the report of the operation with id = <operationId>
    async def get_report(self, operationId):
        # We need to wait for the method to finish before returning the result 
        # because it is an asynchronous method
        return await self.__get_operation_results("report", operationId)

    # PRE: <operationId> is a string that represents the id of the operation
    # POST: Returns the event-logs of the operation with id = <operationId>
    async def get_event_logs(self, operationId):
        return await self.__get_operation_results("event-logs", operationId)
        
    # PRE: <typeOfResult> is a string that can be "report" or "event-logs"
    #      <operationId> is a string that represents the id of the operation
    # POST: Returns the <typeOfResult> of the operation with id = <operationId>    
    async def __get_operation_results(self, typeOfResult, operationId):
      url = self.getUrl() + self.getEndpoint() + f"/{operationId}/{typeOfResult}"
      async with aiohttp.ClientSession() as session:
        try:
            async with session.post(
              url, 
              headers=self.getHeaders(),
              data=json.dumps({"enable_agent_output": True})
              ) as response:
                print(response)
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            raise
    
    # PRE: True
    # POST: Returns all operations in the caldera server
    async def __get_new_operations(self):
      url = self.getUrl() + self.getEndpoint()
      async with aiohttp.ClientSession() as session:
        try:
            async with session.get(
              url, 
              headers=self.getHeaders(),
              data=json.dumps({"enable_agent_output": True})
              ) as response:
                print(response)
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientError as e:
            print(f"Request error: {e}")
            raise
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            raise        

    # PRE: True
    # POST: Returns a list of dictionaries with the operation id and name of the operations
    #       that have been seen in the last 24 hours
    #       The list is in the format [{operation_id: operation_name}, ...]
    async def get_new_id_operations(self):
      operations_json = await self.__get_new_operations()
      recent_operation_ids = []
      
      # Get current time and calculate 24 hours ago
      current_time = datetime.utcnow()
      time_24_hours_ago = current_time - timedelta(hours=24)
      
      # Process each operation
      for operation in operations_json:
        # Check each agent in the host_group
        for agent in operation.get('host_group', []):
          # Parse the last_seen timestamp
          if 'last_seen' in agent:
            try:
              # Convert ISO format timestamp to datetime object
              last_seen = datetime.strptime(agent['last_seen'], "%Y-%m-%dT%H:%M:%SZ")
              
              # Check if the agent was seen in the last 24 hours
              if last_seen >= time_24_hours_ago:
                # Add the operation ID and name as a dictionary to the list
                operation_info = {"id": operation['id'], "name": operation['name']}
                if operation_info not in recent_operation_ids:
                  recent_operation_ids.append(operation_info)
                break  # No need to check other agents in this operation
            except (ValueError, TypeError) as e:
              print(f"Error parsing timestamp: {e}")
              continue
      
      return recent_operation_ids
      
    