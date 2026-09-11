"""
Synchronize ALL navbar blocks across every HTML file to the canonical version.
Each page gets the same links, with only its own "active" link highlighted.
Also fixes DRHP link back to drhp.html (not SEBI).
"""
import os
import re

# Canonical nav links (same order, same labels, everywhere)
# active_href is set per-file below
NAV_LINKS = [
    ("index.html",    "Home"),
    ("screener.html", "Screener"),
    ("drhp.html",     "DRHP"),
    ("ipo-gmp.html",  "IPO"),
    ("events.html",   "Events"),
    ("about.html",    "About"),
]

# Which file is "active" (gets the green highlight)
ACTIVE_MAP = {
    "index.html":    "index.html",
    "screener.html": "screener.html",
    "drhp.html":     "drhp.html",
    "ipo-gmp.html":  "ipo-gmp.html",
    "events.html":   "events.html",
    "about.html":    "about.html",
    "shares.html":   None,
    "contact.html":  None,
    "stock.html":    None,
}

# Pages with a nav to update
FILES_WITH_NAV = [
    "index.html", "screener.html", "drhp.html", "ipo-gmp.html",
    "events.html", "about.html", "shares.html", "contact.html", "stock.html"
]

def build_nav(active_href):
    items = []
    for href, label in NAV_LINKS:
        if href == active_href:
            items.append(f'        <a href="{href}" style="color: var(--primary); font-weight: 700;">{label}</a>')
        else:
            items.append(f'        <a href="{href}">{label}</a>')
    inner = "\n".join(items)
    return f'      <nav class="nav-links" id="nav-links">\n{inner}\n      </nav>'

for fname in FILES_WITH_NAV:
    if not os.path.exists(fname):
        print(f"SKIP (not found): {fname}")
        continue

    content = open(fname, 'r', encoding='utf-8', errors='replace').read()

    # Match the nav block (handle variations in class name order, id, etc.)
    pattern = r'<nav\b[^>]*\bid="nav-links"[^>]*>.*?</nav>'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)

    if not match:
        print(f"NO NAV FOUND in {fname}")
        continue

    active = ACTIVE_MAP.get(fname)
    new_nav = build_nav(active)
    new_content = content[:match.start()] + new_nav + content[match.end():]

    if new_content != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"UPDATED: {fname}")
    else:
        print(f"already ok: {fname}")

print("\nAll navbars synchronized!")
