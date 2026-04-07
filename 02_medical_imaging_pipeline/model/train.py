import json
import torch
from torch import nn, optim
from torchvision import models
from sklearn.metrics import accuracy_score, roc_auc_score
from config import ARTIFACTS_DIR, NUM_CLASSES, EPOCHS, LR, DEVICE, MODEL_NAME
from preprocessing.dataset import build_dataloaders

def build_model(num_classes: int):
    if MODEL_NAME == "resnet18":
        model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        return model
    raise ValueError(f"Unsupported MODEL_NAME={MODEL_NAME}")

def run_epoch(model, loader, criterion, optimizer=None, device="cpu"):
    is_train = optimizer is not None
    model.train() if is_train else model.eval()

    total_loss = 0.0
    all_probs, all_preds, all_labels = [], [], []

    with torch.set_grad_enabled(is_train):
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            logits = model(images)
            loss = criterion(logits, labels)

            if is_train:
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            probs = torch.softmax(logits, dim=1)[:, 1].detach().cpu().numpy()
            preds = torch.argmax(logits, dim=1).detach().cpu().numpy()
            labs = labels.detach().cpu().numpy()

            total_loss += loss.item() * images.size(0)
            all_probs.extend(probs.tolist())
            all_preds.extend(preds.tolist())
            all_labels.extend(labs.tolist())

    avg_loss = total_loss / len(loader.dataset)
    acc = accuracy_score(all_labels, all_preds)
    auc = roc_auc_score(all_labels, all_probs) if len(set(all_labels)) > 1 else None
    return {"loss": avg_loss, "accuracy": acc, "roc_auc": auc}

def main():
    device = "cuda" if torch.cuda.is_available() and DEVICE == "cuda" else "cpu"
    train_loader, val_loader, test_loader, classes = build_dataloaders()

    model = build_model(NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)

    history = []
    best_val_auc = -1.0

    for epoch in range(1, EPOCHS + 1):
        train_metrics = run_epoch(model, train_loader, criterion, optimizer, device=device)
        val_metrics = run_epoch(model, val_loader, criterion, optimizer=None, device=device)

        row = {"epoch": epoch, "train": train_metrics, "val": val_metrics}
        history.append(row)
        print(row)

        val_auc = val_metrics["roc_auc"] or 0.0
        if val_auc > best_val_auc:
            best_val_auc = val_auc
            torch.save({
                "model_state_dict": model.state_dict(),
                "classes": classes,
                "model_name": MODEL_NAME,
            }, ARTIFACTS_DIR / "best_model.pt")

    with open(ARTIFACTS_DIR / "history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    test_metrics = run_epoch(model, test_loader, criterion, optimizer=None, device=device)
    with open(ARTIFACTS_DIR / "test_metrics.json", "w", encoding="utf-8") as f:
        json.dump(test_metrics, f, indent=2)

    print("Saved model + metrics to artifacts/")

if __name__ == "__main__":
    main()
