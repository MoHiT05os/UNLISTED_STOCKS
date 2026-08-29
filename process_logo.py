from PIL import Image
import os, shutil

# Source logo
src = r"C:\Users\TheRealMohitYadav\.gemini\antigravity\brain\5982a19f-c483-4069-a766-f093cf756d31\.user_uploaded\media_1787982040960.jpg"

# Destination
os.makedirs("images", exist_ok=True)
dest = "images/logo.png"

img = Image.open(src).convert("RGBA")
data = img.getdata()

new_data = []
for r, g, b, a in data:
    # Remove near-white pixels (background)
    if r > 230 and g > 230 and b > 230:
        new_data.append((255, 255, 255, 0))  # transparent
    else:
        new_data.append((r, g, b, a))

img.putdata(new_data)
img.save(dest)
print(f"Logo saved to {dest} ({img.size[0]}x{img.size[1]})")
