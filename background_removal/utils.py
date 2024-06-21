import requests
from PIL import Image, ImageOps
from io import BytesIO
from django.conf import settings
from .tests import generate_and_save_image
from .serializers import ImageUploadSerializer
import os


def remove_background(image_file):
    api_key = os.getenv('REMOVE_BG_API_KEY')
    remove_bg_url = 'https://api.remove.bg/v1.0/removebg'

    files = {'image_file': image_file}
    headers = {'X-Api-Key': api_key}

    response = requests.post(remove_bg_url, files=files, headers=headers)

    if response.status_code == 200:
        return response.content 
    else:
        return None  

def add_background(processed_image_content, bg_option=None, bg_color=None, bg_image=None,bg_prompt=None):
    original = Image.open(BytesIO(processed_image_content)).convert("RGBA")
    
    if bg_option == 'white':
        background = Image.new("RGBA", original.size, (255, 255, 255))
    elif bg_option == 'color' and bg_color:
        background = Image.new("RGBA", original.size, bg_color)
    elif bg_option == 'image' and bg_image:
        bg = Image.open(bg_image).convert("RGBA")
        background = ImageOps.fit(bg, original.size)
    elif bg_option == 'prompt' and bg_prompt:
        bg = Image.open(bg_prompt).convert("RGBA")
        background = ImageOps.fit(bg, original.size)
    else:
        return original  # No background

    composite = Image.alpha_composite(background, original)
    output = BytesIO()
    composite.save(output, format="PNG")
    return output.getvalue()
