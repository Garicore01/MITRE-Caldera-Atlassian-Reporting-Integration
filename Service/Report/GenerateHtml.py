"""
Author: 	Gari Arellano
Date:		15-04-2025
Project: 	Atlassian
Filename:	CreateHtml.py
Description:
    This file contains the GenerateHtml class which is used to generate an HTML report from the
    Caldera JSON report data.
"""
from jinja2 import Template
from ..Statistics import Statistics

class GenerateHtml:
    
    def __init__(self, report_data):
        self.report_data = report_data

    # PRE: <report_data> is a dictionary that contains the JSON report data.
    # POST: Returns an HTML string that represents the report.
    # OBS: The HTML has inline CSS because it is going to be used in Confluence. 
    #      With style tags Confluence doesn't render the CSS.
    def create_html(self):
        statistics = Statistics(self.report_data)
        stats = statistics.calculate_statistics()
        pie_chart = statistics.generate_pie_chart(stats['success_rate'])
        host_chart = statistics.generate_host_chart(stats['host_stats'])
        
        template = Template("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>MITRE Caldera Operation Report</title>
        </head>
        <body style="font-family: Arial, sans-serif; margin: 20px;">
            <h1 style="color: #333;">MITRE Caldera Operation Report</h1>
            <h2 style="color: #333;">Operation: {{ report.name }}</h2>
            <h2 style="color: #333;">Client: {{ report.group }}</h2>
            
            <div style="display: flex; flex-wrap: wrap; gap: 20px; margin-bottom: 30px;">
                <div style="flex: 1; min-width: 300px; padding: 20px; border-radius: 8px; 
                            background-color: #f8f9fa; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #333;">Overall Operation Statistics</h3>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{{ pie_chart }}" alt="Success Rate Pie 
                            Chart" style="max-width: 100%; height: auto;">
                    </div>
                </div>
                
                <div style="flex: 2; min-width: 300px; padding: 20px; border-radius: 8px; 
                            background-color: #f8f9fa; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h3 style="color: #333;">Per-Host Success Rates</h3>
                    <div style="text-align: center; margin: 20px 0;">
                        <img src="data:image/png;base64,{{ host_chart }}" alt="Host Success Rates" \
                            style="max-width: 100%; height: auto;">
                    </div>
                </div>
            </div>
            
            <h2 style="color: #333;">Hosts Involved</h2>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                            background-color: #f4f4f4;">Paw</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                            background-color: #f4f4f4;">Host</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                            background-color: #f4f4f4;">Platform</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                            background-color: #f4f4f4;">Privilege</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left;  
                            background-color: #f4f4f4;">IP Address</th>
                </tr>
                {% for host in report.hosts %}
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ host.paw }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ host.host }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ host.platform }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ host.privilege }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ host.ip }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <h2 style="color: #333;">Executed Steps</h2>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px;">
                <tr>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Host</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Step Name</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Technique ID</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Command</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">PlainText Command</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Platform</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Description</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Output</th>
                    <th style="border: 1px solid #ddd; padding: 8px; text-align: left; 
                    background-color: #f4f4f4;">Status</th>
                </tr>
                {% for step in report.steps %}
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.host }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.name }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.technique_id }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.command }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.plaintext_command }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.platform }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.description }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.output }}</td>
                    <td style="border: 1px solid #ddd; padding: 8px; text-align: left;">
                    {{ step.status }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <h2 style="color: #333;">Operation Outcome</h2>
            <p>The operation executed multiple techniques successfully on the involved hosts.</p>
        </body>
        </html>
        """)
        return template.render(report=self.report_data, stats=stats, pie_chart=pie_chart, \
                            host_chart=host_chart)