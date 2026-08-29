import os, re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Change H1 text
c = re.sub(r'Invest in India\'s<br>Next Big <em[^>]*>Stories</em>', 'All <em>unlisted</em> & pre-IPO shares', c)

# 2. Extract Top Sectors
# Look for <section class="section tint"> containing Top sectors
m = re.search(r'(\s*<section class=\"section tint\">[\s\S]*?Top sectors[\s\S]*?</section>)', c)
top_sectors = ''
if m:
    top_sectors = m.group(1)
    c = c.replace(top_sectors, '\n')

# 3. Remove Market Movers
# It looks like: <!-- Market Movers Grid --> ... <div class="movers-grid" id="movers-grid"></div>
m_movers = re.search(r'<!-- Market Movers Grid -->[\s\S]*?<div class=\"movers-grid\" id=\"movers-grid\"></div>', c)
if m_movers:
    c = c.replace(m_movers.group(0), '')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

if top_sectors:
    with open('screener.html', 'r', encoding='utf-8') as f:
        sc = f.read()
    
    # Remove tabs from screener.html
    sc = re.sub(r'<div class=\"screener-tabs\">[\s\S]*?</div>\s*', '', sc)
    
    # Remove panels and add Top Sectors
    # The panels start at <!-- HEATMAPS Panel --> and go to before </main>
    # In screener.html, it's followed by </main>
    # Let's replace everything from HEATMAPS Panel up to </main>
    sc = re.sub(r'<!-- HEATMAPS Panel -->[\s\S]*?(?=</main>)', top_sectors + '\n', sc)

    with open('screener.html', 'w', encoding='utf-8') as f:
        f.write(sc)
