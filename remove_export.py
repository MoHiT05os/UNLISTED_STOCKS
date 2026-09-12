import re

with open('screener.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<a href="#"[^>]*onclick="alert\(\'Export feature coming soon!\'\)"[^>]*>.*?</a>', '', content, flags=re.DOTALL)

with open('screener.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated screener.html")
