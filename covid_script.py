# Importing libraries
import requests

# Setting headers to use with requests session
headers = {
        'authority': 'xx9p7hp1p7.execute-api.us-east-1.amazonaws.com',
        'x-parse-application-id': 'unAFkcaNDeXajurGB7LChj8SgQYS2ptm',
          }

# Gathering data and storing it
with requests.Session() as session:
    session.headers.update(headers)
    resp = session.get('https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalGeral').json()
    url = resp['results'][0]['arquivo']['url']
    r = requests.get(url, allow_redirects=True)
    open('covid_data.xlsx', 'wb').write(r.content)
