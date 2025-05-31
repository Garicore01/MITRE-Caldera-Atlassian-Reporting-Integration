"""
Author: 	Gari Arellano
Date:		21-03-2025
Project: 	TFG
Filename:	JiraReport.py
Description:
  This file contains the JiraReport class which is used to create a ticket in Jira.
"""
from requests.auth import HTTPBasicAuth
import json
import aiohttp
import os
import logging

logger = logging.getLogger('test_report')

class JiraReport:
    def __init__(self):
       logger.info("Initializing JiraReport class")
       self.__url = os.getenv("jira_url")
       self.__email = os.getenv("atlassian_email")
       self.__token = os.getenv("atlassian_token")
       self.__project_id = os.getenv("jira_project_id")
       self.__issue_type = os.getenv("jira_issue_type")
       # It has to be the Aiohttp BasicAuth object because aiohttp need this kind of
       # object to make the authentication
       self.auth = aiohttp.BasicAuth(self.__email, self.__token)
       logger.info("JiraReport initialized successfully")

    # PRE: <title_report> is a string that represents the title of the report
    #      <data> is a JSON object that contains the data of the ticket
    #      <white_list> is a whitelist object.
    # POST: Creates ticket in Jira for each successful step in the data
    async def create_tickets(self, title_report, data, white_list):
        logger.info(f"Starting tickets creation")
        try:
            for step in data["steps"]:
                if (
                    step["status"] == "Success" and 
                    not white_list.is_in_whitelist(step["ability_id"], step["group"])
                ):
                    logger.debug(f"Creating ticket for successful step: {step['name']}")
                    title = f"TFG Gari-Pruebas-Vulnerabilidad {step['name']} encontrada en " \
                            f"{step['group']}"
                    logger.info(f"Starting ticket creation for title: {title}")
                    await self.__create(title, title_report,step)

            logger.info("Ticket creation process completed")
        except Exception as e:
            logger.error(f"Error creating ticket: {str(e)}")
            raise

    # PRE: <title> is a string that represents the title of the page
    #      <title_report> is a string that represents the title of the report
    #      <data> is an object with the data of the step
    # POST: Returns a JSON object with the response of the created page on Confluence server
    async def __create(self, title, title_report, data):
        logger.info(f"Creating Jira ticket with title: {title}")
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        payload = json.dumps({
            "fields": {
                "project": {
                    "id": self.__project_id
                },
                "summary": title,
                "description": {
                    "version": 1,
                    "type": "doc",
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Se ha encontrado una vulnerabilidad con los siguientes detalles:",
                                    "marks": [
                                        {
                                            "type": "strong"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "type": "table",
                            "attrs": {
                                "isNumberColumnEnabled": False,
                                "layout": "default"
                            },
                            "content": [
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableHeader",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Campo",
                                                            "marks": [
                                                                {
                                                                    "type": "strong"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableHeader",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Valor",
                                                            "marks": [
                                                                {
                                                                    "type": "strong"
                                                                }
                                                            ]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Report"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": title_report
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Client"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["group"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Host"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["host"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "IP"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["ip"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Step"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["name"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Ability ID"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["ability_id"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Descripción"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["description"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Comando"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["plaintext_command"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    "type": "tableRow",
                                    "content": [
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": "Salida"
                                                        }
                                                    ]
                                                }
                                            ]
                                        },
                                        {
                                            "type": "tableCell",
                                            "attrs": {},
                                            "content": [
                                                {
                                                    "type": "paragraph",
                                                    "content": [
                                                        {
                                                            "type": "text",
                                                            "text": data["output"]
                                                        }
                                                    ]
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "issuetype": {
                    "id": self.__issue_type
                }
            }
        })

        try:
            # With connector=aiohttp.TCPConnector(ssl=False) we are ignoring the SSL certificate
            async with aiohttp.ClientSession(
                connector=aiohttp.TCPConnector(ssl=False) # Ignore the SSL certificate
            ) as session:
                # Use aiohttp to make an asynchronous request
                async with session.post(
                    self.__url,
                    headers=headers,
                    auth=self.auth,
                    data=payload
                ) as response:
                    if response.status in [200, 201]:  # Both 200 and 201 are success status codes
                        try:
                            result = await response.json()
                            logger.info(f"Jira ticket created successfully: {result['key']}")
                            return result
                        except aiohttp.ContentTypeError as e:
                            error_text = await response.text()
                            logger.error(
                                f"Invalid response from Jira server. Response: {error_text}"
                            )
                            raise Exception(
                                "Invalid response from Jira server. " 
                                "Please check your Jira URL and credentials."
                            )
                    else:
                        error_text = await response.text()
                        logger.error(
                            f"Failed to create Jira ticket. Status: {response.status}, Error: {error_text}"
                        )
                        raise Exception(f"Failed to create Jira ticket: {error_text}")
        except Exception as e:
            logger.error(f"Error in Jira ticket creation: {str(e)}")
            raise