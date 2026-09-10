import json
with open('js/shares-data.js', 'r', encoding='utf-8') as f:
    content = f.read()
start = content.find('window.SHARES_DATA = ') + len('window.SHARES_DATA = ')
end = content.find(';\n  window.SECTORS_DATA =')
shares_json = content[start:end]
shares = json.loads(shares_json)

search_terms = ['nse', 'jio', 'oyo', 'sbi', 'hero', 'cochin', 'studds', 'lava', 'gas', 'arohan', 'sembcorp', 'ags', 'vikram', 'sambhv', 'fincorp']
for term in search_terms:
    print(f'-- {term.upper()} --')
    for s in shares:
        name = str(s.get('name', ''))
        short = str(s.get('shortName', ''))
        if term.lower() in name.lower() or term.lower() in short.lower():
            print(f"  {name} | {short}")
