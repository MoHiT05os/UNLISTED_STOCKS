import re

path = r'C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS\js\shares-data.js'
with open(path, encoding='utf-8') as f:
    content = f.read()

fixed = re.sub(
    r"(icon:\s*'[^']*')(\s*\n\s+foundedYear:)",
    r"\1,\2",
    content
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)

print("Fixed icon commas.")
