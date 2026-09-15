import glob
import re

for f in glob.glob('*.html'):
    with open(f, 'r', encoding='utf-8') as file:
        c = file.read()
    
    # Let's just do a direct string split and replace
    if '<div class="ftop">' in c:
        start = c.find('<div class="ftop">')
        if '<div class="disclaimer">' in c[start:]:
            end = c.find('<div class="disclaimer">', start)
            c = c[:start] + c[end:]
        elif '<div class="footer-cols">' in c[start:]:
            end = c.find('<div class="footer-cols">', start)
            c = c[:start] + c[end:]
        elif '<div class="fbottom">' in c[start:]:
            end = c.find('<div class="fbottom">', start)
            c = c[:start] + c[end:]
            
        with open(f, 'w', encoding='utf-8') as file:
            file.write(c)
        print("Fixed", f)
