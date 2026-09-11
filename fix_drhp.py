import re

with open('drhp.html', 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'class="stage-card" style="background: #[a-fA-F0-9]+; color: #[a-fA-F0-9]+;"', 'class="stage-card" style="background: rgba(255,255,255,0.03); color: var(--text); border: 1px solid var(--border);"', content)
content = re.sub(r'class="card-pill" style="background: #[a-fA-F0-9]+; color: #[a-fA-F0-9]+;"', 'class="card-pill" style="background: rgba(212,175,55,0.15); color: var(--primary);"', content)
content = re.sub(r'class="card-timeline" style="background: rgba\([^)]+\); color: #[a-fA-F0-9]+;"', 'class="card-timeline" style="background: rgba(255,255,255,0.05); color: var(--text-muted);"', content)

with open('drhp.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated drhp.html")
