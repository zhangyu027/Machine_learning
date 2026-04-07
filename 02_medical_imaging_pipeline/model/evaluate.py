import json
import matplotlib.pyplot as plt
import torch
from torch import nn
from torchvision import models
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from config import ARTIFACTS_DIR, NUM_CLASSES, DEVICE
from preprocessing.dataset import build_dataloaders

def build_model():
    model = models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)
    return model

def main():
    device = "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
    _, _, test_loader, classes = build_dataloaders()

    checkpoint = torch.load(ARTIFACTS_DIR / "best_model.pt", map_location=device)
    model = build_model().to(device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    y_true, y_pred = [], []
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            logits = model(images)
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            y_pred.extend(preds.tolist())
            y_true.extend(labels.numpy().tolist())

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
    fig, ax = plt.subplots(figsize=(6, 6))
    disp.plot(ax=ax)
    fig.savefig(ARTIFACTS_DIR / "confusion_matrix.png", bbox_inches="tight")

    with open(ARTIFACTS_DIR / "classes.json", "w", encoding="utf-8") as f:
        json.dump(classes, f)

    print("Saved confusion matrix and classes metadata.")

if __name__ == "__main__":
    main()
