from Service.Caldera.Api import Operation
from Service.Report.CreateReport import CreateReport
from Service.Report.CreatePage import CreatePage
#import re
import asyncio
from dotenv import load_dotenv
import datetime
import os

load_dotenv()

async def get_reports(operation):
    #return await operation.get_report("854fccc9-68f7-4c39-ae56-6fa47f58f606")
    return await operation.get_new_id_operations()

async def get_report(operation, id):
    return await operation.get_report(id)

async def get_event_logs(operation, id):
    return await operation.get_event_logs(id)


async def __main__():    
    caldera_server      = os.getenv("caldera_server")
    api_key             = os.getenv("api_key")
    atlassian_url       = os.getenv("atlassian_url")
    atlassian_token     = os.getenv("atlassian_token")
    atlassian_email     = os.getenv("atlassian_email")
    atlassian_space_id  = os.getenv("atlassian_space_id")
    atlassian_father_id = os.getenv("atlassian_father_id")

    op = Operation(caldera_server, api_key)
    ids = await get_reports(op)
    
    for id in ids:
        report = await get_report(op, id['id'])
        event_logs = await get_event_logs(op, id['id'])

        group = report["host_group"][0]["group"]

        report_html = CreateReport(report, event_logs)
        await report_html.initialize()
        html_content = report_html.create_report()
        # Save the HTML content to a file
        with open(f"/app/Scripts/Service/builds/{group}_caldera_report.html", "w", encoding="utf-8") as file:
            file.write(html_content)
        # Create a page in Atlassian
        page = CreatePage(atlassian_url, atlassian_email, atlassian_token)
        date = datetime.datetime.now()
        date = date.strftime("%d-%m-%Y")
        title = f"Caldera Report {group} - {id['name']} - {date}"
        response = await page.create(
            atlassian_space_id,
            title,
            atlassian_father_id,
            html_content
        )
    

if __name__ == "__main__":
    asyncio.run(__main__())






