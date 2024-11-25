import sys
import os
import argparse
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

def fetch_column_from_sheet(spreadsheet_id, range_name, credentials_dict):
    try:
        # Authenticate using the service account credentials from environment variables
        credentials = service_account.Credentials.from_service_account_info(
            credentials_dict,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )

        # Build the service
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])

        if not values or len(values) < 2:  # Ensure there is at least a header row and one data row
            print('No data found in the specified range.')
            return []

        # Skip the first row (header) and fetch only the data rows
        column_values = [row[0] for row in values[1:] if row]  # Ensure no empty rows are included
        return column_values

    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")
        sys.exit(1)

def parse_and_save_to_json(column_values, filename):
    import re
    todos = []
    for idx, value in enumerate(column_values, start=1):
        print(f"Row {idx}: {value}")  # Log each row
        try:
            value = value.strip("```").strip()
            value = value.replace("'", "\"")
            value = re.sub(r',\s*([\]}])', r'\1', value)
            todo = json.loads(value)
            todos.append(todo)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON on Row {idx}: {value}\nError: {e}")
            continue

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(todos, f, indent=4)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch a single column from Google Sheets and save to a JSON file.')
    parser.add_argument('output_filename', nargs='?', default='data/jobs.json', help='Output JSON file path')
    parser.add_argument('--range-name', default='list_of_jobs!E:E', help='Range in the spreadsheet to fetch (single column)')

    args = parser.parse_args()

    spreadsheet_id = os.getenv('SPREADSHEET_ID')

    if not spreadsheet_id:
        print("Error: SPREADSHEET_ID is not set in the environment variables.")
        sys.exit(1)

    # Read service account keys from environment variables
    private_key = os.getenv('PRIVATE_KEY')
    if private_key:
        private_key = private_key.replace('\\n', '\n')  # Handle escaped newlines

    credentials_dict = {
        "type": "service_account",
        "project_id": os.getenv('PROJECT_ID'),
        "private_key_id": os.getenv('PRIVATE_KEY_ID'),
        "private_key": private_key,
        "client_email": os.getenv('CLIENT_EMAIL'),
        "client_id": os.getenv('CLIENT_ID'),
        "auth_uri": os.getenv('AUTH_URI'),
        "token_uri": os.getenv('TOKEN_URI'),
        "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_CERT_URL'),
        "client_x509_cert_url": os.getenv('CLIENT_CERT_URL'),
    }

    # Check for missing credentials
    missing_credentials = [key for key, value in credentials_dict.items() if not value]
    if missing_credentials:
        print(f"Error: Missing environment variables for {', '.join(missing_credentials)}")
        sys.exit(1)

    column_values = fetch_column_from_sheet(spreadsheet_id, args.range_name, credentials_dict)
    parse_and_save_to_json(column_values, args.output_filename)
