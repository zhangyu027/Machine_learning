from pathlib import Path
import tempfile
from fastapi import FastAPI, UploadFile, File
from model.predict import predict_image

app = FastAPI(title="Medical Imaging Diagnosis API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix or ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    result = predict_image(tmp_path)
    return result
