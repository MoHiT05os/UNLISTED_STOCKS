import glob

# Inline script to prevent flash — reads localStorage BEFORE any CSS
ANTI_FLASH_SCRIPT = '<script>!function(){var t=localStorage.getItem(\'unlisted_theme\');document.documentElement.setAttribute(\'data-theme\',t||\'light\')}()</script>'

# Inline style so even before CSS loads, background is white
ANTI_FLASH_STYLE = '<style>html,body{background:#f8fafc !important;color:#0f172a !important;}</style>'

files = glob.glob('*.html')
for fname in files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove any residual data-theme="dark" on <html> tag (we set it via JS now)
    content = content.replace(' data-theme="dark"', '').replace(" data-theme='dark'", '')
    content = content.replace(' data-theme="light"', '').replace(" data-theme='light'", '')

    # Add anti-flash inline style + script right after <head>
    if ANTI_FLASH_SCRIPT not in content:
        content = content.replace('<head>', '<head>\n  ' + ANTI_FLASH_STYLE + '\n  ' + ANTI_FLASH_SCRIPT)

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed: {fname}')

print('All files updated.')
