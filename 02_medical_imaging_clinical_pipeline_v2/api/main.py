"""FastAPI inference service for uploaded medical images."""
from __future__ import annotations

import io
import time
from pathlib import Path

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image
from torchvision import transforms

from src.models import TransferLearningCNN

app = FastAPI(title="Medical Imaging Clinical AI API", version="2.0.0")
CHECKPOINT = Path("models/checkpoints/resnet50_medical_imaging.pt")
_model = None
_metadata = None


def load_model():
    global _model, _metadata
    if _model is not None:
        return _model, _metadata
    if not CHECKPOINT.exists():
        raise FileNotFoundError(f"Checkpoint not found: {CHECKPOINT}")
    checkpoint = torch.load(CHECKPOINT, map_location="cpu")
    model = TransferLearningCNN(
        architecture=checkpoint.get("architecture", "resnet50"),
        num_classes=len(checkpoint.get("classes", ["normal", "abnormal"])),
        in_channels=checkpoint.get("in_channels", 1),
        pretrained=False,
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    _model, _metadata = model, checkpoint
    return _model, _metadata


@app.get("/health")
def health():
    return {"status": "ok", "checkpoint_available": CHECKPOINT.exists()}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg"}:
        raise HTTPException(415, "Upload a PNG or JPEG image.")
    started = time.perf_counter()
    try:
        image = Image.open(io.BytesIO(await file.read())).convert("L")
        model, metadata = load_model()
    except FileNotFoundError as exc:
        raise HTTPException(503, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(400, f"Invalid image or model: {exc}") from exc

    size = int(metadata.get("image_size", 224))
    tensor = transforms.Compose([
        transforms.Resize((size, size)), transforms.ToTensor(), transforms.Normalize([0.5], [0.5])
    ])(image).unsqueeze(0)
    with torch.no_grad():
        probabilities = torch.softmax(model(tensor), dim=1)[0]
    index = int(probabilities.argmax())
    classes = metadata.get("classes", ["normal", "abnormal"])
    return {
        "predicted_class": classes[index],
        "confidence": float(probabilities[index]),
        "class_probabilities": {name: float(probabilities[i]) for i, name in enumerate(classes)},
        "latency_ms": round((time.perf_counter() - started) * 1000, 2),
        "clinical_disclaimer": "Research/portfolio output only; not for diagnosis or patient care.",
    }
