import re, os

# ─────────────────────────────────────────────────────────────
# HELPER
# ─────────────────────────────────────────────────────────────
def read(f):
    with open(f, 'r', encoding='utf-8') as fh:
        return fh.read()

def write(f, c):
    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(c)
    print(f"  ✓ Saved {f}")

# ─────────────────────────────────────────────────────────────
# 1. index.html  — multiple changes
# ─────────────────────────────────────────────────────────────
print("\n== index.html ==")
c = read('index.html')

# 1a. "most trusted" → "India's trusted"
c = c.replace("India's Most Trusted Unlisted Shares Platform", "India's Trusted Unlisted Shares Platform")
print("  • Replaced 'Most Trusted' → 'Trusted'")

# 1b. Remove the small gold tagline "— INVEST | GROW | PROSPER —"
c = re.sub(
    r'<p style="font-size:13px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var\(--primary\);margin-bottom:44px;opacity:0\.9;"\s*>\s*— INVEST.*?PROSPER —\s*</p>',
    '',
    c, flags=re.DOTALL
)
print("  • Removed duplicate small 'INVEST | GROW | PROSPER' tagline")

# 1c. Happy investors: 10,000+ → 100+
c = c.replace('<div style="font-size:32px;font-weight:900;color:var(--text);letter-spacing:-1px;">10,000+</div>', 
              '<div style="font-size:32px;font-weight:900;color:var(--text);letter-spacing:-1px;">100+</div>')
print("  • Changed Happy Investors: 10,000+ → 100+")

# 1d. "Talk to an Expert" button → themed contact card popup
#     Replace the WhatsApp link button with a button that shows contact popup
old_talk_btn = '''          <a href="https://wa.me/919354082477" class="btn btn-ghost" style="padding:18px 36px;font-size:16px;font-weight:600;border-radius:12px;" target="_blank">
            <svg width="18" height="18" fill="currentColor" viewBox="0 0 24 24" style="margin-right:8px;"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51a12.8 12.8 0 00-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
            Talk to an Expert
          </a>'''

new_talk_btn = '''          <button onclick="document.getElementById('contact-modal').style.display='flex'" class="btn btn-ghost" style="padding:18px 36px;font-size:16px;font-weight:600;border-radius:12px;">
            <svg width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="margin-right:8px;"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.08 6.08l1.08-.92a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.18z"/></svg>
            Talk to an Expert
          </button>

  <!-- ── Contact Modal ── -->
  <div id="contact-modal" style="display:none;position:fixed;inset:0;z-index:9999;background:rgba(0,0,0,0.6);backdrop-filter:blur(6px);align-items:center;justify-content:center;" onclick="if(event.target===this)this.style.display='none'">
    <div style="background:var(--bg-card);border:1px solid var(--border);border-radius:20px;padding:40px;max-width:520px;width:90%;position:relative;box-shadow:0 24px 64px rgba(0,0,0,0.4);">
      <button onclick="document.getElementById('contact-modal').style.display='none'" style="position:absolute;top:16px;right:16px;background:none;border:none;color:var(--text-muted);cursor:pointer;font-size:22px;line-height:1;">✕</button>
      <div style="text-align:center;margin-bottom:32px;">
        <div style="font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:2px;color:var(--primary);margin-bottom:12px;">Get in Touch</div>
        <h2 style="font-size:26px;font-weight:800;letter-spacing:-0.5px;margin:0;">Let\'s Connect</h2>
        <p style="color:var(--text-muted);margin-top:8px;font-size:15px;">Our team is ready to guide you.</p>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
        <a href="tel:+919891222800" style="display:flex;flex-direction:column;align-items:center;gap:10px;background:rgba(var(--primary-rgb),0.07);border:1px solid rgba(var(--primary-rgb),0.2);border-radius:14px;padding:24px 16px;text-decoration:none;transition:all 0.2s;" onmouseover="this.style.background='rgba(var(--primary-rgb),0.14)';this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(var(--primary-rgb),0.07)';this.style.transform=\'\'">
          <div style="width:48px;height:48px;background:rgba(var(--primary-rgb),0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--primary);">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.08 6.08l1.08-.92a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 17.18z"/></svg>
          </div>
          <div style="text-align:center;">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:4px;">PHONE</div>
            <div style="font-size:14px;font-weight:700;color:var(--text);">+91 98912 22800</div>
          </div>
        </a>
        <a href="mailto:mdbarthasphere@gmail.com" style="display:flex;flex-direction:column;align-items:center;gap:10px;background:rgba(var(--primary-rgb),0.07);border:1px solid rgba(var(--primary-rgb),0.2);border-radius:14px;padding:24px 16px;text-decoration:none;transition:all 0.2s;" onmouseover="this.style.background='rgba(var(--primary-rgb),0.14)';this.style.transform='translateY(-2px)'" onmouseout="this.style.background='rgba(var(--primary-rgb),0.07)';this.style.transform=\'\'">
          <div style="width:48px;height:48px;background:rgba(var(--primary-rgb),0.15);border-radius:50%;display:flex;align-items:center;justify-content:center;color:var(--primary);">
            <svg width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
          </div>
          <div style="text-align:center;">
            <div style="font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;color:var(--text-muted);margin-bottom:4px;">EMAIL</div>
            <div style="font-size:13px;font-weight:700;color:var(--text);">mdbarthasphere<br>@gmail.com</div>
          </div>
        </a>
      </div>
    </div>
  </div>'''

c = c.replace(old_talk_btn, new_talk_btn)
print("  • Replaced Talk to Expert button with themed contact popup modal")

# 1e. Remove Reliance Retail from popular shares (if hardcoded)
c = re.sub(r'\{[^{}]*Reliance Retail[^{}]*\},?\s*', '', c, flags=re.DOTALL)
print("  • Removed Reliance Retail from index.html (if present)")

write('index.html', c)


# ─────────────────────────────────────────────────────────────
# 2. js/shares-data.js — remove Reliance Retail entry
# ─────────────────────────────────────────────────────────────
print("\n── js/shares-data.js ──")
c = read('js/shares-data.js')
before = len(c)
# Remove any JSON object block that contains "Reliance Retail"
c = re.sub(r'\{[^{}]*"Reliance Retail"[^{}]*\},?\s*', '', c, flags=re.DOTALL)
if len(c) < before:
    print("  • Removed Reliance Retail share entry")
else:
    print("  • (Reliance Retail not found as standalone JSON block)")
write('js/shares-data.js', c)


# ─────────────────────────────────────────────────────────────
# 3. screener.html — remove filters + fix blinking banner + change banner text
# ─────────────────────────────────────────────────────────────
print("\n── screener.html ──")
c = read('screener.html')

# 3a. Remove Geography filter group (lines 392-404)
c = re.sub(
    r'\s*<!--\s*GEOGRAPHY\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed Geography filter")

# 3b. Remove EBIT Margin from Financials filter
c = re.sub(
    r'\s*<div class="range-group">\s*<label>EBIT Margin[^<]*</label>.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed EBIT Margin filter")

# 3c. Remove EBIT Growth from Growth filter
c = re.sub(
    r'\s*<div class="range-group">\s*<label>EBIT Growth[^<]*</label>.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed EBIT Growth filter")

# 3d. Remove ARR Growth from Growth filter
c = re.sub(
    r'\s*<div class="range-group">\s*<label>ARR Growth[^<]*</label>.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed ARR Growth filter")

# 3e. Remove Seed / Angel from Funding filter (remove the whole "Seed Funding" concept)
c = c.replace('<label class="filter-sub-item"><input type="checkbox"> Seed / Angel</label>', '')
print("  • Removed Seed / Angel funding filter item")

# 3f. Remove PRICE filter group entirely
c = re.sub(
    r'\s*<!--\s*PRICE\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed Price filter group")

# 3g. Remove IPO filter group entirely
c = re.sub(
    r'\s*<!--\s*IPO\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed IPO filter group")

# 3h. Remove BUSINESS METRICS filter group
c = re.sub(
    r'\s*<!--\s*BUSINESS METRICS\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed Business Metrics filter group")

# 3i. Remove OWNERSHIP filter group
c = re.sub(
    r'\s*<!--\s*OWNERSHIP\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed Ownership filter group")

# 3j. Remove RISK filter group
c = re.sub(
    r'\s*<!--\s*RISK\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed Risk filter group")

# 3k. Remove INVESTOR filter group
c = re.sub(
    r'\s*<!--\s*INVESTOR\s*-->\s*<div class="filter-group">.*?</div>\s*</div>',
    '',
    c, flags=re.DOTALL, count=1
)
print("  • Removed Investor filter group")

# 3l. Fix blinking banner — remove animation:pulse from the eyebrow dot
#     The blinking is from the `animation:pulse` on the green dot in the hero banner
#     Screener hero eyebrow pill - remove the animation to stop blinking
c = c.replace(
    '<span style="width:7px;height:7px;background:var(--primary);border-radius:50%;display:inline-block;animation:pulse 2s infinite;"></span>\n        LIVE MARKET SCREENER',
    '<span style="width:7px;height:7px;background:var(--primary);border-radius:50%;display:inline-block;"></span>\n        LIVE MARKET SCREENER'
)
print("  • Fixed blinking banner dot (removed animation:pulse)")

# 3m. Change screener banner subtitle text
c = c.replace(
    'Filter 969+ unlisted companies by sector, risk score, EBITDA, IPO window, and more. Built for serious investors.',
    'Screen 1000+ unlisted companies by sector, market cap, and key financials. Built for serious investors.'
)
print("  • Updated screener banner description text")

write('screener.html', c)


# ─────────────────────────────────────────────────────────────
# 4. Bump CSS version to v14 across all HTML files
# ─────────────────────────────────────────────────────────────
print("\n── Bumping CSS version to v14 ──")
import glob
for fname in glob.glob('*.html'):
    c = read(fname)
    new_c = re.sub(r'css/(.*?)\.css\?v=\d+', r'css/\1.css?v=14', c)
    if new_c != c:
        write(fname, new_c)

print("\n✅ All changes applied!")
