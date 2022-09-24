"""
Server API
Generate image in Cloud
"""
# Import dependencies
import os

import cloudinary
import cloudinary.api
import cloudinary.uploader
from cloudinary import CloudinaryImage
from diffusers import StableDiffusionPipeline
from flask import Flask, request
from PIL import Image
from pydantic import BaseModel
from torch import autocast
import qrcode
import googletrans

# App
app = Flask(__name__)
translator = googletrans.Translator()
cloudinary.config( 
  cloud_name = "dr4luonmq", 
  api_key = "783617815293663", 
  api_secret = "iRHTK7KUGuAaXxOPNu9mw-btSDY" 
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

def _spanish_to_english(sentence: str) -> str:
    """
    Spanish to English model
    """
    obj = translator.translate(sentence, dest='en')
    return obj.text

def increase():
    """
    Incease image ID by generation
    """
    global _counter
    _counter += 1
    return _counter
def make_qr(image_url, img_id):
    qr = qrcode.make(image_url)
    path= f"./qrs/{img_id}.png"
    qr.save(path)
    return submit_image(path, img_id)

# Model
pipe = StableDiffusionPipeline.from_pretrained(
	"CompVis/stable-diffusion-v1-4", 
	use_auth_token=True
).to("cuda")

class GenerateImage(BaseModel):
    prompt : str
    id : int

def submit_image(file_path : str, id):
    img_code = str(id)
    cloudinary.uploader.upload(file_path, public_id=img_code, unique_filename = False, overwrite=True)
    srcURL = cloudinary.CloudinaryImage(img_code).build_url()
    return srcURL

@app.post("/generate")
def generate_image():
    # Serialize payload
    payload = request.get_json()
    id = increase()
    prompt = payload.get('prompt')
    en_prompt = _spanish_to_english(prompt)
    # Generate image
    with autocast("cuda"):
        image = pipe(en_prompt)["sample"][0]  
    file_path = os.path.join(os.getcwd(), f"files/{id}.png")
    image.save(file_path)
    # Send image to CDN
    image_cdn_url = submit_image(file_path, str(id))
    qr_url = make_qr(image_cdn_url, id)
    return {
        "image_cdn_url": image_cdn_url,
        "qr_cdn_url": qr_url,
        "prompt": prompt
    }

if __name__ == "__main__":
    app.run(port=8080, debug=True)