import os, re

ROOT = r"C:\Users\TheRealMohitYadav\Videos\UNLISTED_STOCKS"

# ── NEW HEADER BRAND BLOCK ──────────────────────────────────────────────────
NEW_BRAND = '''<a href="index.html" class="brand" style="display:flex; align-items:center; text-decoration:none;">
        <img src="images/logo.png" alt="MDB Arthasphere" style="height:52px; width:auto; object-fit:contain;" />
      </a>'''

# ── Pattern that matches the old brand block (both ASSET BOX variants) ──────
OLD_BRAND_PATTERN = re.compile(
    r'<a href="index\.html" class="brand".*?</a>',
    re.DOTALL
)

html_files = [f for f in os.listdir(ROOT) if f.endswith('.html')]

for fname in html_files:
    path = os.path.join(ROOT, fname)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Replace brand block with logo image
    content = OLD_BRAND_PATTERN.sub(NEW_BRAND, content, count=1)

    # 2. Replace all text occurrences of "ASSET BOX" with "MDB ARTHASPHERE"
    content = content.replace('ASSET BOX', 'MDB ARTHASPHERE')

    # 3. Update page <title> if it mentions the old name
    content = content.replace('| ASSET BOX', '| MDB ARTHASPHERE')

    # 4. Update footer mono-img initials (AB -> MA)
    content = content.replace(
        'fmono-img" style="background: linear-gradient(135deg, #10b981, #059669); font-weight:800; font-size:13px;">AB<',
        'fmono-img" style="background: linear-gradient(135deg, #10b981, #059669); font-weight:800; font-size:13px;">MA<'
    )

    # 5. Update fbn div text
    content = content.replace('<div class="fbn">MDB ARTHASPHERE</div>', '<div class="fbn">MDB ARTHASPHERE</div>')

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {fname}")
    else:
        print(f"No changes: {fname}")

print("Done!")
