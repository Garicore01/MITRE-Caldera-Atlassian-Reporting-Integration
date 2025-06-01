# MITRE Caldera Integration Service

This service provides automated integration between MITRE CALDERA (a cyber security platform) and Atlassian products (Confluence and Jira) for automated reporting and ticket creation.

## Overview

The service automatically:
- Monitors CALDERA operations
- Generates detailed HTML reports
- Creates Confluence pages with operation results
- Creates Jira tickets for identified issues
- Maintains logs of all operations

## Features

- **Automated Operation Monitoring**: Continuously monitors CALDERA operations for new activities
- **Report Generation**: Creates detailed HTML reports of CALDERA operations
- **Confluence Integration**: Automatically creates and updates Confluence pages with operation results
- **Jira Integration**: Creates tickets in Jira for identified security issues
- **Logging System**: Comprehensive logging of all operations and activities
- **Whitelist Management**: Configurable whitelist system for filtering results

## Prerequisites

- Python 3.x
- MITRE CALDERA server
- Atlassian Confluence instance
- Atlassian Jira instance
- Required Python packages (see Installation section)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd mitre-caldera
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with the following variables:
```env
caldera_server=your_caldera_server
api_key=your_caldera_server_api_key
atlassian_url=your_atlassian_url
atlassian_token=your_atlassian_token
atlassian_email=your_atlassian_email
confluence_space_id=confluence_space_id_to_import_the_report
confluence_father_id=confluence_father_id_of_the_page_to_import_the_report
gitlab_token=your_gitlab_token
gitlab_url=your_gitlab_token_url
log_dir=directory_to_save_the_logs
jira_url=your_jira_url
jira_issue_type=your_jira_issue_type
jira_token=your_jira_token
jira_project_id=your_jira_project_id
```

## Project Structure

```
mitre-caldera/
├── src/
│   ├── Service/
│   │   ├── Caldera/      # CALDERA API integration
│   │   ├── Report/       # Report generation
│   │   ├── Tickets/      # Jira ticket management
│   │   ├── Statistics/   # Statistical analysis
│   │   └── logs/         # Log files
│   └── main.py          # Main service entry point
```

## Usage

### Running with Python

Run the service:
```bash
python Scripts/main.py
```

The service will:
1. Monitor CALDERA operations
2. Generate reports for new operations
3. Create Confluence pages
4. Create Jira tickets
5. Clean up processed operations

### Running with Docker

1. Build the Docker image:
```bash
docker build -t mitre-caldera-service .
```

2. Run the container:
```bash
docker run -d \
  --name mitre-caldera \
  -v $(pwd)/.env:/app/.env \
  -v $(pwd)/logs:/app/logs \
  mitre-caldera-service
```

Note: Make sure your `.env` file is properly configured before running the container.

## Logging

Logs are stored in the configured `log_dir` with the format:
```
python_service_report_DD-MM-YYYY.log
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

The GNU GPL is a free, copyleft license for software and other kinds of works. The GPL guarantees that users have the freedom to:
- Use the software for any purpose
- Change the software to suit their needs
- Share the software with others
- Share the changes they make

For more information about the GPL v3.0, visit: https://www.gnu.org/licenses/gpl-3.0.html

## Contact

gariiarellano01@gmail.com
