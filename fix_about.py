with open('about.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
c = re.sub(
    r'<!-- Big Logo in center top -->\s*<img src="images/logo\.png"[^>]*>\s*<h1 class="text-gradient"[^>]*>About MDB ARTHASPHERE</h1>',
    '''<!-- Big Logo and Title horizontally centered -->
        <div style="display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 24px; flex-wrap: wrap;">
          <img src="images/logo.png" alt="MDB Arthasphere Logo" style="height: 80px; width: auto; object-fit: contain;">
          <h1 class="text-gradient" style="margin: 0; font-size: 36px;">About MDB ARTHASPHERE</h1>
        </div>''',
    c
)

with open('about.html', 'w', encoding='utf-8') as f:
    f.write(c)
