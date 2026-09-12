import re
import glob

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Google Rating div blocks
    content = re.sub(r'<div style="text-align:center;">\s*<div[^>]*>4\.9 &#9733;</div>\s*<div[^>]*>Google Rating</div>\s*</div>', '', content)
    
    # 2. Remove "Based on 750+ Google Reviews"
    content = re.sub(r'<div[^>]*>Based on 750\+ Google Reviews</div>', '', content)
    
    # 3. Remove screener.html Google Rating
    content = re.sub(r'<div style="width:1px;height:32px;background:var\(--border\);"></div>\s*<div style="text-align:center;">\s*<div style="font-size:20px;font-weight:800;color:var\(--primary\);">4\.9&#9733;</div>\s*<div style="font-size:11px;color:var\(--text-muted\);font-weight:600;text-transform:uppercase;letter-spacing:0\.5px;">Google Rating</div>\s*</div>', '', content)

    # 4. Remove App Download section from footers (It usually comes after "Connect" or similar)
    # The user wants to remove the app download section entirely.
    # Usually it looks like:
    # <div>
    #   <h4 class="footer-heading">Get the App</h4>
    #   <div style="display:flex;gap:12px;margin-top:16px;">
    #     <img src="...Google_Play_Store_badge_EN.svg"...>
    #     <img src="...Download_on_the_App_Store_Badge.svg"...>
    #   </div>
    # </div>
    # Let's write a regex that matches the whole div containing the badges.
    content = re.sub(r'<div>\s*<h4 class="footer-heading">[^<]*App[^<]*</h4>\s*<div[^>]*>\s*<img[^>]*Google_Play_Store_badge[^>]*>\s*<img[^>]*App_Store_Badge[^>]*>\s*</div>\s*</div>', '', content)
    
    # Also handle if it is slightly different formatted
    content = re.sub(r'<div[^>]*>\s*<h4[^>]*>.*?App.*?</h4>\s*<div[^>]*>\s*<img[^>]*Google_Play.*?App_Store.*?\s*</div>\s*</div>', '', content, flags=re.DOTALL)
    
    # If the regex doesn't catch it, let's just strip the badges directly as a fallback, but the whole column is better.
    # I'll just write a very broad regex for the app column
    pattern = r'<div(?:(?!\s*<div).)*?Google_Play_Store_badge.*?</div>\s*</div>'
    content = re.sub(pattern, '', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Cleaned", filepath)

for f in glob.glob('*.html'):
    clean_file(f)
