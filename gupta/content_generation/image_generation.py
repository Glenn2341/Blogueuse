import requests
import json
import time
import base64
import random
from PIL import Image

from models import Post

class Prompt_Anchor:
    def __init__(self, positive, negative):
        self.positive = positive
        self.negative = negative

anchor_sketch = Prompt_Anchor( 
    positive= '(painting by Aella the Huntress).  (cold) (outdoors)  (digital art) naturalistic art style, film grain, Fujifilm XT3, (Dishonored Game)',
    negative= 'blurry, deformed, distorted, game graphics'
)
anchor_landscape = Prompt_Anchor( 
    positive= 'meditation, cold weather, majestic, peaceful, high detail, outdoor landscape',
    negative= '((((big hands, un-detailed skin, semi-realistic, cgi, 3d, render, sketch, cartoon, drawing, anime)))), (((ugly mouth, ugly eyes, missing teeth, crooked teeth, close up, cropped, out of frame))), worst quality, low quality, jpeg artifacts, ugly, duplicate, morbid, mutilated, extra fingers, mutated hands, poorly drawn hands, poorly drawn face, mutation, deformed, blurry, dehydrated, bad anatomy, bad proportions, extra limbs, cloned face, disfigured, gross proportions, malformed limbs, missing arms, missing legs, extra arms, extra legs, fused fingers, too many fingers, long neck'
)
anchor_nostalgia = Prompt_Anchor(
    positive= 'crisp clear air, nostalgic, detailed, high detail, winter landscape',
    negative= 'blurry, deformed, distorted'
)
anchor_cozy = Prompt_Anchor(
    positive = 'painted art, neutral color palette, warm lighting, high detail, cozy and inviting',
    negative = 'blurry, deformed, distorted'
)
anchor_painted = Prompt_Anchor(
    positive= 'intense, detailed, painting, stylized, outdoors, cold',
    negative= 'blurry, deformed, distorted'
)
anchor_acrylic = Prompt_Anchor(
    positive= 'Acrylic painting, high contrast, bold brushstrokes, high-resolution',
    negative= 'blurry, deformed, distorted, (fuzzy lines)'
)


anchors = anchor_landscape, anchor_nostalgia, anchor_cozy, anchor_painted, anchor_acrylic #anchor_sketch,

def crop_image_width(input_file, output_file, new_width):
    img = Image.open(input_file)
    width, height = img.size

    left = (width - new_width) / 2
    top = 0
    right = (width + new_width) / 2
    bottom = height

    cropped_img = img.crop((left, top, right, bottom))
    cropped_img.save(output_file)

def resize_image(input_file, output_file, new_width, new_height):
    img = Image.open(input_file)
    resized_img = img.resize((new_width, new_height), Image.ANTIALIAS)
    resized_img.save(output_file)

def extract_from_artifacts(response_data, image_name):
    # Assuming you have already obtained the response_data from the API call
    artifacts = response_data["artifacts"]

    # Extract the base64-encoded image from the first artifact
    base64_image_data = artifacts[0]["base64"]

    # Decode the base64 data and save it as an image file
    with open(image_name, "wb") as f:
        f.write(base64.b64decode(base64_image_data))


def get_image_diffusion(api_key, prompt_anchor, prompt, width, height):

    prompt_positive = prompt_anchor.positive + ', (Title: ' + prompt + ')'
    print('requesting image with positive prompt: ' + prompt_positive)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    url = "https://api.stability.ai/v1/generation/stable-diffusion-512-v2-1/text-to-image"

    data = {
    "text_prompts": [
        {
            "text": prompt_positive,
            "weight": 0.5,
        },
        {
            "text": prompt_anchor.negative,
            "weight": -.5
        }
        ],
        "height": height,
        "width": width,
        "cfg_scale": 7,
        "clip_guidance_preset": "NONE",
        "samples": 1,
        "seed": 0,
        "steps": 50,
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_data = response.json()
        print('200 code received: ' + response_data['artifacts'][0]['finishReason'])
        return response_data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


    #return extract_from_artifacts(response_data=response_data, savepath=savepath, postid=postid)

#must create image larger becuase api doesn't want to create small images, must be a multiple of 64
def generate_images(post, api_key, savepath_small, savepath_large):
    gen_width = 896
    gen_height = 512

    #ensure the same anchor is picked for all images for the same post
    #selected_anchor = anchors[post.id % len(anchors)]

    selected_anchor = random.choice(anchors)

    response_data = get_image_diffusion(api_key=api_key, prompt_anchor=selected_anchor, prompt=post.title,
                                 width=gen_width, height=gen_height)

    #create large image
    large_image_name =  f'{savepath_large}{post.id}.jpg'
    extract_from_artifacts(response_data, large_image_name)
    print(f"Large image saved as {large_image_name}.png")

    #resize from 896/512 -> 448/256    
    small_image_name = f'{savepath_small}{post.id}.jpg'
    resize_image(input_file=large_image_name, output_file=small_image_name, new_width=448, new_height=256)
    print(f"Small image saved as {small_image_name}.png")

    #crop small image to 416x256
    crop_image_width(input_file=small_image_name, output_file=small_image_name, new_width=416)