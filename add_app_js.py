import glob
for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    if 'js/app.js' not in c:
        c = c.replace('</body>', '  <script src="js/app.js"></script>\n</body>')
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)
        print('Added app.js to', f)
