# Importing libraries
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setting headers to use with requests session
headers = {
        'authority': 'xx9p7hp1p7.execute-api.us-east-1.amazonaws.com',
        'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm',
          }

# Gathering data and storing it
with requests.Session() as session:
    print('Starting download process.')
    session.headers.update(headers)
    resp = session.get('https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral').json()
    url = resp['results'][0]['arquivo']['url']
    r = requests.get(url, allow_redirects=True)
    open('covid_data.xlsx', 'wb').write(r.content)
    print('Download completed.')

# Use credencials to create a client to interact with the Google Drive API and Google Sheets API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('covid_dashboard_credentials.json', scope)
client = gspread.authorize(creds)

# Finding the workbook and opening the first sheet
sheet = client.open("COVID-19 Dashboard").sheet1

# Extracting and printing all the sheet values
sheet_values = sheet.get_all_records()
print(sheet_values)
