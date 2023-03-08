import os
import json
import base64
import sys
import logging
import logging.config
from datetime import datetime
from typing import Tuple

import urllib3
import requests
from dotenv import load_dotenv

# Set correct working directory
cwd = os.getcwd()
os.chdir("/app")
new_cwd = os.getcwd()

# Load environment variables
load_dotenv()
# Disable insecure connection warning when connecting to unverifiable server
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# Enable logging
logging.config.fileConfig("logger.conf")
logger = logging.getLogger(__name__)

# This section contains the essential variables for the script. DNAC details are read from the '.env' file present in the folder.
# The 'RETENTION' variable specifies the number of backups to be kept - edit it as needed
DNAC_URL = os.environ.get("DNA_CENTER_BASE_URL")
DNAC_USER = os.environ.get("DNA_CENTER_USERNAME")
DNAC_PASS = os.environ.get("DNA_CENTER_PASSWORD")
WEBEX_ENABLED = os.environ.get("WEBEX_NOTIFICATION_ENABLED")
WEBEX_TOKEN = os.environ.get("WEBEX_TOKEN")
WEBEX_RECIPIENT = os.environ.get("WEBEX_RECIPIENT")
RETENTION_POLICY = os.environ.get("RETENTION_POLICY")

def makeRequestToDNAC(method: str, endpoint: str, headers: dict) -> Tuple[bool, dict]:
    url = "https://" + DNAC_URL + endpoint
    data = {}
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            verify = False
        )
    except Exception as e:
        logger.error("Operation failed!")
        logger.debug("Error encountered:\n%s", e)
        return False, data
    if response.status_code >=200 and response.status_code<=299:
        logger.debug("Request successfull!")
        data = json.loads(response.content)
        return True, data
    else:
        logger.error("Request failed! See message below for more info!\n", response.content)
        return False, data

def getAuthenticationToken(username: str, password: str) -> str:
    token = ""
    endpoint = "/dna/system/api/v1/auth/token"
    auth2encode = username + ":" + password
    auth = base64.b64encode(auth2encode.encode('UTF-8')).decode('ASCII')
    headers = {
            "Accept": "application/json",
            "Authorization": "Basic " + auth,
            "Content-Type": "application/json"
        }
    logger.info("Authenticating to DNAC...")
    outcome, response = makeRequestToDNAC(method="POST", endpoint=endpoint, headers=headers)
    if outcome:
        token = response["Token"]
        return token
    else:
        logger.error("Authentication failed! Script terminating!")
        sys.exit(1)

def getBackupsList(headers: dict) -> list:
    endpoint = "/api/system/v1/maglev/backup"
    logger.info("Attempting to retrieve the list of backups...")
    outcome, response = makeRequestToDNAC(method="GET", endpoint=endpoint, headers=headers)
    if outcome:
        index = 1
        logger.info("Backups list successfully retrieved!")
        logger.info("There are currently %s backups available for this DNAC node:", len(response['response']))
        for item in sorted(response['response'], key=lambda d: d['start_timestamp'], reverse=True):
            backup_start_time = datetime.fromtimestamp(item['start_timestamp']).replace(microsecond=0)
            backup_end_time = datetime.fromtimestamp(item['end_timestamp']).replace(microsecond=0)
            logger.info(f"{index} - Name: {item['description']} -> Size: {item['backup_size'] / 1000000} MB -> Start time: {backup_start_time} -> End time: {backup_end_time}-> Completion status: {item['status']}")
            index+=1
        return sorted(response['response'], key=lambda d: d['start_timestamp'])
    else:
        logger.error("Could not retrieve backups! Script terminating!")
        sys.exit(1)

def deleteOldestBackup(headers: dict, backups_list: list) -> None:
    # Select the oldest backup ID to delete (1st element in the backups list) and use it in the API call to delete it
    id_of_item_to_delete = backups_list[0]["backup_id"]
    endpoint = "/api/system/v1/maglev/backup/" + id_of_item_to_delete
    logger.info("Attempting to delete backup %s...", backups_list[0]['description'])
    outcome, response = makeRequestToDNAC(method="DELETE", endpoint=endpoint, headers=headers)
    if outcome:
        logger.info("Backup %s has been successfully deleted!", backups_list[0]['description'])
    else:
        logger.error("Could not delete backup %s! Script terminating!", backups_list[0]['description'])
        sys.exit(1)

def applyBackupPolicy(headers: dict) -> None:
    # Get list of backups currently present on DNAC
    logger.info("Current backup policy: keep newest %s backup(s).", RETENTION_POLICY)
    backups_list = getBackupsList(headers)
    index = 0 
    while len(backups_list) > int(RETENTION_POLICY):
        index+=1
        deleteOldestBackup(headers, backups_list)
        backups_list = getBackupsList(headers)
    logger.info(f"Policy has been applied! {index} old backup(s) have been purged.")
    if WEBEX_ENABLED:
        sendWebexMessageToPerson(
            message=f"Policy has been applied! {index} old backup(s) have been purged.",
            email=WEBEX_RECIPIENT
        )
    else:
        logger.info("Backup policy enforcement completed!")

def sendWebexMessageToPerson(message: str, email: str) -> None:
    webex_url = "https://webexapis.com/v1/messages"
    payload = {
        "text": message,
        "toPersonEmail": email
    }
    headers = {
        "Authorization": "Bearer " + WEBEX_TOKEN,
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(webex_url, data=json.dumps(payload), headers=headers, verify = False)
    except Exception as e:
        logger.error("Operation failed!")
        logger.debug("Error encountered:\n%s", e)

    if response.status_code >=200 and response.status_code<=299:
        logger.info("Message successfully sent!")
    else:
        logger.error("Could not send the message")
    
# Script body
token = getAuthenticationToken(username=DNAC_USER, password=DNAC_PASS)
headers = {
        "x-auth-token": token,
        "Content-Type": "application/json"
    }
applyBackupPolicy(headers=headers)
