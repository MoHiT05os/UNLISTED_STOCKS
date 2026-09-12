import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('<h2>Rated <em>4.9</em> by investors</h2>', '<h2>Trusted by investors</h2>')
content = re.sub(r'<div style="text-align: right;">\s*<div[^>]*>4\.9 <span[^>]*>[^<]*</span></div>\s*</div>', '', content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
