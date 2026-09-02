"""
Add Events nav link to all HTML pages (before About).
"""
import glob, re

files = [f for f in glob.glob('*.html') if f != 'events.html']
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has events link
    if 'events.html' in content:
        print(f'SKIP (has it): {fname}')
        continue

    # Insert Events link before About link in nav
    for pattern in [
        ('href="about.html">About', 'href="events.html">Events</a>\n        <a href="about.html">About'),
        ("href='about.html'>About", "href='events.html'>Events</a>\n        <a href='about.html'>About"),
    ]:
        if pattern[0] in content:
            content = content.replace(pattern[0], pattern[1])
            break

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed: {fname}')

print('Done')
