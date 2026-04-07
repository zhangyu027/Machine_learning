from typing import Dict
import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image
from config import ARTIFACTS_DIR, IMAGE_SIZE, NUM_CLASSES, DEVICE

def build_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model

def load_model():
    device = "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
    checkpoint = torch.load(ARTIFACTS_DIR / "best_model.pt", map_location=device)
    model = build_model().to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    classes = checkpoint["classes"]
    return model, classes, device

def preprocess(image_path: str):
    tfm = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    return tfm(image).unsqueeze(0)

def predict_image(image_path: str) -> Dict:
    model, classes, device = load_model()
    x = preprocess(image_path).to(device)
    with torch.no_grad():
        logits = model(x)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
        pred_idx = int(probs.argmax())
    return {
        "predicted_class": classes[pred_idx],
        "probabilities": {cls: float(prob) for cls, prob in zip(classes, probs)},
    }
