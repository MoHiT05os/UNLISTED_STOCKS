import re

# ── Fix 1: Add DRHP link to navs that are missing it ──────────────────────
files_to_fix = ['screener.html', 'about.html', 'shares.html', 'contact.html']

for fname in files_to_fix:
    try:
        with open(fname, 'r', encoding='utf-8') as f:
            content = f.read()

        if 'drhp.html' in content:
            print(f'{fname}: DRHP link already exists')
            continue

        # Add DRHP after screener or home link in nav
        if 'href="screener.html">Screener</a>' in content:
            content = content.replace(
                'href="screener.html">Screener</a>',
                'href="screener.html">Screener</a>\n        <a href="drhp.html">DRHP</a>'
            )
            with open(fname, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'{fname}: Added DRHP link')
        else:
            print(f'{fname}: Could not find screener link to insert after')
    except FileNotFoundError:
        print(f'{fname}: File not found')

# ── Fix 2: Risk score - simple Green/Red only (>5 = red, <=5 = green) ─────
print()

# Fix in screener.html
with open('screener.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Current: parseFloat(risk) >= 7 ? '#10b981' : parseFloat(risk) >= 4 ? '#f59e0b' : '#ef4444'
# New:     parseFloat(risk) > 5 ? '#ef4444' : '#10b981'
content = content.replace(
    "parseFloat(risk) >= 7 ? '#10b981' : parseFloat(risk) >= 4 ? '#f59e0b' : '#ef4444'",
    "parseFloat(risk) > 5 ? '#ef4444' : '#10b981'"
)

with open('screener.html', 'w', encoding='utf-8') as f:
    f.write(content)
print('screener.html: Risk color fixed')

# Fix in components.js
with open('js/components.js', 'r', encoding='utf-8') as f:
    content = f.read()

# Current: (riskScore >= 7 ? '#10b981' : riskScore >= 4 ? '#f59e0b' : '#ef4444')
# New:     (riskScore > 5 ? '#ef4444' : '#10b981')
content = content.replace(
    "(riskScore >= 7 ? '#10b981' : riskScore >= 4 ? '#f59e0b' : '#ef4444')",
    "(riskScore > 5 ? '#ef4444' : '#10b981')"
)

with open('js/components.js', 'w', encoding='utf-8') as f:
    f.write(content)
print('components.js: Risk color fixed')

print()
print('All fixes applied.')
