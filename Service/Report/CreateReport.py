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


class CreateReport:
    def __init__(self, report, event_logs):
        self.report = report
        self.event_logs = event_logs
        self.whitelist = WhiteList()

    # PRE: True
    # POST: Initializes the report by downloading the whitelists from Confluence.
    #       This method is called before creating the report to ensure that the whitelists are
    #       available for the report generation.
    async def initialize(self):
        await self.whitelist.download_whitelists()

    # PRE: True
    # POST: Returns an HTML string that represents the report.
    def create_report(self):
        extracted_data = self.__extract_relevant_data()
        html_report = GenerateHtml(extracted_data)
        return html_report.create_html() 
        

    # PRE: True
    # POST: Returns a new dictionary with the relevant data extracted from the JSON report. 
    def __extract_relevant_data(self):
        hosts = []
        #techniques = {}
        steps = []
        # Dictionary to map PAW to host
        paw_hosts = {}
        
        # Get the first group and last_seen from the first host
        first_host = self.report["host_group"][0]
        group = first_host["group"]
        
        # First we extract the relevant data for the hosts
        for host in self.report["host_group"]:
            executed_links = [link for link in host.get("links", []) if link["status"] == 0]
            if executed_links:
                hosts.append({
                    "paw": host["paw"],
                    "host": host["host"],
                    "platform": host["platform"],
                    "ip": host["host_ip_addrs"][0] if host["host_ip_addrs"] else "Unknown",
                    "privilege": host["privilege"],
                })
                paw_hosts[host["paw"]] = host["host"]
        # Next we extract the relevant data for the executed steps
        for agent, step_list in self.report.get("steps", {}).items():
            for step in step_list.get("steps", []):
                steps.append({
                    # Get the host name with the key <agent>. Remember that the key is the PAW
                    "host": paw_hosts.get(agent, "Unknown"),
                    "name": step["name"],
                    "technique_id": step["attack"]["technique_id"],
                    "command": step["command"],
                    "plaintext_command": step["plaintext_command"],
                    "platform": step["platform"],
                    "description": step["description"],
                    # Extract the output from the event-logs file
                    "output": self.__extract_output(step["pid"]),
                    "status": self.__set_status(step["ability_id"], group, step["status"]),
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
    # POST: Returns a string that represents the status of the step.
    #       If the ability is in the WhiteList of the client, it returns "Ommitted".
    #       Else
    #       If the status is 0, it returns "Success". 
    #       If the status is 1, it returns "Failed".
    def __set_status(self, ability_id, group, status):
        # Check if the ability is in the whitelist
        if self.whitelist.is_in_whitelist(ability_id, group):
            return "Ommitted"
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
    
    