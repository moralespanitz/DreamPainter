"""
DreamPainter API
"""
import os
import qrcode
import http.client
import json
import googletrans
import requests
from PIL import Image
from pydantic import BaseModel
from flask import Flask, request
import cloudinary
import cloudinary.uploader
import cloudinary.api
# App
app = Flask(__name__)

cloudinary.config( 
  cloud_name = "dr4luonmq", 
  api_key = "783617815293663", 
  api_secret = "iRHTK7KUGuAaXxOPNu9mw-btSDY" 
)

"""
Global variables
"""
# Counter
_counter = 1000

URL = "http://localhost:8000"
SERVER_URL = "http://localhost:8080"
headers = {'Content-type': 'application/json'}

translator = googletrans.Translator()
conn = http.client.HTTPSConnection(SERVER_URL)

def submit_image(file_path : str, id):
    img_code = str(id)
    cloudinary.uploader.upload(file_path, public_id=img_code, unique_filename = False, overwrite=True)
    srcURL = cloudinary.CloudinaryImage(img_code).build_url()
    return srcURL

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


origins = [
    "http://localhost",
    "http://localhost:3000",
]

@app.get("/")
async def root():
    return {"API": "DreamPainter"}

@app.post("/generate")
async def generate_image():
    # Original text
    data = request.get_json()
    prompt = data.get('prompt')
    # Translated text
    en_sentence = _spanish_to_english(prompt)
    # Image id
    img_id = increase()
    # Serializer
    json_en_sentence = {'prompt': en_sentence, 'id': img_id}

    # POST prompt and id to server
    response = requests.post(f"{SERVER_URL}/generate", json=json_en_sentence)

    # Get image_url
    image_url = response.text.replace("\"", "") 

    # Generate url qr
    qr = qrcode.make(image_url)
    qr.save(f"./qrs/{img_id}.png")
    qr_uri = f"{URL}/qrs/{img_id}"
    return {
        "image_url": image_url,
        "qr_uri": qr_uri,
        "texto": prompt
    }

@app.get("/qrs/{id}")
def get_qr(id : int):
    file_path = os.path.join(os.getcwd(), f"qrs/{id}.png")
    image_cdn_url = submit_image(file_path, f"qr_{str(id)}")
    return image_cdn_url