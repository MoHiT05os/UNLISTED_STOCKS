import json

with open('js/shares-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract the JSON array
start = content.find('window.SHARES_DATA = ') + len('window.SHARES_DATA = ')
end = content.find(';\n  window.SECTORS_DATA =', start)
if end == -1:
    end = content.find(';\n', start)
shares_json = content[start:end]

shares = json.loads(shares_json)

targets = [
    'NSE India', 'National Stock Exchange', 'Reliance Retail', 'PhonePe', 'Jio Platforms', 
    'OYO', 'Oravel', 'Zepto', 'SBI Funds', 'HDFC Securities', 'Care Health', 'Hero FinCorp',
    'Cochin International', 'Chennai Super', 'Bira', 'Studds', 'Orbis',
    'Lava', 'Indian Gas Exchange', 'Muthoot', 'Arohan', 'InCred', 'Sembcorp',
    'AGS Health', 'Vikram Solar', 'Sambhv', 'Fincare'
]

matched_ids = set()

for t in targets:
    matches = [s for s in shares if t.lower() in str(s.get('name', '')).lower() or t.lower() in str(s.get('shortName', '')).lower()]
    if matches:
        for m in matches:
            m['hot'] = True
            matched_ids.add(m['id'])
            print(f"Matched: {t} -> {m['name']}")
    else:
        print(f"NOT FOUND: {t}")
        
# Set the SEBI tag specifically for NSE
for s in shares:
    name_lower = str(s.get('name', '')).lower()
    if 'nse' in name_lower or 'national stock exchange' in name_lower:
        if 'tags' not in s:
            s['tags'] = []
        if 'SEBI Nod (Soon to List)' not in s['tags']:
            s['tags'].insert(0, 'SEBI Nod (Soon to List)')

# Rewrite the file
new_shares_json = json.dumps(shares, separators=(',', ':'))
new_content = content[:start] + new_shares_json + content[end:]

with open('js/shares-data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print(f"Successfully marked {len(matched_ids)} stocks as 'hot'.")
