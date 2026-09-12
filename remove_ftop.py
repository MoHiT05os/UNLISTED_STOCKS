import glob
import re

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The block looks like:
    # <div class="ftop">
    #   <div class="fbrand">...</div>
    #   <div class="fcta">...</div>
    # </div>
    
    # We can match from <div class="ftop"> up to the first <div class="footer-cols">
    # and replace it with just <div class="footer-cols">
    content = re.sub(r'<div class="ftop">.*?<div class="footer-cols">', '<div class="footer-cols">', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned", filepath)
