import os
import glob

html_files = glob.glob('*.html')
for file in html_files:
    if file in ['login.html', 'signup.html']:
        continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace header sign in button
    content = content.replace('<button class="btn btn-ghost hide-sm">Sign In</button>', '<a href="login.html" class="btn btn-ghost hide-sm" style="text-decoration:none;display:inline-flex;align-items:center;">Sign In</a>')
    
    # Replace footer sign in button
    content = content.replace('<button class="btn btn-ghost">Sign In</button>', '<a href="login.html" class="btn btn-ghost" style="text-decoration:none;display:inline-flex;align-items:center;">Sign In</a>')
    
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

print('Updated Sign In links across all HTML files.')
