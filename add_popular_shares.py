import json

with open('js/shares-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find('window.SHARES_DATA = ') + len('window.SHARES_DATA = ')
end = content.find(';\n  window.SECTORS_DATA =')
if end == -1:
    end = content.find(';\n', start)
shares_json = content[start:end]
shares = json.loads(shares_json)

# User's exact requested popular shares
requested_shares = [
    {"name": "National Stock Exchange of India (NSE)", "shortName": "NSE India", "price": 4500, "sector": "Financial Services"},
    {"name": "Reliance Retail", "shortName": "Reliance Retail", "price": 850, "sector": "Others"},
    {"name": "PhonePe", "shortName": "PhonePe", "price": 600, "sector": "Technology"},
    {"name": "Jio Platforms", "shortName": "Jio Platforms", "price": 950, "sector": "Technology"},
    {"name": "OYO / Oravel Stays", "shortName": "OYO", "price": 50, "sector": "Others"},
    {"name": "Zepto", "shortName": "Zepto", "price": 120, "sector": "Technology"},
    {"name": "SBI Funds Management", "shortName": "SBI Mutual Fund", "price": 1100, "sector": "Financial Services"},
    {"name": "HDFC Securities", "shortName": "HDFC Securities", "price": 1400, "sector": "Financial Services"},
    {"name": "Care Health Insurance", "shortName": "Care Health", "price": 250, "sector": "Financial Services"},
    {"name": "Hero FinCorp", "shortName": "Hero FinCorp", "price": 950, "sector": "Financial Services"},
    {"name": "Cochin International Airport (CIAL)", "shortName": "Cochin Airport", "price": 280, "sector": "Infrastructure"},
    {"name": "Chennai Super Kings (CSK)", "shortName": "CSK", "price": 260, "sector": "Others"},
    {"name": "Bira 91 / B9 Beverages", "shortName": "Bira 91", "price": 750, "sector": "Others"},
    {"name": "Studds Accessories", "shortName": "Studds", "price": 850, "sector": "Automobile"},
    {"name": "Orbis Financial", "shortName": "Orbis", "price": 400, "sector": "Financial Services"},
    {"name": "Lava International", "shortName": "Lava", "price": 100, "sector": "Technology"},
    {"name": "Indian Gas Exchange (IGX)", "shortName": "IGX", "price": 500, "sector": "Energy"},
    {"name": "Muthoot Fincorp", "shortName": "Muthoot Fincorp", "price": 450, "sector": "Financial Services"},
    {"name": "Arohan Financial Services", "shortName": "Arohan", "price": 150, "sector": "Financial Services"},
    {"name": "InCred Holdings", "shortName": "InCred", "price": 400, "sector": "Financial Services"},
    {"name": "Sembcorp Green Infra", "shortName": "Sembcorp", "price": 200, "sector": "Energy"},
    {"name": "AGS Health", "shortName": "AGS Health", "price": 300, "sector": "Healthcare"},
    {"name": "Vikram Solar", "shortName": "Vikram Solar", "price": 350, "sector": "Energy"},
    {"name": "Sambhv Steel", "shortName": "Sambhv Steel", "price": 200, "sector": "Infrastructure"},
    {"name": "Fincare Small Finance Bank", "shortName": "Fincare", "price": 250, "sector": "Financial Services"}
]

import uuid

for req in requested_shares:
    # Try to find a match in existing shares
    match_found = False
    
    # We use a broad search term derived from the requested name
    search_term = req['shortName'].lower()
    if 'nse' in search_term: search_term = 'nse'
    if 'csk' in search_term: search_term = 'chennai super'
    if 'bira' in search_term: search_term = 'bira'
    if 'cochin' in search_term: search_term = 'cochin internat'
    if 'igx' in search_term: search_term = 'indian gas exch'
    if 'sbi mutual fund' in search_term: search_term = 'sbi funds'
    if 'oyo' in search_term: search_term = 'oravel'
    
    for s in shares:
        if search_term in str(s.get('name', '')).lower() or search_term in str(s.get('shortName', '')).lower():
            s['hot'] = True
            
            # Special case for NSE
            if 'nse' in search_term:
                s['tags'] = s.get('tags', [])
                if 'SEBI Nod (Soon to List)' not in s['tags']:
                    s['tags'].insert(0, 'SEBI Nod (Soon to List)')
            
            match_found = True
            break
            
    if not match_found:
        tags = ['Popular']
        if 'nse' in req['shortName'].lower():
            tags.insert(0, 'SEBI Nod (Soon to List)')
            tags.insert(1, 'Pre-IPO')
            
        new_share = {
            "id": str(uuid.uuid4()),
            "name": req['name'],
            "shortName": req['shortName'],
            "slug": req['shortName'].lower().replace(' ', '-').replace('/', '').replace('(', '').replace(')', ''),
            "sector": req['sector'],
            "price": req['price'],
            "prevPrice": req['price'],
            "change": 0,
            "changePct": 0,
            "financialRiskScore": 5,
            "minInvestment": 50000,
            "description": f"{req['name']} unlisted shares.",
            "tags": tags,
            "hot": True
        }
        shares.append(new_share)

# Rewrite the file
new_shares_json = json.dumps(shares, separators=(',', ':'))
new_content = content[:start] + new_shares_json + content[end:]

with open('js/shares-data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)
    
print("Updated js/shares-data.js successfully!")
