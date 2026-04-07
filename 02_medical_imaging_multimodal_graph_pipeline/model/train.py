import json
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, roc_auc_score
from torch import nn, optim

from config import ARTIFACTS_DIR, DEVICE, EPOCHS, LR, MODEL_TYPE, WEIGHT_DECAY
from model.multimodal_model import MultiModalGraphClassifier
from preprocessing.dataset import build_dataloaders

def compute_auc(y_true, probs):
    try:
        probs = np.asarray(probs)
        y_true = np.asarray(y_true)
        if probs.ndim == 1:
            return float(roc_auc_score(y_true, probs))
        if probs.shape[1] == 2:
            return float(roc_auc_score(y_true, probs[:, 1]))
        return float(roc_auc_score(y_true, probs, multi_class="ovr"))
    except Exception:
        return None

def run_epoch(model, loader, criterion, optimizer=None, device="cpu"):
    is_train = optimizer is not None
    model.train() if is_train else model.eval()

    total_loss = 0.0
    all_probs, all_preds, all_labels = [], [], []

    with torch.set_grad_enabled(is_train):
        for images, labels, metadata, _ in loader:
            images = images.to(device)
            labels = labels.to(device)
            metadata = metadata.to(device)

            logits = model(images, metadata)
            loss = criterion(logits, labels)

            if is_train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            probs = torch.softmax(logits, dim=1).detach().cpu().numpy()
            preds = torch.argmax(logits, dim=1).detach().cpu().numpy()
            labs = labels.detach().cpu().numpy()

            total_loss += loss.item() * images.size(0)
            all_probs.extend(probs.tolist())
            all_preds.extend(preds.tolist())
            all_labels.extend(labs.tolist())

    avg_loss = total_loss / max(len(loader.dataset), 1)
    acc = accuracy_score(all_labels, all_preds) if all_labels else 0.0
    auc = compute_auc(all_labels, all_probs) if all_labels else None
    return {"loss": avg_loss, "accuracy": acc, "roc_auc": auc}

def main():
    device = "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
    train_loader, val_loader, test_loader, info = build_dataloaders()

    classes = info["classes"]
    metadata_dim = info["metadata_dim"]

    model = MultiModalGraphClassifier(
        num_classes=len(classes),
        metadata_dim=metadata_dim,
        model_type=MODEL_TYPE,
    ).to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.AdamW(model.parameters(), lr=LR, weight_decay=WEIGHT_DECAY)

    history = []
    best_score = -1.0

    for epoch in range(1, EPOCHS + 1):
        train_metrics = run_epoch(model, train_loader, criterion, optimizer=optimizer, device=device)
        val_metrics = run_epoch(model, val_loader, criterion, optimizer=None, device=device)

        row = {"epoch": epoch, "train": train_metrics, "val": val_metrics}
        history.append(row)
        print(row)

        monitor = val_metrics["roc_auc"] if val_metrics["roc_auc"] is not None else val_metrics["accuracy"]
        if monitor > best_score:
            best_score = monitor
            torch.save({
                "model_state_dict": model.state_dict(),
                "classes": classes,
                "metadata_dim": metadata_dim,
                "metadata_columns": info["metadata_columns"],
                "model_type": MODEL_TYPE,
            }, ARTIFACTS_DIR / "best_model.pt")

    with open(ARTIFACTS_DIR / "history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    test_metrics = run_epoch(model, test_loader, criterion, optimizer=None, device=device)
    with open(ARTIFACTS_DIR / "test_metrics.json", "w", encoding="utf-8") as f:
        json.dump(test_metrics, f, indent=2)

    with open(ARTIFACTS_DIR / "run_summary.json", "w", encoding="utf-8") as f:
        json.dump({
            "model_type": MODEL_TYPE,
            "classes": classes,
            "metadata_dim": metadata_dim,
            "metadata_columns": info["metadata_columns"],
            "dataset_sizes": {
                "train": info["train_size"],
                "val": info["val_size"],
                "test": info["test_size"],
            }
        }, f, indent=2)

    print("Saved model + metrics to artifacts/")

if __name__ == "__main__":
    main()
