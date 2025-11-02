from PIL import Image, ImageDraw
import os

# Create icons directory if it doesn't exist
os.makedirs('/app/frontend/static/icons', exist_ok=True)

sizes = [72, 96, 128, 144, 152, 192, 384, 512]
for size in sizes:
    # Create a pink background with white circle (BFF logo style)
    img = Image.new('RGB', (size, size), '#FF69B4')
    draw = ImageDraw.Draw(img)
    
    # Draw a white circle in the center
    center = size // 2
    radius = size // 3  # Slightly larger circle
    
    # Draw the circle
    draw.ellipse([
        center - radius, 
        center - radius, 
        center + radius, 
        center + radius
    ], fill='white')
    
    # Save the icon
    img.save(f'/app/frontend/static/icons/icon-{size}x{size}.png')
    print(f'Generated icon: {size}x{size}')
