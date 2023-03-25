#!/usr/bin/python
import json
import csv
import sys
import fileinput
from datetime import datetime
import os
import time
import contextlib
import requests

session = requests.Session()

# Make an API call to the Knack API
def make_api_call(url, headers):
    try:
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise an error if the request fails
        return response.json()
    except requests.exceptions.RequestException as e:
        # Log the error message and the URL that caused the error
        error_message = f"Error during API call: {e}"
        error_url = f"Failed URL: {url}"
        write_to_log(error_message, log_file_path)
        write_to_log(error_url, log_file_path)
        raise e

# Get the path to the folder where the backup files will be saved
def get_folder_path(app_name):
    today = datetime.today()
    backup_type = "Monthly Backups" if today.day == 1 else "Last 30 Days Backups"
    folder_name = today.strftime('%Y-%m-%d') if backup_type == "Last 30 Days Backups" else today.strftime('%d')
    folder_path = os.path.join("..", backup_type, app_name, folder_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return folder_path

# Save the API reply to a file
def save_api_reply_to_file(api_reply, app_name, object_name, object_key, page_number):
    folder_path = get_folder_path(app_name)
    file_name = os.path.join(folder_path, f"{app_name}- {object_name} -{object_key}-page {page_number}.json")
    with open(file_name, "w") as f:
        json.dump(api_reply, f)
    print(f"COMPLETED: {file_name}")

# Get and save records for a specific page
def get_and_save_records_for_page(object_key, page_number, headers, app_name, object_name):
    url = f"https://api.knack.com/v1/objects/{object_key}/records?page={page_number}&rows_per_page=1000&format=raw"
    api_reply = make_api_call(url, headers)
    save_api_reply_to_file(api_reply, app_name, object_name, object_key, page_number)
    page_number += 1
    return page_number, api_reply['total_pages']


def sanitize_object_name(name):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*', '[', ']']
    for char in invalid_chars:
        name = name.replace(char, '-')
    return name

# Get the list of objects from the Knack API
def get_objects(headers):
    url = "https://api.knack.com/v1/objects"
    response = session.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['objects']

# Export data for a specific object
def export_object_data(headers, app_name, object_name, object_key):
    page_number = 1
    total_pages = 1

    # Loop through all pages and export data
    while page_number <= total_pages:
        page_number, total_pages = get_and_save_records_for_page(object_key, page_number, headers, app_name, object_name)

# Export all objects from a Knack app
def export_objects(headers, app_name):
    objects = get_objects(headers)

    # Export data for each object
    for obj in objects:
        object_name = obj['name']
        object_name = sanitize_object_name(object_name)  # Sanitize the object_name
        object_key = obj['key']
        export_object_data(headers, app_name, object_name, object_key)

# Write a message to the log file and print it to the console
def write_to_log(message, log_path):
    with open(log_path, "a") as log_file:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} {message}"
        print(log_entry)
        log_file.write(f"{log_entry}\n")

# Main script

# Set up the script environment
log_file_path = "../Log.txt"

# Record the start of the backup process in the log
write_to_log("*********** Daily Backup Initiated", log_file_path)

# Load API keys from the JSON file
with open('Knack API Keys.json', 'r') as f:
    apps_data = json.load(f)

# Process each app
for app in apps_data['API_KEYS']:
    try:
        app_name = apps_data['API_KEYS'][app]['appName']
        app_id = apps_data['API_KEYS'][app]['appId']
        api_key = apps_data['API_KEYS'][app]['apiKey']

        print(f"Starting export for {app_name} (app ID: {app_id})")

        headers = {
            "Content-Type": "application/json",
            "X-Knack-Application-Id": app_id,
            "X-Knack-REST-API-Key": api_key
        }

        # Export data and create backup files
        export_objects(headers, app_name)

        # Record the completion of the backup for this app in the log
        write_to_log(f"Backup for {app_name} Completed", log_file_path)
    except Exception as e:
        write_to_log(f"Error during backup for {app_name}: {e}", log_file_path)

# Record the completion of the daily backup in the log
write_to_log("*********** Daily Backup Completed", log_file_path)

