import glob
import re

theme_btn = '''
        <button class="theme-toggle" id="theme-toggle" aria-label="Toggle Dark Mode">
          <svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path></svg>
        </button>'''

search_btn_pattern = re.compile(r'(<button class="search-trigger"[^>]*>.*?</button>)', re.DOTALL)

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    if 'class="theme-toggle"' not in c:
        c = search_btn_pattern.sub(r'\1' + '\n' + theme_btn, c)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)
        print('Added to', f)
