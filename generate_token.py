import os.path
import sys
import time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def wait_for_file(filename, timeout=60, interval=1):
    """Wait for a file to be created.
    
    Args:
        filename (str): The name of the file to wait for.
        timeout (int): Maximum time to wait in seconds.
        interval (int): Interval between checks in seconds.
    """
    start_time = time.time()
    while not os.path.exists(filename):
        if time.time() - start_time > timeout:
            raise TimeoutError(f"Timed out waiting for file: {filename}")
        time.sleep(interval)

def generate_token():
    """Generate token.json by completing the OAuth flow."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
        
        # Wait for the token.json file to be created
        wait_for_file("token.json")

if __name__ == "__main__":
    generate_token()
    print("token.json has been issued. Please run the ./setup.sh script again.")
