#!/bin/bash

###############################################################################################
# This script updates the Caldera service to the latest version.
#
# ¡¡¡IMPORTANT!!!: Remember that Operations and Schedules are not stored. So, when you stop the 
# service, you lose all the operations and schedules.
# This script needs stop the caldera service, so be sure that you have some notes with the 
# schedules and operations.
###############################################################################################

# Function to print messages
print_message() {
    echo -e "\n$1\n"
}

# Check if the script is run as sudo or root
if [ "$EUID" -ne 0 ]; then 
    print_message "Please run as root or with sudo"
    exit 1
fi

CALDERA_DIR="/home/caldera/caldera"

cd "$CALDERA_DIR" || { print_message "Failed to change directory to $CALDERA_DIR"; exit 1; }

# We need to stop the service to avoid conflicts with the update
print_message "Stopping Caldera service..."
sudo systemctl stop caldera

# Pull the latest changes from the master branch
print_message "Updating Caldera..."
git pull origin master

# Install any new dependencies
print_message "Installing dependencies..."
pip install -r requirements.txt --break-system-packages

# Start again the Caldera service
print_message "Starting Caldera service..."
sudo systemctl start caldera

print_message "Caldera update complete!"