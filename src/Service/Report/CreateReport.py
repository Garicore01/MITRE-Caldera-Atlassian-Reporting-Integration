"""
Author: 	Gari Arellano
Date:		14-04-2025
Project: 	Atlassian
Filename:	CreateReport.py
Description:
  This file contains the CreateReport class which is used to create a report from the Caldera
  JSON. 
"""
from .GenerateHtml import GenerateHtml
from .WhiteList import WhiteList
import logging

logger = logging.getLogger('test_report')

class CreateReport:

    # PRE: <report> is an optional dictionary that represents the report.
    #      <event_logs> is an optional list of dictionaries that represents the event logs.
    # POST: Initializes the report and event_logs attributes with the given values (or empty values 
    #       if not provided) and creates a new instance of the WhiteList class.
    def __init__(self, report=None, event_logs=None):
        logger.info("Initializing CreateReport class")
        self.report = report if report is not None else ""
        # The event_logs is necessary to extract the output of the steps
        self.event_logs = event_logs if event_logs is not None else ""
        self.whitelist = WhiteList()
        self.__html = GenerateHtml()
        logger.info("CreateReport initialized successfully")
    

    # PRE: <report> is a dictionary that represents the report.
    # POST: Sets the report attribute to the given value.
    def setReport(self, report):
        logger.info("Setting new report data")
        self.report = report
        logger.info("Report data updated successfully")
    
    # PRE: <event_logs> is a list of dictionaries that represents the event logs.
    # POST: Sets the event_logs attribute to the given value.
    def setEventLogs(self, event_logs):
        logger.info("Setting new event logs")
        self.event_logs = event_logs
        logger.info("Event logs updated successfully")

    # PRE: <white_list> is a WhiteList object to check if the ability is in the whitelist.
    # POST: Returns a new dictionary with the relevant data extracted from the JSON report.
    def extract_relevant_data(self, white_list):
        logger.info("Extracting relevant data from report")
        try:
            result = self.__extract_relevant_data(white_list)
            logger.info("Data extraction completed successfully")
            return result
        except Exception as e:
            logger.error(f"Error extracting relevant data: {str(e)}")
            raise
        
    # PRE: <data> is a dictionary that contains the report data.
    # POST: Returns an HTML string that represents the report.
    def create_report(self, data):
        #html_report = GenerateHtml(data)
        self.__html.setData(data)
        return self.__html.create_html()

    # PRE: <white_list> is a WhiteList object to check if the ability is in the whitelist.
    # POST: Returns a new dictionary with the relevant data extracted from the JSON report. 
    def __extract_relevant_data(self, white_list):
        hosts = []
        #techniques = {}
        steps = []
        # List to store all groups
        group = []
        # Dictionary to map PAW to host
        paw_hosts = {}
        # Dictionary to map PAW to group
        paw_group = {}
        # Dictionary to map PAW to IP
        ip_hosts = {}
        
        # First we extract the relevant data for the hosts
        for host in self.report["host_group"]:
            paw_hosts[host["paw"]] = host["host"]
            paw_group[host["paw"]] = host["group"]
            ip_hosts[host["paw"]] = host["host_ip_addrs"][0] if host["host_ip_addrs"] else "Unknown"
            
            # Add group if not already present
            if host["group"] not in group:
                group.append(host["group"])
                
            # Add host information
            hosts.append({
                "paw": host["paw"],
                "host": host["host"],
                "group": host["group"],
                "platform": host["platform"],
                "ip": host["host_ip_addrs"][0] if host["host_ip_addrs"] else "Unknown",
                "privilege": host["privilege"],
            })
            
        # Next extract steps information
        for agent_paw, step_list in self.report.get("steps", {}).items():
            for step in step_list.get("steps", []):
                steps.append({
                    "host": paw_hosts.get(agent_paw, "Unknown"),
                    "ip": ip_hosts.get(agent_paw, "Unknown"),
                    "group": paw_group.get(agent_paw, "Unknown"),
                    "name": step["name"],
                    "technique_id": step["attack"]["technique_id"],
                    "command": step["command"],
                    "plaintext_command": step["plaintext_command"],
                    "platform": step["platform"],
                    "description": step["description"],
                    # Extract the output from the event-logs file
                    "output": self.__extract_output(step["pid"]),
                    "status": self.__set_status(step["ability_id"], 
                                              paw_group.get(agent_paw, "Unknown"), 
                                              step["status"],
                                              white_list),
                    "ability_id": step["ability_id"],
                })


        return {
            "name": self.report["name"],
            "group": group,
            "hosts": hosts,
            "steps": steps
        }

    # PRE: <group> is a string that represents the group of the host.
    #      <last_seen> is a string that represents the last seen date of the host.
    #      <status> is an integer that represents the status of the step.
    #      <white_list> is a WhiteList object to check if the ability is in the whitelist.
    # POST: Returns a string that represents the status of the step.
    #       If the ability is in the WhiteList of the client, it returns "Ommitted".
    #       Else
    #       If the status is 0, it returns "Success". 
    #       If the status is 1, it returns "Failed".
    def __set_status(self, ability_id, group, status, white_list):
        logger.info("Setting status of the step")
        # Check if the ability is in the whitelist
        if white_list.is_in_whitelist(ability_id, group):
            logger.info(f"Ability {ability_id} is in whitelist for group {group}")
            return "Omitted"
        else:
            # If the status is 0, it means that the step was successful.
            if status == 0:
                return "Success"
            # If the status is 1, it means that the step failed.
            elif status == 1:
                return "Failed"
            else:
                return "Unknown"
        

    # PRE: <pid> is the process ID of the step.
    # POST: Returns the output of the step with the given process ID.
    def __extract_output(self, pid):
        for entry in self.event_logs:
            # Use the PID of the step to find the output in the event logs.
            if entry["pid"] == pid:
                return entry.get("output", {}).get("stdout", "")
        return "No output available"
    
    