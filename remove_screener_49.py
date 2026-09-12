import re

with open('screener.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<div style="width:1px;height:32px;background:var\(--border\);"></div>\s*<div style="text-align:center;">\s*<div style="font-size:20px;font-weight:800;color:[^>]+>4\.9[^<]*</div>\s*<div[^>]+>Google Rating</div>\s*</div>', '', content)

with open('screener.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated screener.html")
