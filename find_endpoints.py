from curl_cffi import requests
import re

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
html = requests.get(url, impersonate='chrome110').text

endpoints = re.findall(r'[\'\"]([^\'\"]+\.json)[\'\"]', html)
endpoints += re.findall(r'[\'\"]([^\'\"]+\.php[^\'\"]*)[\'\"]', html)
endpoints += re.findall(r'url\s*:\s*[\'\"]([^\'\"]+)[\'\"]', html)

print("Possible Endpoints:", set(endpoints))
