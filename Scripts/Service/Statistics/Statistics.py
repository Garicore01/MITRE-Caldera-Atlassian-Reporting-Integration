"""
Author: 	Gari Arellano
Date:		15-04-2025
Project: 	Atlassian
Filename:	Statistics.py
Description:
    This file contains the Statistics class, which is responsible for calculating and generating
    statistics from the report data. It includes methods to calculate overall success rates and
    generate pie and bar charts for visualizing the success rates of operations.
"""

import matplotlib.pyplot as plt
import base64
from io import BytesIO
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('statistics.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('Statistics')

class Statistics:
    def __init__(self, report_data=None):
        logger.info("Initializing Statistics class")
        self.data = report_data if report_data is not None else ""
        logger.info(f"Report data initialized: {'Data present' if self.data else 'No data'}")
    
    # PRE: <report_data> is a dictionary that contains the JSON report data.
    # POST: Sets the data attribute to the given value.
    def setData(self, report_data):
        logger.info("Setting new report data")
        self.data = report_data
        logger.info("Report data updated successfully")

    # PRE: <report_data> is a dictionary that contains the JSON report data.
    # POST: Returns a dictionary with the calculated statistics.
    #       This includes the total number of steps, successful steps, and success rate for  
    #       each host. 
    #       The steps are filtered to exclude omitted steps.
    def calculate_statistics(self):
        logger.info("Starting statistics calculation")
        total_steps = 0
        successful_steps = 0
        
        if not self.data or "steps" not in self.data:
            logger.warning("No data or steps found in report data")
            return {
                "total_steps": 0,
                "successful_steps": 0,
                "success_rate": 0,
                "host_stats": {}
            }
            
        for step in self.data["steps"]:
            if step["status"] != "Omitted":
                total_steps += 1
            if step["status"] == "Success":
                successful_steps += 1
                
        success_rate = (successful_steps / total_steps * 100) if total_steps > 0 else 0
        logger.info(f"Statistics calculated - Total steps: {total_steps}, Successful steps: {successful_steps}, Success rate: {success_rate:.2f}%")

        # Calculate per-host statistics
        host_stats = {}
        for host in self.data["hosts"]:
            host_name = host["host"]
            host_steps = [step for step in self.data["steps"] if step["host"] == host_name and 
                          step["status"] != "Omitted"]
            total_host_steps = len(host_steps)
            successful_host_steps = sum(1 for step in host_steps if step["status"] == "Success")
            host_success_rate = (successful_host_steps / total_host_steps * 100) \
                if total_host_steps > 0 else 0
            host_stats[host_name] = {
                "total_steps": total_host_steps,
                "successful_steps": successful_host_steps,
                "success_rate": host_success_rate
            }

        return {
            "total_steps": total_steps,
            "successful_steps": successful_steps,
            "success_rate": success_rate,
            "host_stats": host_stats
        }

    # PRE: <success_rate> is a float that represents the overall success rate of the operation.
    # POST: Returns a base64 encoded string of the generated pie chart.
    #       The chart shows the overall success rate of the operation.
    #       The chart is saved as a PNG image in memory and encoded to base64.
    def generate_pie_chart(self, success_rate):
        plt.figure(figsize=(4, 4))
        labels = ['Not Secure', 'Secure']
        sizes = [success_rate, 100-success_rate]
        colors = ['#f44336', '#4CAF50']
        
        plt.pie(sizes, 
                colors=colors,
                startangle=90,
                labels=labels,
                autopct='%1.1f%%',
                textprops={'fontsize': 10})
        plt.axis('equal')
        plt.title('Overall Success Rate', pad=10, fontsize=12)
        
        # Save to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.3)
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    # PRE: <host_stats> is a dictionary that contains the success rates for each host.
    # POST: Returns a base64 encoded string of the generated horizontal bar chart.
    #       The chart shows the success rates for each host.
    #       The chart is saved as a PNG image in memory and encoded to base64.
    def generate_host_chart(self, host_stats):
        plt.figure(figsize=(10, len(host_stats) * 1.5))
        
        hosts = list(host_stats.keys())
        success_rates = [stats['success_rate'] for stats in host_stats.values()]
        failed_rates = [100-rate for rate in success_rates]
        
        # Create stacked bar chart
        bars1 = plt.barh(hosts, success_rates, color='#f44336', label='Not Secure', height=0.6)
        bars2 = plt.barh(hosts, failed_rates, left=success_rates, color='#4CAF50', label='Secure',\
                        height=0.6)
        
        # Add value labels
        for bar in bars1:
            width = bar.get_width()
            if width > 0:
                plt.text(width/2, bar.get_y() + bar.get_height()/2,
                        f'{width:.1f}%',
                        ha='center', va='center', color='white', fontweight='bold', fontsize=14)
        
        plt.xlim(0, 100)
        plt.xlabel('Success Rate (%)', fontsize=16)
        plt.title('Success Rate by Host', pad=20, fontsize=18)
        plt.legend(loc='lower right', bbox_to_anchor=(1, 1), fontsize=14)
        
        # Adjust tick label size
        plt.tick_params(axis='both', which='major', labelsize=14)
        
        plt.tight_layout()
        
        # Save to bytes
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0.5)
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')