"""
Utility functions for AIImageGen
"""

import os
import hashlib
from datetime import datetime
from pathlib import Path
from PIL import Image

def generate_filename(prompt, provider, timestamp=None):
    """Generate a unique filename based on prompt and provider"""
    if timestamp is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create a short hash from the prompt
    prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
    
    return f"{provider}_{timestamp}_{prompt_hash}.png"

def ensure_output_dir(output_dir):
    """Ensure output directory exists"""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path

def resize_image(image_path, size):
    """Resize an image to specified dimensions"""
    try:
        with Image.open(image_path) as img:
            if isinstance(size, str):
                width, height = map(int, size.split('x'))
            else:
                width, height = size
            
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            resized.save(image_path)
            return True
    except Exception as e:
        print(f"Error resizing image: {e}")
        return False

def get_image_info(image_path):
    """Get basic info about an image file"""
    try:
        with Image.open(image_path) as img:
            return {
                'size': img.size,
                'format': img.format,
                'mode': img.mode,
                'file_size': os.path.getsize(image_path)
            }
    except Exception as e:
        print(f"Error getting image info: {e}")
        return None

def validate_size_string(size_str):
    """Validate size string format (e.g., '1024x1024')"""
    try:
        parts = size_str.split('x')
        if len(parts) != 2:
            return False
        width, height = map(int, parts)
        return width > 0 and height > 0
    except ValueError:
        return False