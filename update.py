import os

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

for file in html_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Base rebranding
    content = content.replace('UnlistedZone', 'SECRET LIST')
    content = content.replace('Unlisted Zone', 'SECRET LIST')
    
    # 2. Logo abbreviation
    content = content.replace('>UZ<', '>SL<')
    
    # 3. Address update
    content = content.replace('Level 2, Raheja Centre, Nariman Point, Mumbai, Maharashtra 400021', 'Lucknow, Uttar Pradesh')
    content = content.replace('Mumbai', 'Lucknow')
    
    # 4. Header brand replacement (TRMY House branding)
    brand_old = '''<a href="index.html" class="brand">
        <div class="logo-wrap">SL</div>
        SECRET LIST
      </a>'''
    brand_new = '''<a href="index.html" class="brand" style="display:flex; align-items:center; gap:12px; text-decoration:none;">
        <div class="logo-wrap">SL</div>
        <div style="display:flex; flex-direction:column; line-height:1.2;">
            <span style="font-weight:700; letter-spacing:0.5px; font-size: 20px;">SECRET LIST</span>
            <span style="font-size:11px; font-weight:500; opacity:0.8; color: var(--primary);">from the house of TRMY</span>
        </div>
      </a>'''
    
    content = content.replace(brand_old, brand_new)
    
    # 5. Footer brand replacement
    fbrand_old = '''<div class="fbrand">
          <div class="fmono-img">SL</div>
          <div>
            <div class="fbn">SECRET LIST</div>'''
    
    fbrand_new = '''<div class="fbrand">
          <div class="fmono-img">SL</div>
          <div>
            <div class="fbn">SECRET LIST</div>
            <div style="font-size:12px; font-weight:500; color:var(--primary); margin-top:4px;">from the house of TRMY</div>'''
    
    content = content.replace(fbrand_old, fbrand_new)
    
    # Write back
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

# CSS Update for max-width
css_file = 'css/design-system.css'
with open(css_file, 'r', encoding='utf-8') as f:
    css = f.read()
css = css.replace('max-width: 1200px;', 'max-width: 1600px;')
with open(css_file, 'w', encoding='utf-8') as f:
    f.write(css)

print("Update completed successfully.")
