import json
import tempfile
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, File, Form, UploadFile

from model.predict import predict_image

app = FastAPI(title="Medical Imaging Multimodal Diagnosis API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    metadata_json: Optional[str] = Form(default=None),
):
    suffix = Path(file.filename).suffix or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    metadata = json.loads(metadata_json) if metadata_json else None
    result = predict_image(tmp_path, metadata)
    return result
