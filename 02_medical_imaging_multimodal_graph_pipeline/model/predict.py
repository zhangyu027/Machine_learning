import argparse
import json
from typing import Dict, List, Optional

import torch
from PIL import Image
from torchvision import transforms

from config import ARTIFACTS_DIR, IMAGE_SIZE, DEVICE
from model.multimodal_model import MultiModalGraphClassifier

def load_model():
    device = "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
    checkpoint = torch.load(ARTIFACTS_DIR / "best_model.pt", map_location=device)

    model = MultiModalGraphClassifier(
        num_classes=len(checkpoint["classes"]),
        metadata_dim=checkpoint["metadata_dim"],
        model_type=checkpoint["model_type"],
    ).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()
    return model, checkpoint, device

def preprocess_image(image_path: str):
    tfm = transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])
    image = Image.open(image_path).convert("RGB")
    return tfm(image).unsqueeze(0)

def build_metadata_tensor(metadata_dict: Optional[Dict], metadata_columns: List[str], device: str):
    if not metadata_columns:
        return torch.zeros(1, 0, device=device)

    metadata_dict = metadata_dict or {}
    values = [float(metadata_dict.get(col, 0.0)) for col in metadata_columns]
    return torch.tensor(values, dtype=torch.float32, device=device).unsqueeze(0)

def predict_image(image_path: str, metadata_dict: Optional[Dict] = None) -> Dict:
    model, checkpoint, device = load_model()
    x = preprocess_image(image_path).to(device)
    metadata = build_metadata_tensor(metadata_dict, checkpoint["metadata_columns"], device=device)

    with torch.no_grad():
        logits = model(x, metadata)
        probs = torch.softmax(logits, dim=1).cpu().numpy()[0]
        pred_idx = int(probs.argmax())

    return {
        "model_type": checkpoint["model_type"],
        "predicted_class": checkpoint["classes"][pred_idx],
        "probabilities": {
            cls: float(prob) for cls, prob in zip(checkpoint["classes"], probs)
        },
        "metadata_used": {col: float((metadata_dict or {}).get(col, 0.0)) for col in checkpoint["metadata_columns"]},
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", required=True, help="Path to image")
    parser.add_argument("--metadata_json", default=None, help="JSON string for metadata")
    args = parser.parse_args()

    metadata = json.loads(args.metadata_json) if args.metadata_json else None
    print(json.dumps(predict_image(args.image, metadata), indent=2))
