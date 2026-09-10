from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
response = requests.get(url, impersonate='chrome110')
html = response.text
print("Title:", re.search(r'<title>(.*?)</title>', html, re.I).group(1) if '<title>' in html else 'No title')
soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table')
print(f"Found {len(tables)} tables")

for t in tables:
    rows = t.find_all('tr')
    if len(rows) > 0:
        print("Rows count:", len(rows))
        print("Row 0:", [td.text.strip() for td in rows[0].find_all(['th', 'td'])][:5])
        if len(rows) > 1:
            print("Row 1:", [td.text.strip() for td in rows[1].find_all(['th', 'td'])][:5])
