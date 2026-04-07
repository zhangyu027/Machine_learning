import json

import matplotlib.pyplot as plt
import torch
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

from config import ARTIFACTS_DIR, DEVICE
from model.multimodal_model import MultiModalGraphClassifier
from preprocessing.dataset import build_dataloaders

def main():
    device = "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
    _, _, test_loader, info = build_dataloaders()

    checkpoint = torch.load(ARTIFACTS_DIR / "best_model.pt", map_location=device)
    model = MultiModalGraphClassifier(
        num_classes=len(checkpoint["classes"]),
        metadata_dim=checkpoint["metadata_dim"],
        model_type=checkpoint["model_type"],
    ).to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    y_true, y_pred = [], []
    with torch.no_grad():
        for images, labels, metadata, _ in test_loader:
            images = images.to(device)
            labels = labels.to(device)
            metadata = metadata.to(device)

            logits = model(images, metadata)
            preds = torch.argmax(logits, dim=1).cpu().numpy()

            y_pred.extend(preds.tolist())
            y_true.extend(labels.cpu().numpy().tolist())

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=checkpoint["classes"])
    fig, ax = plt.subplots(figsize=(6, 6))
    disp.plot(ax=ax)
    fig.savefig(ARTIFACTS_DIR / "confusion_matrix.png", bbox_inches="tight")

    with open(ARTIFACTS_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(checkpoint["classes"], f, indent=2)

    print("Saved confusion matrix and classes metadata.")

if __name__ == "__main__":
    main()
