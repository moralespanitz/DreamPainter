"""
Server API

Generate image in Cloud
"""
from fastapi import FastAPI

server = FastAPI()

@server.post("/generate")
async def generate_image(prompt : str):
    ...

@server.get("/files/{id}")
async def get_image(id : int):
    ...
