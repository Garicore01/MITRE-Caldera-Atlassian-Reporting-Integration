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
│   │   │   └── Utils/    # Utility scripts for Caldera
│   │   │       ├── install_caldera_agent_win_v2.ps1  # Windows agent installation and persistence
│   │   │       ├── update-caldera.sh                 # Caldera server update script
│   │   │       └── backup.sh                         # Caldera backup automation
│   │   ├── Report/       # Report generation
│   │   ├── Tickets/      # Jira ticket management
│   │   ├── Statistics/   # Statistical analysis
│   │   └── logs/         # Log files
│   └── main.py          # Main service entry point
```

## Utility Scripts

The project includes several utility scripts in the `src/Service/Caldera/Utils` directory:

### Windows Agent Installation (`install_caldera_agent_win_v2.ps1`)
- PowerShell script for installing and configuring Caldera agent on Windows systems
- Creates a persistent Windows service using NSSM
- Configures automatic startup and recovery options
- Sets up necessary firewall rules
- Requires administrative privileges

### Caldera Server Update (`update-caldera.sh`)
- Bash script for updating Caldera to the latest version
- Stops the Caldera service before update
- Pulls latest changes from master branch
- Installs new dependencies
- Restarts the service
- Requires root privileges
- ⚠️ Note: Operations and Schedules are not preserved during update

### Backup Automation (`backup.sh`)
- Creates compressed backups of the Caldera installation
- Maintains a history of the last 5 backups
- Automatically manages backup rotation
- Logs backup operations
- Requires root privileges
- Backups are stored in `/var/backups/caldera`

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

## Service Configuration

The project includes a systemd service configuration file (`Configuration/caldera.service`) that allows you to run MITRE Caldera as a system service. This configuration:

- Automatically starts Caldera when the system boots
- Restarts the service if it crashes
- Runs under a dedicated `caldera` user
- Ensures the service starts after network connectivity is established

To set up the service:

1. Copy the service file to the systemd directory:
```bash
sudo cp Configuration/caldera.service /etc/systemd/system/
```

2. Reload systemd to recognize the new service:
```bash
sudo systemctl daemon-reload
```

3. Enable and start the service:
```bash
sudo systemctl enable caldera
sudo systemctl start caldera
```

You can check the service status with:
```bash
sudo systemctl status caldera
```

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
