import glob
import re

for filepath in glob.glob('*.html'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The block starts with <section class="section app-promo"> and ends with </section>
    # Since there are no nested <section> tags inside this section, `.*?</section>` should work.
    # WAIT! Why did it fail before?
    # Because my python script was `re.sub(r'<section[^>]*app-promo[^>]*>.*?</section>', '', content, flags=re.DOTALL)`.
    # Did it fail?
    # Let me try replacing everything from <!-- 13. App Promo --> up to <!-- 14. Footer -->
    
    # Actually, let's just do a manual find and string slice.
    while '<section class="section app-promo">' in content:
        start = content.find('<section class="section app-promo">')
        # Find the next </section> after start
        end = content.find('</section>', start)
        if end != -1:
            end += len('</section>')
            content = content[:start] + content[end:]
        else:
            break
            
    # Also remove the comment if it exists
    content = content.replace('<!-- 13. App Promo -->', '')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned", filepath)
