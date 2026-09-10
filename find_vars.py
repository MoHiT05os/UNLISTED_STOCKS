import requests
import re

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
headers = {'User-Agent': 'Mozilla/5.0'}
html = requests.get(url, headers=headers).text

# Search for JSON or variable assignments
matches = re.findall(r'var\s+\w+\s*=\s*\[{.*?}\];', html, re.DOTALL)
print(f"Found {len(matches)} variable arrays")
for m in matches:
    print(m[:200])
