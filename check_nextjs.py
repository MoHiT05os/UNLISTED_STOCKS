from curl_cffi import requests
import re
import json

url = 'https://www.investorgain.com/report/ipo-gmp-live/331/'
html = requests.get(url, impersonate='chrome110').text

print("Searching for 'Bajaj' or known IPOs...")
# Find text blocks in NextJS payloads
matches = re.findall(r'Bajaj Housing Finance', html)
print(f"Found 'Bajaj Housing Finance' {len(matches)} times")

# Let's extract a surrounding chunk of one of the matches
if len(matches) > 0:
    idx = html.find('Bajaj Housing Finance')
    print("SURROUNDING TEXT:")
    print(html[idx-200:idx+300])
