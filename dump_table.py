import requests
from bs4 import BeautifulSoup

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
headers = {'User-Agent': 'Mozilla/5.0'}
html = requests.get(url, headers=headers).text

soup = BeautifulSoup(html, 'html.parser')
tables = soup.find_all('table')

for i, table in enumerate(tables):
    print(f"--- Table {i} ---")
    print(table.prettify()[:1000])  # Print first 1000 chars of each table
