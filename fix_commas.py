import re

path = r'C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS\js\shares-data.js'
with open(path, encoding='utf-8') as f:
    content = f.read()

# Fix: asOf: '...' without trailing comma, followed by foundedYear
# The inject_metrics script inserted fields after asOf without adding comma to asOf
fixed = re.sub(
    r"(asOf:\s*'[^']*')(\s*\n\s+foundedYear)",
    r"\1,\2",
    content
)

count = len(re.findall(r"asOf:\s*'[^']*'", content))
fixed_count = len(re.findall(r"asOf:\s*'[^']*',", fixed))
print(f"asOf entries total: {count}")
print(f"asOf entries with comma after fix: {fixed_count}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(fixed)

print("Done!")
