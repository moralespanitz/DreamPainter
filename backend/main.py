import io
import os
import qrcode
from captcha.image import ImageCaptcha
import googletrans
from fastapi import FastAPI, Response, Request, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
from pydantic import BaseModel

"""
Global variables
"""
# Counter

_counter = 1001
URL = "localhost:8000"
# Google Translate
translator = googletrans.Translator()

# Spanish to English
def _spanish_to_english(sentence : str) -> str:
    obj = translator.translate(sentence, dest='en')
    return obj.text

def increase():
    global _counter 
    _counter += 1
    return _counter

# General app
app =  FastAPI()
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
    return {"message": "dream painter"}

class SentenceBody(BaseModel):
    sentence: str 

# TODO: remove
img = Image.open("images/1001.png")

@app.post("/generate")
async def generate_image(sentence : SentenceBody):
    # Translate from spanish to english
    en_sentence = _spanish_to_english(sentence.sentence)
    # Get image id
    img_id = increase()
    # Save to image folders
    global img
    path = f"images/{img_id}.png"
    img.save(path)
    # file_path = os.path.join(os.getcwd(), path)
    # if os.path.exists(file_path):
        # return FileResponse(file_path, media_type='image/png')
    return {"id": img_id}

@app.get("/image/{id}")
async def get_image(id : int):
    try:
        file_path = os.path.join(os.getcwd(), f"images/{id}.png")
        if os.path.exists(file_path):
            img = Image.open(f"images/{id}.png")
            return FileResponse(file_path, media_type='image/png')
    except:
        return {"message": "File nout found"}

@app.get("/qr/{id}")
def get_qr(id: int):
    file_path = os.path.join(os.getcwd(), f"images/{id}.png")
    if os.path.exists(file_path):
        image_url = f"{URL}/image/{id}"
        qr = qrcode.make(image_url)
        path = f"./qrs/{id}.png"
        stream = io.BytesIO()
        qr.save(path)
        return FileResponse(path)
    return {"message": "Image generated not exists"}

"""
Captcha
Reference: https://codereview.stackexchange.com/questions/269428/fastapi-session-captcha
"""
# TODO: To test
import random
import string
import base64
import uuid
def captcha_generator(size: int):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))

def generate_captcha():
    captcha: str = captcha_generator(5)
    image = ImageCaptcha()
    data = image.generate(captcha)
    data = base64.b64encode(data.getvalue())
    return {"data": data, "captcha": captcha}

@app.get('/start-session')
def start_session(request: Request):
    captcha = generate_captcha()
    request.session["captcha"] = captcha['captcha']
    captcha_image = captcha["data"].decode("utf-8")
    return StreamingResponse(io.BytesIO(base64.b64decode(captcha_image)), media_type="image/png")

# TODO: Change to middleware
@app.post('/verify-captcha')
def captcha(
     request: Request
    ,response: Response
    ,data # This includes the captcha answer provided by user
):

   if request.session.get("captcha", uuid.uuid4()) == data.captcha:
       return status.HTTP_200_OK
   else:
      request.session["captcha"] = str(uuid.uuid4())
      raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Captcha Does not Match")