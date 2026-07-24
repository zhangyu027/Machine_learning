"""Production-oriented CNN training entry point.

Uses torchvision ImageFolder layout:
  data/images/train/normal, data/images/train/abnormal
  data/images/val/normal,   data/images/val/abnormal
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from src.models import TransferLearningCNN
from src.train_eval import evaluate_image_model, train_image_model


def build_loaders(data_dir: Path, image_size: int, batch_size: int):
    train_tf = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((image_size, image_size)),
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(7),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ])
    eval_tf = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((image_size, image_size)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ])
    train_ds = datasets.ImageFolder(data_dir / "train", transform=train_tf)
    val_ds = datasets.ImageFolder(data_dir / "val", transform=eval_tf)
    return (
        DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0),
        DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=0),
        train_ds.classes,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, default=Path("data/images"))
    parser.add_argument("--architecture", choices=["resnet50", "efficientnet_b0"], default="resnet50")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--pretrained", action="store_true")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    train_loader, val_loader, classes = build_loaders(args.data_dir, args.image_size, args.batch_size)
    model = TransferLearningCNN(args.architecture, len(classes), 1, args.pretrained)
    history = train_image_model(model, train_loader, epochs=args.epochs, device=device)
    metrics, y_true, y_pred, y_prob = evaluate_image_model(model, val_loader, device=device)

    checkpoint_dir = Path("models/checkpoints")
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = checkpoint_dir / f"{args.architecture}_medical_imaging.pt"
    torch.save({
        "state_dict": model.state_dict(),
        "architecture": args.architecture,
        "classes": classes,
        "image_size": args.image_size,
        "in_channels": 1,
        "metrics": metrics,
    }, checkpoint_path)
    Path("evaluation/cnn_metrics.json").write_text(json.dumps({"metrics": metrics, "history": history}, indent=2))
    print(f"Saved checkpoint to {checkpoint_path}")


if __name__ == "__main__":
    main()
