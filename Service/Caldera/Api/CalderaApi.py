"""
Author: 	Gari Arellano
Date:		12-03-2025
Project: 	Atlassian
Filename:	CalderaApi.py
Description:
  This file contains the CalderaApi base class which is used as a base class to interact 
  with the MITRE Caldera API.
  MITRE Caldera Api has many groups of endpoints and each group has its own class, this class
  is the base class for all the groups.
"""

from abc import ABC, abstractmethod
class CalderaApi(ABC):
    def __init__(self, server, api_key):
        self.__url = f"http://{server}/api/v2"
        self.__headers = {
            "KEY": api_key
        }

    def setUrl(self, url):
        self.__url = url

    def setHeaders(self, headers):
        self.__headers = headers

    def getUrl(self):
        return self.__url
    
    def getHeaders(self):
        return self.__headers
    
    @abstractmethod
    def make_request(self, enpoint):
        pass