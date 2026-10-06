from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

import cv2
import numpy as np
import base64

from parking_model import analyze_parking
from parking_slots import parking_slots


app = FastAPI(
    title="Smart Parking Management API",
    description="Parking occupancy detection using ResNet50",
    version="1.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():

    return {
        "message": "Smart Parking API is running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Read uploaded image
    contents = await file.read()

    np_array = np.frombuffer(
        contents,
        np.uint8
    )

    image = cv2.imdecode(
        np_array,
        cv2.IMREAD_COLOR
    )

    if image is None:

        return {
            "error": "Invalid image"
        }

    # Analyze parking
    results = analyze_parking(
        image,
        parking_slots
    )

    # Get annotated image
    annotated_image = results.pop("annotated_image")

    # Convert image to JPG
    success, encoded_image = cv2.imencode(
        ".jpg",
        annotated_image
    )

    if not success:

        return {
            "error": "Could not encode image"
        }

    # Convert image to Base64
    image_base64 = base64.b64encode(
        encoded_image
    ).decode("utf-8")

    # Add image to response
    results["annotated_image"] = image_base64

    return results
