import os
import pandas as pd
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import numpy as np

# Define the required scopes and paths
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CLIENT_SECRET_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

# Function to fetch Google Sheets data
def get_google_sheets_data(SPREADSHEET_ID, RANGE_NAME):
    creds = None
    # Check if we have a token file
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    
    # If no valid credentials are available, ask the user to log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for future runs
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Fetch the data from the Google Sheet
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    return values

def save_to_excel(data, output_filename):
    df = pd.DataFrame(data[1:], columns=data[0])  
    df.to_excel(output_filename, index=False)
    print(f"Data successfully saved to {output_filename}")

if __name__ == '__main__':
    SPREADSHEET_ID = '1ztM8SVAxHaRXVMabmzebCp3F0oCJWq161D2o-vOq9A4'  
    RANGE_NAME = 'Sheet1!A:E'  

    sheet_data = get_google_sheets_data(SPREADSHEET_ID, RANGE_NAME)

    if sheet_data:
        save_to_excel(sheet_data, 'google_sheet_data.xlsx')
    else:
        print('No data found.')
