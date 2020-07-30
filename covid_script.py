# Importing libraries
import requests
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from time import sleep

# Setting headers to use with requests session
headers = {
        'authority': 'xx9p7hp1p7.execute-api.us-east-1.amazonaws.com',
        'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm',
          }
while True:
    # Gathering data and storing it
    with requests.Session() as session:
        print('Starting download process.')
        session.headers.update(headers)
        resp = session.get('https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral').json()
        url = resp['results'][0]['arquivo']['url']
        r = requests.get(url, allow_redirects=True)
        open('covid_data.xlsx', 'wb').write(r.content)
        print('Download completed.')

    # Using credencials to create a client to interact with the Google Drive API and Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('covid_dashboard_credentials.json', scope)
    client = gspread.authorize(creds)

    # Finding the workbook and opening the first sheet
    sheet = client.open("COVID-19 Dashboard").sheet1

    # Extracting and printing all the sheet values
    sheet_values = sheet.get_all_records()
    print(sheet_values)

    # Creating df with excel file
    print('Creating DataFrame.')
    covid_df = pd.read_excel('covid_data.xlsx')
    # Filtering data from Santa Catarina
    covid_santa_catarina = covid_df.copy().query('estado == "SC"')
    # Dropping unhelpful columns
    covid_santa_catarina.drop(['regiao', 'estado', 'coduf', 'Recuperadosnovos',
                               'codmun', 'codRegiaoSaude', 'interior/metropolitana',
                               'emAcompanhamentoNovos'], axis=1, inplace=True)
    # Renaming columns
    covid_santa_catarina.rename(columns={'nomeRegiaoSaude': 'regiao_do_estado', 'semanaEpi': 'semana_epidemia',
                                         'populacaoTCU2019': 'populacao_tcu_2019', 'casosAcumulado': 'casos_acumulados',
                                         'casosNovos': 'casos_novos', 'obitosAcumulado': 'obitos_acumulados',
                                         'obitosNovos': 'obitos_novos'}, inplace=True)
    # Selecting only the day and month of date
    covid_santa_catarina['data'] = covid_df.data.dt.strftime('%d/%m')
    # Filling null values with empty string to avoid API error
    covid_santa_catarina.fillna('', inplace=True)
    print('DataFrame created. Updating sheet.')

    # Updating sheet
    sheet.update([covid_santa_catarina.columns.values.tolist()] + covid_santa_catarina.values.tolist())
    print('Sheet updated.')
    print(f'Waiting 1 hour to update again. Current date and hour: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
    sleep(3600)
