import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── Fix 1: Replace dark placeholder divs in blog cards with real gradient images ──
articles = [
    {
        'gradient': 'linear-gradient(135deg, #1e3a5f 0%, #0f2027 50%, #1a1a2e 100%)',
        'icon': '📊',
        'tag': 'IPO ANALYSIS',
        'title': 'Swiggy DRHP Filed: What it means for unlisted investors',
        'desc': "A deep dive into Swiggy's latest DRHP filing, financials, and how it impacts the current unlisted market premium.",
        'delay': '',
    },
    {
        'gradient': 'linear-gradient(135deg, #1a2f1a 0%, #0a1f0a 50%, #0f2027 100%)',
        'icon': '🚀',
        'tag': 'COMPANY RESEARCH',
        'title': "Zepto's rapid rise in the quick commerce space",
        'desc': "Analyzing Zepto's unit economics, expansion plans, and valuation jump in the recent funding rounds.",
        'delay': 'reveal-delay-1',
    },
    {
        'gradient': 'linear-gradient(135deg, #2d1b4e 0%, #1a0f3d 50%, #0f1429 100%)',
        'icon': '💡',
        'tag': 'GUIDE',
        'title': 'The ultimate guide to liquidity events for startup employees',
        'desc': 'How and when can you sell your vested ESOPs? Understanding lock-in periods, buybacks, and secondary sales.',
        'delay': 'reveal-delay-2',
    },
]

new_blog_grid = '''        <div class="grid-3">
'''

for a in articles:
    delay_class = f'reveal {a["delay"]}'.strip()
    new_blog_grid += f'''          <div class="blog-card reveal {a['delay']}">
            <div style="height: 180px; background: {a['gradient']}; border-radius: var(--radius-md); margin-bottom: 16px; display:flex; align-items:center; justify-content:center; position:relative; overflow:hidden;">
              <span style="font-size:64px; opacity:0.35; user-select:none;">{a['icon']}</span>
              <div style="position:absolute; bottom:12px; right:12px; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:rgba(255,255,255,0.4); background:rgba(0,0,0,0.3); padding:4px 8px; border-radius:4px;">{a['tag']}</div>
            </div>
            <div style="font-size: 12px; color: var(--primary); font-weight: 600; margin-bottom: 8px;">{a['tag']}</div>
            <h4 style="margin-bottom: 12px; font-size: 18px;">{a['title']}</h4>
            <p class="text-muted" style="font-size: 14px; margin-bottom: 16px;">{a['desc']}</p>
            <a href="#" class="more-link" style="font-size: 14px;">Read article &rarr;</a>
          </div>
'''

new_blog_grid += '        </div>'

# Replace old grid-3
content = re.sub(
    r'<div class="grid-3">.*?</div>\s*</div>\s*</section>',
    new_blog_grid + '\n      </div>\n    </section>',
    content,
    count=1,
    flags=re.DOTALL
)

# ── Fix 2: Fix ticker — remove display:none that was overriding sticky ──────
# Also ensure it reads SHARES_DATA properly
# The issue is ribbon.js tries backend first, showing NSE stocks from backend
# Force SHARES_DATA in ribbon by removing backend fallback entirely
# Already done in previous ribbon.js rewrite — but ticker may cache old one

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Blog card images updated.')
