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
    if os.path.exists(file_path):
        CloudinaryImage(file_path, public_id=id).image(width=70, height=53, crop="scale")
        image_cdn_url = cloudinary.CloudinaryImage(id).build_url()
        return image_cdn_url
    return "Cdn not found"

@server.post("/generate")
async def generate_image(payload : GenerateImage):
    id = payload.id
    prompt = payload.prompt
    with autocast("cuda"):
        image = pipe(prompt)["sample"][0]  
    file_path = os.path.join(os.getcwd(), f"files/{id}.png")
    image.save(file_path)
    # Send image to CDN
    image_cdn_url = submit_image(file_path, id)
    return image_cdn_url