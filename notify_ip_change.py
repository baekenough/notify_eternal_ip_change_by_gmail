import os
import json
import base64
from email.mime.text import MIMEText
import requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# load .env file
load_dotenv()

USER_ID = os.getenv('USER_ID')
SERVER_NAME = os.getenv('SERVER_NAME')

# Gmail API Setup
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.json'

# Load credentials from token.json
def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    return creds

creds = get_credentials()
if not creds or not creds.valid:
    print("Invalid credentials. Please ensure token.json is valid.")
    exit(1)

IP_INFO_FILE = 'ip_info.json'

def read_ip_info():
    if os.path.exists(IP_INFO_FILE):
        with open(IP_INFO_FILE, "r") as file:
            return json.load(file)
    return {"ip": None, "last_update_time": None}

def get_gmail_service():
    return build('gmail', 'v1', credentials=creds)

def create_message(subject, body, to):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email(service, message):
    try:
        message = (service.users().messages().send(userId="me", body=message).execute())
        print(f"Message Id: {message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def notify_change(new_ip_info):
    service = get_gmail_service()
    subject = f"{SERVER_NAME} IP Address Change Notification"
    body = f"{SERVER_NAME} The IP address has changed.\nIP: {new_ip_info['ip']}\nlast update: {new_ip_info['last_update_time']}"
    message = create_message(subject, body, USER_ID)
    send_email(service, message)

def main():
    print("Starting IP change notification script...")
    current_ip_info = read_ip_info()
    print(f"Current IP Info: {current_ip_info}")
    notify_change(current_ip_info)
    print("Notification sent.")

if __name__ == "__main__":
    main()
