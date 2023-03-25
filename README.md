# Knack Backup Script
This script allows you to back up data from a Knack app by exporting all records from each object and saving them as JSON files. The script can be run on a daily basis to create incremental backups for the last 30 days, as well as monthly backups for long-term storage.

# Prerequisites
Before using the script, you will need to obtain the API keys for your Knack app and save them in a JSON file called Knack API Keys.json in a directory above the script directory. The JSON file should have the following format:

{
  "API_KEYS": {
    "app1": {
      "appName": "Your App Name",
      "appId": "Your App ID",
      "apiKey": "Your API Key"
    },
    "app2": {
      "appName": "Your Second App Name",
      "appId": "Your Second App ID",
      "apiKey": "Your Second API Key"
    }
  }
}

You can obtain the API keys from the Knack builder interface by going to the "Settings" > "API & Code" page and generating a new REST API key. Make sure to copy the Application ID and API key for each app you want to back up and add them to the JSON file.

You will also need to install the following Python libraries:

requests
json

# Usage
To use the script, simply run the knack_backup_script.py file in your Python environment. The script will automatically connect to the Knack API using the API keys you provided and export all records from each object in the app.

The exported data will be saved in two folders: "Monthly Backups" for long-term storage, and "Last 30 Days Backups" for incremental backups. Each backup file will be named after the object it belongs to, with the format "APP_NAME - OBJECT_NAME - OBJECT_KEY - page PAGE_NUMBER.json".

The script will also log any errors or messages to a file called "Log.txt" in a directory above the script directory.

# License
This project is licensed under the MIT License. See the LICENSE file for details.

# Contributing
Contributions to this project are welcome. See the CONTRIBUTING file for more information.

# Authors
Miguel Gutierrez Rodriguez
