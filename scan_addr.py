import os

search_terms = ['255+', 'address', 'Gurugram', 'gurugram', 'office', 'registered', 
                'South City', 'Sector 17', 'footer-address', 'contact-info',
                'New Delhi', 'Mumbai', 'Bengaluru', 'location']

for f in sorted(os.listdir('.')):
    if not f.endswith('.html'):
        continue
    try:
        lines = open(f, 'r', encoding='utf-8', errors='replace').readlines()
    except:
        continue
    for i, l in enumerate(lines, 1):
        l_lower = l.lower()
        if any(t.lower() in l_lower for t in search_terms):
            clean = l.encode('ascii', 'replace').decode().strip()[:160]
            print(f"{f}:{i}: {clean}")
