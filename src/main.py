from Service.Caldera.Api import Operation
from Service.Report.CreateReport import CreateReport
from Service.Report.CreatePage import CreatePage
from Service.Report.WhiteList import WhiteList
from Service.Tickets.JiraReport import JiraReport
import asyncio
from dotenv import load_dotenv
import datetime
import os
import logging


load_dotenv()
# Configure logging
log_dir = os.getenv("log_dir", "/app/logs")  # Default value
date = datetime.datetime.now()
date = date.strftime("%d-%m-%Y")
log_filename = f"python_service_report_{date}.log"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger('test_report')
logger.setLevel(logging.INFO)

# Avoid adding multiple handlers if this file is executed multiple times
if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(os.path.join(log_dir, log_filename))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# PRE: <inform> is a dictionary that contains the information of the operation
#      <event_logs> is a list of dictionaries that contains the event logs of the operation
#      <report_html> is a Report object
#      <whiteList> is a WhiteList object
# POST: Returns a dictionary with the relevant data of the operation
def extract_data(inform, event_logs, report_html, whiteList):
    report_html.setReport(inform)
    report_html.setEventLogs(event_logs)
    return report_html.extract_relevant_data(whiteList)

# PRE: <title> is the title of the report.
#      <relevant_data> is a dictionary with the relevant data of the operation
#      <whiteList> is a WhiteList object
#      <jira> is a JiraReport object
# POST: Creates a ticket in Jira
async def create_tickets(title, relevant_data, whiteList, jira):
    await jira.create_tickets(title, relevant_data, whiteList)

# PRE: <confluence_space_id> is the id of the confluence space
#      <confluence_father_id> is the id of the confluence page that will be the father of the 
#      new page
#      <title> is the title of the new page
#      <relevant_data> is a dictionary with the relevant data of the operation
#      <report_html> is a Report object
#      <page> is a Page object
# POST: Creates a page in Confluence
async def create_page(confluence_space_id, confluence_father_id, title, relevant_data, 
                      report_html, page):
    html_content = report_html.create_report(relevant_data)
    await page.create(
        confluence_space_id,
        title,
        confluence_father_id,
        html_content
    )

# PRE: None
# POST: Extracts the relevant data from the Caldera operations and checks if it is necessary 
# to create a report in Confluence and tickets in Jira.
async def __main__():    
    logger.info("Starting test report execution")
    caldera_server      = os.getenv("caldera_server")
    api_key             = os.getenv("api_key")
    atlassian_url       = os.getenv("atlassian_url")
    atlassian_token     = os.getenv("atlassian_token")
    atlassian_email     = os.getenv("atlassian_email")
    confluence_space_id  = os.getenv("confluence_space_id")
    confluence_father_id = os.getenv("confluence_father_id")

    try:
        # Create necessary objects and initialize them
        whiteList = WhiteList()
        await whiteList.initialize()

        report_html = CreateReport()

        page = CreatePage(atlassian_url, atlassian_email, atlassian_token)

        op = Operation(caldera_server, api_key)
        ids = await op.get_new_id_operations()

        jira = JiraReport()

        group = ""
        
        # Process each operation
        for id in ids:
            # Get the operation information and event logs
            logger.info(f"Processing operation: {id['name']} (ID: {id['id']})")
            inform = await op.get_inform(id['id'])
            event_logs = await op.get_event_logs(id['id'])

            # Set the report and event logs in the report_html object to extract relevant data
            relevant_data = extract_data(inform, event_logs, report_html, whiteList)

            # Extract group information to use in the report title
            if len(relevant_data["group"]) == 1:
                group = relevant_data["group"][0]
            else:
                group = ", ".join(relevant_data["group"])

            title = f"Caldera Report {group} - {id['name']} - {date}"
            logger.info(f"Operation group: {group}")

            # Create tickets in Jira
            await create_tickets(title, relevant_data, whiteList, jira)
            
            # Create the HTML content and save it in a Confluence page
            await create_page(confluence_space_id, confluence_father_id, title, relevant_data, 
                              report_html, page)
            logger.info(f"Confluence page created for operation {id['name']}")

            # We have to delete the operation, because Caldera doesn't save the operation 
            # in the server. The operation is save in RAM memory and when the server is 
            # restarted, the operation is lost. 
            # That's why we prefer to delete the operation to avoid unnecessary ram memory 
            # usage.
            logger.info(f"Starting to delete operation {id['name']} (ID: {id['id']})")
            await op.delete_operation(id['id'])
            logger.info(
                f"Operation {id['name']} (ID: {id['id']}) deleted successfully in Caldera"
            )

        logger.info("Test report execution completed successfully")
    except Exception as e:
        logger.error(f"Error in test report execution: {str(e)}")
        raise

if __name__ == "__main__":
    asyncio.run(__main__())
    for handler in logging.getLogger().handlers:
        handler.flush()






