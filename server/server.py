"""
Server API

Generate image in Cloud
"""
# Import dependencies
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from torch import autocast
from diffusers import StableDiffusionPipeline
from PIL import Image
from pydantic import BaseModel
import cloudinary
from cloudinary import CloudinaryImage
import cloudinary.uploader
import cloudinary.api
# App
server = FastAPI()

cloudinary.config( 
  cloud_name = "dr4luonmq", 
  api_key = "783617815293663", 
  api_secret = "iRHTK7KUGuAaXxOPNu9mw-btSDY" 
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

# TODO: Add host domain
server.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@server.post("/generate")
async def generate_image(payload : GenerateImage):
    # Serialize payload
    id = payload.id
    prompt = payload.prompt
    # Generate image
    with autocast("cuda"):
        image = pipe(prompt)["sample"][0]  
    file_path = os.path.join(os.getcwd(), f"files/{id}.png")
    image.save(file_path)
    # Send image to CDN
    image_cdn_url = submit_image(file_path, str(id))
    return image_cdn_url