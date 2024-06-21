import cv2
from deepface import DeepFace
from fastapi import FastAPI, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
import numpy as np
from pydantic import BaseModel


app = FastAPI(title="Emotion Api")


class HealthCheck(BaseModel):
    """Response model to validate and return when performing a health check."""

    status: str = "OK"


@app.get(
    "health",
    tags=["healthcheck"],
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    """
    ## Perform a Health Check
    Endpoint to perform a healthcheck on. This endpoint can primarily be used Docker
    to ensure a robust container orchestration and management is in place. Other
    services which rely on proper functioning of the API service will not deploy if this
    endpoint returns any other HTTP status code except 200 (OK).
    Returns:
        HealthCheck: Returns a JSON response with the health status
    """
    return HealthCheck(status="OK")


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
            status_code=status.HTTP_200_OK,
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="An error occurred while processing the image"
        )
