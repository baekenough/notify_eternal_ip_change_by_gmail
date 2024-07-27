import os
import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# load .env file
load_dotenv()

# Current script directory path
script_dir = os.path.dirname(os.path.abspath(__file__))
ip_info_file = os.path.join(script_dir, 'ip_info.json')
last_known_ip_file = os.path.join(script_dir, 'last_known_ip.json')

# Get external IP
new_ip = requests.get('https://ifconfig.me').text.strip()

# Read existing IP
if os.path.exists(last_known_ip_file):
    with open(last_known_ip_file, 'r') as file:
        old_ip_info = json.load(file)
        old_ip = old_ip_info.get('ip', '')
else:
    old_ip = ""

# Check if IP has changed
if new_ip != old_ip:
    print(f"IP has changed from {old_ip} to {new_ip}. Sending notification...")

    # Check if token.json exists and call the appropriate script
    token_file = os.path.join(script_dir, 'token.json')
    if os.path.exists(token_file):
        print("token.json exists. Running check_token.py...")
        os.system(f'python3 {os.path.join(script_dir, "check_token.py")}')
    else:
        print("token.json does not exist. Running generate_token.py...")
        os.system(f'python3 {os.path.join(script_dir, "generate_token.py")}')
        # After generating token, run check_token.py
        os.system(f'python3 {os.path.join(script_dir, "check_token.py")}')
    
    # Save new IP information with KST time
    last_update_time_utc = datetime.utcnow()
    last_update_time_kst = last_update_time_utc + timedelta(hours=9)
    last_update_time_str = last_update_time_kst.strftime("%Y-%m-%d %H:%M:%S")
    new_ip_info = {
        'ip': new_ip,
        'last_update_time': last_update_time_str
    }
    
    with open(ip_info_file, 'w') as file:
        json.dump(new_ip_info, file, indent=4)

    with open(last_known_ip_file, 'w') as file:
        json.dump(new_ip_info, file, indent=4)
    
    # Run mail sending code after check_token.py
    os.system(f'python3 {os.path.join(script_dir, "notify_ip_change.py")}')

    print(f"Updated ip_info.json and last_known_ip.json with new IP: {new_ip}")
else:
    print("IP has not changed.")
