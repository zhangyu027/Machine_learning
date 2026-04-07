from __future__ import annotations

import json
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile
from PIL import Image

from model.predict import Predictor

app = FastAPI(title="Medical Imaging Clinical AI API")
predictor = Predictor()

@app.get("/")
def healthcheck():
    return {
        "status": "ok",
        "message": "Medical Imaging Clinical AI API is running.",
        "predict_endpoint": "/predict",
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...), metadata_json: Optional[str] = Form(default=None)):
    image = Image.open(file.file).convert("RGB")
    metadata = json.loads(metadata_json) if metadata_json else None
    result = predictor.predict(image=image, metadata=metadata)
    return result
