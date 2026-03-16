from PIL import Image
import os

uploads_dir = 'static/uploads'
target_size = (1021, 576)

for filename in os.listdir(uploads_dir):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        filepath = os.path.join(uploads_dir, filename)
        img = Image.open(filepath)
        
        # Convert RGBA to RGB for JPEG
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        
        img_resized = img.resize(target_size, Image.LANCZOS)
        img_resized.save(filepath, quality=95)
        print(f'Resized: {filename}')

print('All images resized to 1021x576 pixels')
