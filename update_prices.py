"""
Match Excel prices into shares-data.js using fuzzy name matching
"""
import re, pandas as pd

df = pd.read_excel(
    r'C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS\Details of stocks.xlsx',
    sheet_name='All unlisted shares'
)
df.columns = [c.strip() for c in df.columns]

# Build price map - key = cleaned lowercase first 12 chars
price_map = {}
for _, row in df.iterrows():
    symbol = str(row.get('Symbol', '')).strip().lower()
    price = row.get('Price', None)
    prev_close = row.get('Previous Close', None)
    if symbol and symbol != 'nan' and price and str(price) != 'nan':
        try:
            price_map[symbol[:12]] = (float(price), float(prev_close) if prev_close and str(prev_close) != 'nan' else float(price))
        except:
            pass

print(f"Price map: {len(price_map)} entries")

# Read shares-data.js
with open('js/shares-data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all stock name+price pairs and try to update
def match_name(name):
    name_clean = name.lower()[:12]
    if name_clean in price_map:
        return price_map[name_clean]
    # Try partial match on first 8 chars
    for k, v in price_map.items():
        if name_clean[:8] in k or k[:8] in name_clean:
            return v
    return None

# Pattern to find name and price in each stock block
stock_pattern = re.compile(
    r"name:\s*'([^']+)'.*?shortName:\s*'([^']+)'.*?price:\s*(\d+(?:\.\d+)?).*?prevPrice:\s*(\d+(?:\.\d+)?)",
    re.DOTALL
)

updates = 0
def replace_prices(m):
    global updates
    name = m.group(1)
    shortname = m.group(2)
    match = match_name(shortname) or match_name(name)
    if match:
        new_price, new_prev = match
        result = m.group(0).replace(
            f"price: {m.group(3)}",
            f"price: {new_price}"
        ).replace(
            f"prevPrice: {m.group(4)}",
            f"prevPrice: {new_prev}"
        )
        updates += 1
        return result
    return m.group(0)

# Replace prices carefully per stock block
blocks = re.split(r'(?=\s*\{\s*\n\s*name:)', content)
updated_blocks = []
for block in blocks:
    m = re.search(r"name:\s*'([^']+)'.*?shortName:\s*'([^']+)'.*?price:\s*(\d+(?:\.\d+)?).*?prevPrice:\s*(\d+(?:\.\d+)?)", block, re.DOTALL)
    if m:
        name = m.group(1)
        shortname = m.group(2)
        match = match_name(shortname) or match_name(name)
        if match:
            new_price, new_prev = match
            block = block.replace(
                f"price: {m.group(3)},",
                f"price: {new_price},"
            )
            block = block.replace(
                f"prevPrice: {m.group(4)},",
                f"prevPrice: {new_prev},"
            )
            updates += 1
    updated_blocks.append(block)

new_content = ''.join(updated_blocks)
with open('js/shares-data.js', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Updated {updates} stock prices from Excel data")
