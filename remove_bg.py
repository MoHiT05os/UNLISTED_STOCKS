from PIL import Image

def remove_white_background(image_path, output_path, tolerance=240):
    img = Image.open(image_path).convert("RGBA")
    data = img.getdata()
    
    new_data = []
    for item in data:
        # Check if the pixel is white-ish
        if item[0] > tolerance and item[1] > tolerance and item[2] > tolerance:
            # Replace it with a transparent pixel
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)
            
    img.putdata(new_data)
    img.save(output_path, "PNG")
    print("Background removed and saved to", output_path)

remove_white_background('images/logo.png', 'images/logo_transparent.png', 230)
