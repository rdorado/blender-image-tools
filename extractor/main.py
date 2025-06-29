from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse, Response
from Database import select_asset_by_id

import io

#from io import bytesio

import base64
import cv2

from utils import loadLayoutFromId
from blenderRenderer import render_as_blender

TEMP_FOLDER="E:\\project\\blender\\extractor\\temp\\"

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://localhost:8080",
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
    return {"message": "Hello World"}

@app.get("/image",
    responses = {
        200: {
            "content": {"image/jpeg": {}}
        }
    },
    response_class=Response
)
async def image():
    img = cv2.imread('sword.jpg')
    #return_img = cv2.processImage(img)
    _, encoded_img = cv2.imencode('.jpg', img)
    #return_img = base64.b64encode(encoded_img)

    #image = bytesio()
    #img = img.save(image, format='jpeg', quality=85)
    #image.seek(0)
    
    #return {'encoded_img': return_img}
    return StreamingResponse(io.BytesIO(encoded_img.tobytes()), media_type="image/jpeg")



    
@app.get("/svg",
    responses = {
        200: {
            "content": {"application/svg+xml": {}}
        }
    },
    response_class=Response
)
async def svg(assetid: int = 0):

    asset = loadLayoutFromId(assetid)
    svg = asset.svg()
    print(svg)
    return Response(content=svg, media_type="application/svg+xml")



@app.get("/blender",
    responses = {
        200: {
            "content": {"application/octet-stream": {}}
        }
    },
    response_class=Response
)
async def svg(assetid: int = 0):
    
    asset = loadLayoutFromId(assetid)
    filename = TEMP_FOLDER+'mesh.blend'
    complete = await render_as_blender(asset, filename)
    return FileResponse(filename)