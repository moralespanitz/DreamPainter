"""
DreamPainter API
"""
import os
import qrcode
import http.client
import json
import googletrans
import requests
from fastapi import FastAPI, Response, Request, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

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


dreampainter = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

dreampainter.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@dreampainter.get("/")
async def root():
    return {"API": "DreamPainter"}


class SentenceBody(BaseModel):
    sentence: str


# model = replicate.models.get("stability-ai/stable-diffusion")

@dreampainter.post("/generate")
async def generate_image(sentence: SentenceBody):
    # Original text
    prompt = sentence.sentence
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

@dreampainter.get("/qrs/{id}")
def get_qr(id : int):
    file_path = os.path.join(os.getcwd(), f"qrs/{id}.png")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"message": "Image generated not exists"}, 404
