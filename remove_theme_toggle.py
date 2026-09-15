import glob
import re

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the theme toggle button
    content = re.sub(r'<button class="theme-toggle"[^>]*>.*?</button>', '', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned", filepath)
