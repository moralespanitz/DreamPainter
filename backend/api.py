"""
API of DreamPainter
"""
# Import dependencies
from multiprocessing import Lock
import qrcode
import os
import torch
import googletrans
from diffusers import StableDiffusionPipeline
from fast_captcha import img_captcha, text_captcha
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from torch import autocast
from PIL import Image
from postprocessing import PostProcessing
access_token = os.getenv("DIFUSSION_MODEL_ACCESS_TOKEN")
device = "cpu"
lock = Lock()
if torch.cuda.is_enabled():
    device = "gpu"
pipe = StableDiffusionPipeline.from_pretrained(
	"CompVis/stable-diffusion-v1-4", 
	use_auth_token=access_token,
).to(device)

"""Global variables"""
translator = googletrans.Translator()

postprocess = PostProcessing()
# Set general app
app = FastAPI()

counter = 10000
def _increase():
    counter += 1
    return counter

def _spanish_to_english(sentence : str) -> str:
    obj = translator.translate(sentence, dest='en')
    return obj.text

"""APIs"""
@app.get("/")
def read_root():
    return {"Open": "Day"}

@app.get("/generate/{sentence}")
def generate_image(sentence: str, summary='difussion', name='difussion'):
    try:
        en_sentence = _spanish_to_english(sentence)
        with autocast("cuda"):
            img = pipe(en_sentence)["sample"][0]  
        lock.acquire()
        request_id = _increase()
        lock.release()
        img.save(f"{request_id}.png")
        return StreamingResponse(content=img, media_type='image/png')
    except:
        return "Bad request"
    

@app.get("/qr/{id}", summary='image', name='qr')
def get_qr(id):
    try:
        URL = os.getenv("DOMAIN")
        QR = f"{URL}/images/{id}"
        img = qrcode.make(QR)
        return StreamingResponse(content=img, media_type='image/svg')
    except:
        return {"message": "Not image generated"}

@app.get("/images/{id}")
def get_image(id : int):
    path = f"images/{id}.png"
    try:
        img = Image.open(path)
        processed_img = postprocess.get_image(img)
        return StreamingResponse(content=processed_img, media_type='image/png')
    except:
        return {"message": "Not found image"}

@app.get("/captcha", summary='captcha', name='captcha')
def get_captcha():
    img, text = img_captcha()
    print(text)
    return StreamingResponse(content=img, media_type='image/jpeg')

@app.post("/captcha")
def validate_captcha():
    # parsing original and input text
    # compare if they are same
    # if not is same -> return to captcha
    # else -> save in session httpOnly
    return {"Validate": "Captcha"}

@app.get("/images/{id}")
def get_qr(id: int):
    return {"id" : id}
