"""FastAPI inference service for the trained medical-imaging classifier."""

from __future__ import annotations

import io
import time
from pathlib import Path
from typing import Any

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError
from torch import nn
from torchvision import models, transforms


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CHECKPOINT = (
    ROOT
    / "models"
    / "checkpoints"
    / "efficientnet_b0"
    / "best_model.pt"
)

app = FastAPI(
    title="Medical Imaging Clinical AI API",
    description=(
        "Research and portfolio demonstration API for binary chest X-ray "
        "classification. Not for diagnosis or patient care."
    ),
    version="3.0.0",
)

_model: nn.Module | None = None
_metadata: dict[str, Any] | None = None
_device: torch.device | None = None


def select_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")
    if hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def build_model(
    architecture: str,
    num_classes: int,
) -> nn.Module:
    if architecture == "resnet18":
        model = models.resnet18(weights=None)
        model.fc = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(model.fc.in_features, num_classes),
        )
    elif architecture == "resnet50":
        model = models.resnet50(weights=None)
        model.fc = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(model.fc.in_features, num_classes),
        )
    elif architecture == "efficientnet_b0":
        model = models.efficientnet_b0(weights=None)
        model.classifier = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(model.classifier[1].in_features, num_classes),
        )
    elif architecture == "efficientnet_v2_s":
        model = models.efficientnet_v2_s(weights=None)
        model.classifier = nn.Sequential(
            nn.Dropout(0.30),
            nn.Linear(model.classifier[1].in_features, num_classes),
        )
    else:
        raise ValueError(f"Unsupported architecture: {architecture}")

    return model


def load_model() -> tuple[nn.Module, dict[str, Any], torch.device]:
    global _model, _metadata, _device

    if _model is not None and _metadata is not None and _device is not None:
        return _model, _metadata, _device

    if not DEFAULT_CHECKPOINT.is_file():
        raise FileNotFoundError(
            f"Checkpoint not found: {DEFAULT_CHECKPOINT}"
        )

    device = select_device()
    checkpoint = torch.load(DEFAULT_CHECKPOINT, map_location=device)

    architecture = str(
        checkpoint.get("architecture", "efficientnet_b0")
    )
    class_names = checkpoint.get(
        "class_names",
        checkpoint.get("classes", ["NORMAL", "PNEUMONIA"]),
    )
    image_size = int(checkpoint.get("image_size", 224))

    if not isinstance(class_names, list) or len(class_names) != 2:
        raise ValueError(
            "Checkpoint must contain exactly two class names."
        )

    model = build_model(
        architecture=architecture,
        num_classes=len(class_names),
    )
    model.load_state_dict(checkpoint["state_dict"])
    model.to(device)
    model.eval()

    metadata = {
        **checkpoint,
        "architecture": architecture,
        "class_names": class_names,
        "image_size": image_size,
        "checkpoint_path": str(DEFAULT_CHECKPOINT),
    }

    _model = model
    _metadata = metadata
    _device = device
    return model, metadata, device


def build_inference_transform(image_size: int):
    return transforms.Compose(
        [
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "Medical Imaging Clinical AI API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, Any]:
    response: dict[str, Any] = {
        "status": "ok",
        "checkpoint_available": DEFAULT_CHECKPOINT.is_file(),
        "checkpoint_path": str(DEFAULT_CHECKPOINT),
    }

    if DEFAULT_CHECKPOINT.is_file():
        try:
            _, metadata, device = load_model()
            response.update(
                {
                    "model_loaded": True,
                    "architecture": metadata["architecture"],
                    "class_names": metadata["class_names"],
                    "image_size": metadata["image_size"],
                    "device": str(device),
                }
            )
        except Exception as exc:
            response.update(
                {
                    "status": "degraded",
                    "model_loaded": False,
                    "model_error": str(exc),
                }
            )
    else:
        response["model_loaded"] = False

    return response


@app.post("/predict")
async def predict(file: UploadFile = File(...)) -> dict[str, Any]:
    allowed_content_types = {
        "image/png",
        "image/jpeg",
        "image/jpg",
    }

    if file.content_type not in allowed_content_types:
        raise HTTPException(
            status_code=415,
            detail="Upload a PNG or JPEG image.",
        )

    started = time.perf_counter()

    try:
        payload = await file.read()
        if not payload:
            raise ValueError("The uploaded file is empty.")

        image = Image.open(io.BytesIO(payload)).convert("RGB")
        model, metadata, device = load_model()

        transform = build_inference_transform(
            int(metadata["image_size"])
        )
        tensor = transform(image).unsqueeze(0).to(device)

        with torch.inference_mode():
            logits = model(tensor)
            probabilities = torch.softmax(logits, dim=1)[0]

        probabilities_cpu = probabilities.detach().cpu()
        predicted_index = int(probabilities_cpu.argmax().item())
        class_names = list(metadata["class_names"])

        return {
            "predicted_class": class_names[predicted_index],
            "predicted_index": predicted_index,
            "confidence": float(
                probabilities_cpu[predicted_index].item()
            ),
            "class_probabilities": {
                class_name: float(probabilities_cpu[index].item())
                for index, class_name in enumerate(class_names)
            },
            "architecture": metadata["architecture"],
            "image_size": metadata["image_size"],
            "device": str(device),
            "latency_ms": round(
                (time.perf_counter() - started) * 1000,
                2,
            ),
            "clinical_disclaimer": (
                "Research and portfolio output only; "
                "not for diagnosis or patient care."
            ),
        }

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc
    except UnidentifiedImageError as exc:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Inference failed: {exc}",
        ) from exc
