#!/bin/bash

# Retrieve the username of the executing user.
USER=$(whoami)

# Change the permissions of all files in the directory to that of the executing user.
echo "Changing ownership of the project files to the user: $USER"
sudo chown $USER:$USER *

# Function to install necessary apt packages.
install_apt_packages() {
    PACKAGES=("jq")

    echo "Installing required apt packages..."
    sudo apt update -qq

    for PACKAGE in "${PACKAGES[@]}"; do
        if dpkg -l | grep -qw $PACKAGE; then
            echo "$PACKAGE is already installed. Skipping..."
        else
            sudo apt install -y $PACKAGE
        fi
    done
}

# Function to install necessary pip packages.
install_pip_packages() {
    PACKAGES=("google-api-python-client" "google-auth-httplib2" "google-auth-oauthlib" "requests" "python-dotenv")

    echo "Installing required pip packages..."

    for PACKAGE in "${PACKAGES[@]}"; do
        if pip show $PACKAGE &> /dev/null; then
            echo "$PACKAGE is already installed. Skipping..."
        else
            pip install --upgrade $PACKAGE
        fi
    done
}

# Install apt packages.
install_apt_packages

# Install pip packages.
install_pip_packages

# Check for the existence of token.json, and if not present, provide the URL for issuing it.
echo "Checking for token.json..."

if [ ! -f "token.json" ]; then
    echo 'The token.json file does not exist. Google OAuth authentication is required.'
    python3 generate_token.py
    echo 'Please run the setup.sh script again.'
    exit 0
fi

# If token.json exists, run check_token.py
python3 check_token.py

# Register the script in crontab.
echo "Setting up crontab..."

# Directory path of the current script.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$SCRIPT_DIR/update_ip.py"

# Add a new line to crontab.
CRON_JOB="10 * * * * /usr/bin/python3 $SCRIPT_PATH"

# Back up the current crontab and add a new job.
(crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -

echo "Project setup complete. Crontab has been updated to run the script every hour at 10 minutes past the hour."
