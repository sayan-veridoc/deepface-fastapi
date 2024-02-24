import tempfile
import cv2 
from deepface import DeepFace 
from urllib.parse import quote
from fastapi import FastAPI, File, HTTPException, UploadFile


app = FastAPI(title="Emotion Api")


@app.get("/api/health")
async def hello_world():
    return {"status": "success", "message": "Integrate FastAPI Framework with Next.js"}

ALLOWED_FILE_TYPES = ["image/jpeg", "image/png"]

@app.post("/api/emotion")
async def emotion(file: UploadFile = File(...)):
    try:
            if file.content_type not in ALLOWED_FILE_TYPES:
                raise HTTPException(status_code=400, detail="Only JPEG and PNG images are allowed")

            # Read the image file
            img_temp = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
            img_temp.write(await file.read())
            img_temp.close()

            # Load the image using OpenCV
            img = cv2.imread(img_temp.name)

            # Analyze emotions using DeepFace
            result = DeepFace.analyze(img, actions=['emotion'])

            # Remove temporary file
            img_temp.unlink()

            print(result)

    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while processing the image")
        
