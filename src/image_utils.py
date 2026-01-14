"""
Image optimization utilities for memory-efficient display
"""
from PIL import Image
import io
import base64

def optimize_image_for_web(image_path, max_width=1200, quality=75):
    """
    Resize and compress image for web display to reduce memory usage
    
    Args:
        image_path: Path to original image
        max_width: Maximum width in pixels (default 1200)
        quality: JPEG quality 1-100 (default 75)
    
    Returns:
        Base64 encoded image string or None if error
    """
    try:
        # Open image
        img = Image.open(image_path)
        
        # Calculate new size maintaining aspect ratio
        width, height = img.size
        if width > max_width:
            ratio = max_width / width
            new_size = (max_width, int(height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Convert to RGB if needed (for JPEG)
        if img.mode in ('RGBA', 'P', 'LA'):
            # Create white background
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA' or img.mode == 'LA':
                background.paste(img, mask=img.split()[-1])  # Use alpha channel as mask
            else:
                background.paste(img)
            img = background
        
        # Save to bytes with compression
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        # Encode to base64
        img_str = base64.b64encode(buffer.read()).decode()
        return f"data:image/jpeg;base64,{img_str}"
        
    except Exception as e:
        print(f"Error optimizing image {image_path}: {e}")
        return None

def get_image_html(image_path, max_width=1200, quality=75):
    """
    Get HTML img tag with optimized image
    
    Args:
        image_path: Path to image file
        max_width: Max width for optimization
        quality: JPEG quality
    
    Returns:
        HTML string with img tag
    """
    img_data = optimize_image_for_web(image_path, max_width, quality)
    
    if img_data:
        return f'<img src="{img_data}" style="width: 100%; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">'
    else:
        return f'<p style="color: #64748B;">Unable to load image: {image_path}</p>'
