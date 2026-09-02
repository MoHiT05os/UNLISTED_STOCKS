import pandas as pd
import json
import re

df = pd.read_excel('Details of stocks.xlsx', sheet_name='All unlisted shares')
df.columns = [c.strip() for c in df.columns]
df = df.dropna(subset=['Symbol', 'Price'])
df = df[df['Symbol'].astype(str).str.strip() != '']

def make_slug(n):
    s = re.sub(r'[^a-z0-9]+', '-', n.lower().strip()).strip('-')
    return s + '-unlisted-shares'

def sf(v, d=0):
    try:
        f = float(v)
        import math
        return d if math.isnan(f) else round(f, 2)
    except:
        return d

stocks = []
for _, r in df.iterrows():
    nm = str(r['Symbol']).strip()
    pr = sf(r.get('Price'), None)
    if pr is None or pr == 0:
        continue
    pv = sf(r.get('Previous Close'), pr)
    ch = sf(r.get('Chg'), round(pr - pv, 2))
    cp = sf(r.get('Chg%'), round((ch / pv * 100) if pv else 0, 2))
    nl = nm.lower()

    if any(k in nl for k in ['bank', 'fin', 'nbfc', 'capital', 'credit', 'invest', 'insurance', 'nse', 'bse', 'msei']):
        sec = 'Financial Services'
    elif any(k in nl for k in ['tech', 'software', 'data', 'digital', 'system', 'info']):
        sec = 'Technology'
    elif any(k in nl for k in ['pharma', 'drug', 'health', 'hospital', 'medic', 'biotech']):
        sec = 'Healthcare'
    elif any(k in nl for k in ['power', 'energy', 'solar', 'wind', 'electric', 'green']):
        sec = 'Energy'
    elif any(k in nl for k in ['food', 'agri', 'dairy', 'sugar', 'tea', 'coffee', 'farm']):
        sec = 'Agriculture'
    elif any(k in nl for k in ['steel', 'metal', 'mining', 'cement', 'infra', 'construction', 'real']):
        sec = 'Infrastructure'
    elif any(k in nl for k in ['auto', 'motor', 'vehicle', 'car']):
        sec = 'Automobile'
    elif any(k in nl for k in ['logistic', 'transport', 'ship', 'port', 'freight']):
        sec = 'Logistics'
    else:
        sec = 'Others'

    risk = 8 if abs(cp or 0) < 1 else 6 if abs(cp or 0) < 2 else 4 if abs(cp or 0) < 4 else 2

    stocks.append({
        'id': make_slug(nm),
        'name': nm,
        'shortName': nm[:22],
        'slug': make_slug(nm),
        'sector': sec,
        'price': pr,
        'prevPrice': pv,
        'change': ch,
        'changePct': cp,
        'financialRiskScore': risk,
        'minInvestment': round(pr * 50),
        'description': nm + ' is an unlisted share available in the pre-IPO market.',
        'tags': ['Unlisted', sec],
    })

stocks_json = json.dumps(stocks, ensure_ascii=False)

# Build sectors
sector_counts = {}
for s in stocks:
    sector_counts[s['sector']] = sector_counts.get(s['sector'], 0) + 1

sectors = [
    {'name': k, 'slug': re.sub(r'[^a-z0-9]+', '-', k.lower()).strip('-'), 'count': v, 'icon': ''}
    for k, v in sorted(sector_counts.items())
]
sectors_json = json.dumps(sectors, ensure_ascii=False)

js = "(function() {\n"
js += "  window.SHARES_DATA = " + stocks_json + ";\n"
js += "  window.SECTORS_DATA = " + sectors_json + ";\n"
js += "})();\n"

with open('js/shares-data.js', 'w', encoding='utf-8') as f:
    f.write(js)

print(f"Done: {len(stocks)} stocks and {len(sectors)} sectors written to js/shares-data.js")
