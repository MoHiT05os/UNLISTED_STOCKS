from curl_cffi import requests
from bs4 import BeautifulSoup

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
html = requests.get(url, impersonate='chrome110').text

soup = BeautifulSoup(html, 'html.parser')
scripts = soup.find_all('script')

for i, s in enumerate(scripts):
    if s.string and ('DataTable' in s.string or 'ajax' in s.string or 'data' in s.string):
        print(f"--- Script {i} ---")
        print(s.string[:500])
