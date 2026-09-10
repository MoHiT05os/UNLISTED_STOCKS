"""
Batch updater for MDB Arthasphere:
1. Replace all old address references with new Gurugram address
2. Replace 255+ with 1000+
"""
import os

OLD_ADDR_VARIANTS = [
    'Lucknow, Uttar Pradesh',
    'Lucknow, UP',
    'New Delhi, India',
    'Mumbai, Maharashtra',
]
NEW_ADDR = 'Sector 17-B, Block F, South City I, Sector 41, Gurugram, Haryana 122003'
NEW_ADDR_SHORT = 'Gurugram, Haryana 122003'

files_to_update = [f for f in os.listdir('.') if f.endswith('.html')]

total_changes = 0

for filename in sorted(files_to_update):
    try:
        content = open(filename, 'r', encoding='utf-8', errors='replace').read()
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        continue

    original = content

    # 1. Replace all old address variants
    for old in OLD_ADDR_VARIANTS:
        if old in content:
            content = content.replace(old, NEW_ADDR)
            print(f"  {filename}: address replaced '{old}' -> Gurugram")

    # 2. Replace 255+ shares → 1000+ (be careful not to replace CSS "rgba(255,..." etc)
    # Only replace when in readable text context
    for old, new in [
        ('>255+<', '>1000+<'),
        ('"255+"', '"1000+"'),
        ("'255+'", "'1000+'"),
        ('>255+\n', '>1000+\n'),
        ('Filter 255+', 'Filter 1000+'),
        ('255+ Shares', '1000+ Shares'),
        ('255+ shares', '1000+ shares'),
        ('255+ unlisted', '1000+ unlisted'),
    ]:
        if old in content:
            content = content.replace(old, new)
            print(f"  {filename}: {old} -> {new}")

    if content != original:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        total_changes += 1

print(f"\nDone. Updated {total_changes} files.")
