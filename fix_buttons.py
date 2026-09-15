import glob
import re

search_btn = '''
        <button class="search-trigger" aria-label="Search" title="Search (Ctrl+K)">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>
        </button>'''

theme_btn = '''
        <button class="theme-toggle" id="theme-toggle" aria-label="Toggle Dark Mode">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>'''

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    modified = False
    
    if 'class="search-trigger"' not in c:
        c = c.replace('<div class="header-actions">', '<div class="header-actions">' + search_btn)
        modified = True
        
    if 'class="theme-toggle"' not in c:
        if 'class="search-trigger"' in c:
            # Insert after search trigger
            c = re.sub(r'(<button class="search-trigger"[^>]*>.*?</button>)', r'\1' + '\n' + theme_btn, c, flags=re.DOTALL)
        else:
            c = c.replace('<div class="header-actions">', '<div class="header-actions">' + theme_btn)
        modified = True
        
    if modified:
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)
        print('Fixed buttons in', f)
