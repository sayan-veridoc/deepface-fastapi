import base64
import tempfile
import cv2
from deepface import DeepFace
from urllib.parse import quote
from fastapi import FastAPI, File, HTTPException, Response, UploadFile
from fastapi.responses import JSONResponse
import numpy as np


app = FastAPI(title="Emotion Api")


@app.get("/api/health")
async def hello_world():

    return JSONResponse(
        content={
            "message": "Emotion Api is running !!!",
        },
        status_code=200,
    )


ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"]


@app.post("/api/emotion")
async def emotion(file: UploadFile = File(...)):
    try:
        if file.content_type not in ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=400, detail="Only JPEG and PNG images are allowed"
            )

        img_bytes = await file.read()

        img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), -1)
        # print(img)

        objs = DeepFace.analyze(
            img, actions=["age", "emotion"], enforce_detection=False
        )
        return JSONResponse(
            content={
                "message": "Face Detection successful !",
                "data": objs,
            },
            status_code=200,
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the image"
        )
