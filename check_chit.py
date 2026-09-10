from curl_cffi import requests
from bs4 import BeautifulSoup

url = 'https://www.chittorgarh.com/report/ipo-grey-market-premium-gmp/82/'
response = requests.get(url, impersonate='chrome110')
soup = BeautifulSoup(response.text, 'html.parser')
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")

if len(tables) > 0:
    rows = tables[0].find_all('tr')
    for r in rows[:3]:
        print([td.text.strip() for td in r.find_all(['th', 'td'])])
