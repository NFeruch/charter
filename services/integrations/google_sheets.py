from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials
SCOPES = ['https://www.googleapis.com/auth/drive']
creds = service_account.Credentials.from_service_account_file('client_secrets.json', scopes=SCOPES)

# Build the Drive API service
drive_service = build('drive', 'v3', credentials=creds)
sheets_service = build('sheets', 'v4', credentials=creds)

# Query to get all Google Sheets files
query = "mimeType='application/vnd.google-apps.spreadsheet'"
results = drive_service.files().list(q=query).execute()
items = results.get('files', [])

if not items:
    print('No files found.')
else:
    print('Files:')
    for item in items:
        print(f"{item['name']} ({item['id']})")