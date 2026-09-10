import requests
import re

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
headers = {'User-Agent': 'Mozilla/5.0'}
response = requests.get(url, headers=headers)
html = response.text

# Find datatables ajax
ajax_matches = re.findall(r'ajax\s*:\s*[\'\"]([^\'\"]+)[\'\"]', html)
print("Ajax Matches:", ajax_matches)

# Print all script sources
scripts = re.findall(r'src=[\'\"]([^\'\"]+)[\'\"]', html)
for s in scripts:
    if 'gmp' in s or 'data' in s:
        print("Script:", s)
