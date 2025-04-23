#!/bin/bash

# Function to print messages
print_message() {
    echo -e "\n$1\n"
}

# Check if the script is run as sudo or root
if [ "$EUID" -ne 0 ]; then 
    print_message "Please run as root or with sudo"
    exit 1
fi

# Define the Caldera directory
CALDERA_DIR="/home/caldera/caldera"

# Navigate to the Caldera directory
cd "$CALDERA_DIR" || { print_message "Failed to change directory to $CALDERA_DIR"; exit 1; }

# Stop the Caldera service
print_message "Stopping Caldera service..."
sudo systemctl stop caldera

# Update Caldera
print_message "Updating Caldera..."
git pull origin master

# Install any new dependencies
print_message "Installing dependencies..."
pip install -r requirements.txt --break-system-packages

# Start the Caldera service
print_message "Starting Caldera service..."
sudo systemctl start caldera

print_message "Caldera update complete!"