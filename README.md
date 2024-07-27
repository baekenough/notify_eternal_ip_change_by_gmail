# IP Change Notification Script

This project contains scripts for notifying IP address changes via email using the Gmail API.

## How to Obtain `credentials.json`

1. **Enable the Gmail API:**
   Go to the Google Cloud Console and enable the Gmail API for your project.

2. **Configure OAuth Consent Screen:**
   Configure the OAuth consent screen by setting it to "Test" and adding your email (the email specified in your `.env` file) as a test user.

3. **Create OAuth 2.0 Credentials:**
   Create OAuth 2.0 credentials with the application type set to "Desktop App." Download the resulting JSON file.

4. **Rename and Place `credentials.json`:**
   Rename the downloaded JSON file to `credentials.json` and place it in the project folder.

## How to Use

1. **Run `setup.sh`:**
   Execute the `setup.sh` script. If `token.json` is not available, follow the URL provided during the execution to obtain `token.json`. Do not close the application during this process.

2. **Run `setup.sh` Again:**
   Once `token.json` is obtained, run `setup.sh` again.

3. **Automatic Token Refresh:**
   As long as `token.json` is available, the script will automatically refresh the token when it expires. There is no need to reissue the token.

## .env File Configuration

Make sure to create a `.env` file in the project folder with the following variables:

```env
USER_ID=your_email@example.com
SERVER_NAME=name_of_the_server_to_be_run
