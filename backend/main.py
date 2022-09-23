import io
import os
import qrcode
# pip install googletrans==3.1.0a0
import googletrans
from fastapi import FastAPI, Response, Request, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
# from threading import Lock
import replicate
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

"""
Global variables
"""
# Counter
_counter = 1000
URL = "localhost:8000"
# Google Translate
translator = googletrans.Translator()

# Spanish to English


def _spanish_to_english(sentence: str) -> str:
    obj = translator.translate(sentence, dest='en')
    return obj.text


def increase():
    global _counter
    _counter += 1
    return _counter


# General app
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"API": "DreamPainter"}


class SentenceBody(BaseModel):
    sentence: str


model = replicate.models.get("stability-ai/stable-diffusion")

@app.post("/generate")
async def generate_image(sentence: SentenceBody):
    # Translate from spanish to english
    en_sentence = _spanish_to_english(sentence.sentence)
    img_id = increase()
    global model
    image_url = model.predict(prompt=en_sentence)
    qr = qrcode.make(image_url)
    path = f"./qrs/{img_id}.png"
    stream = io.BytesIO()
    qr.save(path)
    return {
        "id": img_id,
        "url": image_url
    }

@app.get("/image/{id}")
async def get_image(id: int):
    try:
        file_path = os.path.join(os.getcwd(), f"images/{id}.png")
        if os.path.exists(file_path):
            img = Image.open(f"images/{id}.png")
            return FileResponse(file_path, media_type='image/png')
    except:
        return {"message": "File nout found"}


@app.get("/qr/{id}")
def get_qr(id : int):
    file_path = os.path.join(os.getcwd(), f"qrs/{id}.png")
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"message": "Image generated not exists"}
