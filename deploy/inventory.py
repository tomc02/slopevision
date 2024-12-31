#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load environment variables from the specified .env file
env_path = os.path.join("..", ".env")
load_dotenv(dotenv_path=env_path)

# Fetch variables from the .env file
django_server_ip = os.getenv("DJANGO_SERVER_IP")
ansible_user = os.getenv("ANSIBLE_USER")
ssh_private_key_file = os.getenv("SSH_PRIVATE_KEY_FILE")

# Save the dynamic inventory
if django_server_ip and ansible_user and ssh_private_key_file:
    with open("inventory.ini", "w") as f:
        f.write(f"""
[django_server]
{django_server_ip} ansible_user={ansible_user} ansible_ssh_private_key_file={ssh_private_key_file}
""")
else:
    print("Error: Missing required environment variables.")
