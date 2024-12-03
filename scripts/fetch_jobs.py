import sys
import os
import argparse
import json
from slugify import slugify
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

def generate_markdown_file(job, output_dir):
    title = job.get("title", "untitled")
    slug = slugify(title)
    filename = f"{slug}.md"
    filepath = os.path.join(output_dir, filename)

    # Hugo-compliant Markdown content with taxonomies
    markdown_content = f"""---
title: "{title}"
description: "{job.get('description', '')}"
date: "2024-12-03"  # Replace with dynamic date if needed
draft: false
type: "job"  # Set the type to differentiate single page templates
location: "{job.get('location', '')}"
company:
  name: "{job['company'].get('name', '')}"
  url: "{job['company'].get('url', '')}"
  size: "{job['company'].get('size', '')}"
  sector: "{job['company'].get('sector', '')}"
experience:
  min: {job.get('min_years_of_experience', 0)}
  max: {job.get('max_years_of_experience', -1)}
salary:
  min: {job['salary'].get('min', -1)}
  max: {job['salary'].get('max', -1)}
requirements:
{generate_list(job.get('requirements', []))}
good_to_have_requirements:
{generate_list(job.get('good_to_have_requirements', []))}
perks_and_benefits:
{generate_list(job.get('perks_and_benefits', []))}
job_type: "{job.get('job_type', 'full_time')}"
categories: ["Jobs"]  # Taxonomy for categorization
tags:
  - "{job.get('domain', 'software_engineer')}"  # Tags can include the domain or other identifiers
---

{job.get('overview', '')}
"""

    # Write to Markdown file
    os.makedirs(output_dir, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Markdown file created: {filepath}")

def generate_list(items):
    """Generate YAML-compatible list."""
    return "\n".join([f"  - {item}" for item in items])

def parse_and_generate_markdown(column_values, output_dir):
    """Parse column values and generate individual Markdown files."""
    import re
    for idx, value in enumerate(column_values, start=1):
        print(f"Row {idx}: {value}")  # Log each row
        try:
            value = value.strip("```").strip()
            value = value.replace("'", "\"")
            value = re.sub(r',\s*([\]}])', r'\\1', value)
            job = json.loads(value)
            generate_markdown_file(job, output_dir)
        except json.JSONDecodeError as e:
            print(f"Failed to parse JSON on Row {idx}: {value}\nError: {e}")
            continue

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch a single column from Google Sheets and generate Hugo Markdown files.')
    parser.add_argument('--output-dir', default='content/jobs', help='Output directory for Markdown files')
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
    parse_and_generate_markdown(column_values, args.output_dir)
