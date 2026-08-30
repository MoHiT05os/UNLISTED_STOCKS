"""
1. Add DRHP Tracker link to all navbars
2. Read Excel 'All unlisted shares' sheet and update shares-data.js with real price data
"""
import re, pandas as pd

# ── Step 1: Add DRHP link to all navs ──────────────────────────────────────
html_files = ['index.html', 'shares.html', 'screener.html', 'contact.html', 'account.html']

for f in html_files:
    try:
        with open(f, 'r', encoding='utf-8') as fh:
            content = fh.read()

        # Add DRHP link after Screener link in nav
        content = content.replace(
            '<a href="screener.html">Screener</a>',
            '<a href="screener.html">Screener</a>\n        <a href="drhp.html">DRHP</a>'
        )
        content = content.replace(
            '<a href="screener.html">Screener</a>\n        <a href="drhp.html">DRHP</a>\n        <a href="drhp.html">DRHP</a>',
            '<a href="screener.html">Screener</a>\n        <a href="drhp.html">DRHP</a>'
        )

        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(content)
        print(f'Added DRHP link to {f}')
    except FileNotFoundError:
        print(f'Skipped {f} (not found)')

# ── Step 2: Read Excel and update price/prevPrice in shares-data.js ─────────
df = pd.read_excel(
    r'C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS\Details of stocks.xlsx',
    sheet_name='All unlisted shares'
)
df.columns = [c.strip() for c in df.columns]
print(f'\nLoaded {len(df)} rows from Excel')
print('Columns:', df.columns.tolist())

# Build lookup: shortname -> (price, prevPrice)
price_map = {}
for _, row in df.iterrows():
    symbol = str(row.get('Symbol', '')).strip()
    price = row.get('Price', None)
    prev_close = row.get('Previous Close', None)
    if symbol and str(symbol) != 'nan' and price and str(price) != 'nan':
        price_map[symbol.lower()[:10]] = (float(price), float(prev_close) if prev_close and str(prev_close) != 'nan' else float(price))

print(f'Price map has {len(price_map)} entries')
if price_map:
    sample = list(price_map.items())[:3]
    print('Sample:', sample)
