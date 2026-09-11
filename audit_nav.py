"""
Find all navbar blocks in every HTML file so we know what each one has.
"""
import os, re

NAV_CANONICAL = """      <nav class="nav-links" id="nav-links">
        <a href="index.html">Home</a>
        <a href="screener.html">Screener</a>
        <a href="drhp.html">DRHP</a>
        <a href="ipo-gmp.html">IPO</a>
        <a href="events.html">Events</a>
        <a href="about.html">About</a>
      </nav>"""

files = sorted(f for f in os.listdir('.') if f.endswith('.html'))

for fname in files:
    content = open(fname, 'r', encoding='utf-8', errors='replace').read()
    # Extract nav block
    m = re.search(r'<nav class="nav-links"[^>]*>(.*?)</nav>', content, re.DOTALL)
    if m:
        nav = m.group(0)
        links = re.findall(r'href="([^"]+)"[^>]*>(.*?)</a>', nav)
        link_summary = [(h, t.strip()[:30]) for h, t in links]
        print(f"{fname}: {link_summary}")
    else:
        print(f"{fname}: NO NAV FOUND")
