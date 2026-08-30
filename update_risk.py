import os

with open('screener.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "parseFloat(risk) <= 4 ? '#10b981' : parseFloat(risk) <= 7 ? '#f59e0b' : '#ef4444'",
    "parseFloat(risk) >= 7 ? '#10b981' : parseFloat(risk) >= 4 ? '#f59e0b' : '#ef4444'"
)

with open('screener.html', 'w', encoding='utf-8') as f:
    f.write(content)

with open('js/components.js', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace(
    "(riskScore <= 3 ? '#10b981' : riskScore <= 6 ? '#f59e0b' : '#ef4444')",
    "(riskScore >= 7 ? '#10b981' : riskScore >= 4 ? '#f59e0b' : '#ef4444')"
)

with open('js/components.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Risk score logic updated.")
