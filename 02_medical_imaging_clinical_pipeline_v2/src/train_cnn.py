"""Train and evaluate a chest X-ray classifier from an ImageFolder dataset.

Expected directory layout:

    data/images/
        train/
            NORMAL/
            PNEUMONIA/
        val/                    # preferred
            NORMAL/
            PNEUMONIA/

If ``val`` is missing or empty, ``test`` is used automatically:

    data/images/test/<class-name>/...

Supported architectures:
    - resnet18
    - resnet50
    - efficientnet_b0
    - efficientnet_v2_s

The script supports CUDA, Apple Silicon MPS, and CPU. It saves the best
checkpoint, training history, evaluation metrics, ROC and confusion-matrix
plots, and optional TensorBoard logs.
"""

from __future__ import annotations

import argparse
import copy
import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import torch
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    RocCurveDisplay,
)
from torch import nn
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader
from torchvision import datasets, models, transforms


SUPPORTED_ARCHITECTURES = (
    "resnet18",
    "resnet50",
    "efficientnet_b0",
    "efficientnet_v2_s",
)


@dataclass
class TrainingConfig:
    data_dir: str
    architecture: str
    epochs: int
    batch_size: int
    image_size: int
    learning_rate: float
    weight_decay: float
    num_workers: int
    patience: int
    scheduler_patience: int
    scheduler_factor: float
    pretrained: bool
    freeze_backbone: bool
    seed: int
    output_dir: str
    tensorboard: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Train a chest X-ray classifier."
    )

    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path("data/images"),
        help="Directory containing train and val/test folders.",
    )
    parser.add_argument(
        "--architecture",
        choices=SUPPORTED_ARCHITECTURES,
        default="resnet18",
    )
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--image-size", type=int, default=224)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--weight-decay", type=float, default=1e-4)
    parser.add_argument("--num-workers", type=int, default=0)
    parser.add_argument(
        "--patience",
        type=int,
        default=4,
        help="Early-stopping patience measured in epochs.",
    )
    parser.add_argument(
        "--scheduler-patience",
        type=int,
        default=2,
        help="ReduceLROnPlateau patience.",
    )
    parser.add_argument(
        "--scheduler-factor",
        type=float,
        default=0.5,
        help="Learning-rate reduction factor.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("models/checkpoints"),
    )
    parser.add_argument(
        "--no-pretrained",
        action="store_true",
        help="Do not use ImageNet pretrained weights.",
    )
    parser.add_argument(
        "--freeze-backbone",
        action="store_true",
        help="Train only the final classifier head.",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--tensorboard",
        action="store_true",
        help="Write TensorBoard logs when tensorboard is installed.",
    )
    parser.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="Resume model and optimizer state from a saved checkpoint.",
    )

    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    if args.epochs < 1:
        raise ValueError("--epochs must be at least 1.")
    if args.batch_size < 1:
        raise ValueError("--batch-size must be at least 1.")
    if args.image_size < 32:
        raise ValueError("--image-size must be at least 32.")
    if args.learning_rate <= 0:
        raise ValueError("--learning-rate must be positive.")
    if args.weight_decay < 0:
        raise ValueError("--weight-decay cannot be negative.")
    if args.patience < 1:
        raise ValueError("--patience must be at least 1.")
    if args.scheduler_patience < 0:
        raise ValueError("--scheduler-patience cannot be negative.")
    if not 0 < args.scheduler_factor < 1:
        raise ValueError("--scheduler-factor must be between 0 and 1.")


def seed_everything(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

    try:
        torch.use_deterministic_algorithms(False)
    except Exception:
        pass


def select_device() -> torch.device:
    if torch.cuda.is_available():
        return torch.device("cuda")

    if (
        hasattr(torch.backends, "mps")
        and torch.backends.mps.is_available()
    ):
        return torch.device("mps")

    return torch.device("cpu")


def choose_validation_dir(data_dir: Path) -> Path:
    val_dir = data_dir / "val"
    test_dir = data_dir / "test"

    if val_dir.is_dir() and any(val_dir.iterdir()):
        return val_dir

    if test_dir.is_dir() and any(test_dir.iterdir()):
        print(
            "Warning: 'val' is missing or empty; "
            "using 'test' as the validation split."
        )
        return test_dir

    raise FileNotFoundError(
        "No validation split found. Expected either:\n"
        f"  {val_dir}\n"
        "or:\n"
        f"  {test_dir}"
    )


def build_transforms(image_size: int):
    train_transform = transforms.Compose(
        [
            transforms.Grayscale(num_output_channels=3),
            transforms.Resize((image_size, image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(5),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225],
            ),
        ]
    )

    evaluation_transform = transforms.Compose(
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

    return train_transform, evaluation_transform


def build_loaders(
    data_dir: Path,
    image_size: int,
    batch_size: int,
    num_workers: int,
    device: torch.device,
) -> tuple[DataLoader, DataLoader, list[str], Path]:
    data_dir = data_dir.expanduser().resolve()
    train_dir = data_dir / "train"
    validation_dir = choose_validation_dir(data_dir)

    if not train_dir.is_dir():
        raise FileNotFoundError(
            f"Training directory not found: {train_dir}\n"
            "Expected data/images/train/<class-name>/..."
        )

    train_transform, evaluation_transform = build_transforms(image_size)

    train_dataset = datasets.ImageFolder(
        train_dir,
        transform=train_transform,
    )
    validation_dataset = datasets.ImageFolder(
        validation_dir,
        transform=evaluation_transform,
    )

    if len(train_dataset) == 0:
        raise ValueError(f"No training images found in {train_dir}.")
    if len(validation_dataset) == 0:
        raise ValueError(
            f"No validation images found in {validation_dir}."
        )
    if train_dataset.classes != validation_dataset.classes:
        raise ValueError(
            "Class folders do not match.\n"
            f"Train classes: {train_dataset.classes}\n"
            f"Validation classes: {validation_dataset.classes}"
        )
    if len(train_dataset.classes) != 2:
        raise ValueError(
            "This script currently expects exactly two classes. "
            f"Found: {train_dataset.classes}"
        )

    pin_memory = device.type == "cuda"
    persistent_workers = num_workers > 0

    train_loader = DataLoader(
        train_dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=pin_memory,
        persistent_workers=persistent_workers,
    )
    validation_loader = DataLoader(
        validation_dataset,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=pin_memory,
        persistent_workers=persistent_workers,
    )

    print(f"Training directory:   {train_dir}")
    print(f"Validation directory: {validation_dir}")
    print(f"Classes:              {train_dataset.classes}")
    print(f"Training images:      {len(train_dataset)}")
    print(f"Validation images:    {len(validation_dataset)}")

    return (
        train_loader,
        validation_loader,
        train_dataset.classes,
        validation_dir,
    )


def build_model(
    architecture: str,
    num_classes: int,
    pretrained: bool,
    freeze_backbone: bool,
) -> nn.Module:
    if architecture == "resnet18":
        weights = (
            models.ResNet18_Weights.DEFAULT
            if pretrained
            else None
        )
        model = models.resnet18(weights=weights)
        input_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(input_features, num_classes),
        )

    elif architecture == "resnet50":
        weights = (
            models.ResNet50_Weights.DEFAULT
            if pretrained
            else None
        )
        model = models.resnet50(weights=weights)
        input_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(input_features, num_classes),
        )

    elif architecture == "efficientnet_b0":
        weights = (
            models.EfficientNet_B0_Weights.DEFAULT
            if pretrained
            else None
        )
        model = models.efficientnet_b0(weights=weights)
        input_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(0.25),
            nn.Linear(input_features, num_classes),
        )

    elif architecture == "efficientnet_v2_s":
        weights = (
            models.EfficientNet_V2_S_Weights.DEFAULT
            if pretrained
            else None
        )
        model = models.efficientnet_v2_s(weights=weights)
        input_features = model.classifier[1].in_features
        model.classifier = nn.Sequential(
            nn.Dropout(0.30),
            nn.Linear(input_features, num_classes),
        )

    else:
        raise ValueError(
            f"Unsupported architecture: {architecture}"
        )

    if freeze_backbone:
        for parameter in model.parameters():
            parameter.requires_grad = False

        if architecture.startswith("resnet"):
            for parameter in model.fc.parameters():
                parameter.requires_grad = True
        else:
            for parameter in model.classifier.parameters():
                parameter.requires_grad = True

    return model


def trainable_parameters(model: nn.Module):
    return [
        parameter
        for parameter in model.parameters()
        if parameter.requires_grad
    ]


def create_summary_writer(
    enabled: bool,
    log_dir: Path,
):
    if not enabled:
        return None

    try:
        from torch.utils.tensorboard import SummaryWriter
    except ImportError:
        print(
            "Warning: TensorBoard is not installed. "
            "Continuing without TensorBoard logging."
        )
        return None

    log_dir.mkdir(parents=True, exist_ok=True)
    return SummaryWriter(log_dir=str(log_dir))


def run_training_epoch(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    optimizer: torch.optim.Optimizer,
    device: torch.device,
) -> tuple[float, float]:
    model.train()

    total_loss = 0.0
    total_correct = 0
    total_count = 0

    for images, labels in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        optimizer.zero_grad(set_to_none=True)

        logits = model(images)
        loss = criterion(logits, labels)

        loss.backward()
        optimizer.step()

        batch_size = labels.size(0)
        total_loss += loss.item() * batch_size
        total_correct += (
            logits.argmax(dim=1) == labels
        ).sum().item()
        total_count += batch_size

    if total_count == 0:
        raise RuntimeError("The training loader produced no samples.")

    return (
        total_loss / total_count,
        total_correct / total_count,
    )


@torch.no_grad()
def evaluate_model(
    model: nn.Module,
    loader: DataLoader,
    criterion: nn.Module,
    device: torch.device,
) -> dict[str, Any]:
    model.eval()

    total_loss = 0.0
    total_count = 0
    all_labels: list[int] = []
    all_predictions: list[int] = []
    all_probabilities: list[float] = []

    for images, labels in loader:
        images = images.to(device, non_blocking=True)
        labels = labels.to(device, non_blocking=True)

        logits = model(images)
        loss = criterion(logits, labels)
        probabilities = torch.softmax(logits, dim=1)[:, 1]
        predictions = logits.argmax(dim=1)

        batch_size = labels.size(0)
        total_loss += loss.item() * batch_size
        total_count += batch_size

        all_labels.extend(labels.cpu().numpy().tolist())
        all_predictions.extend(
            predictions.cpu().numpy().tolist()
        )
        all_probabilities.extend(
            probabilities.cpu().numpy().tolist()
        )

    if total_count == 0:
        raise RuntimeError("The validation loader produced no samples.")

    labels_array = np.asarray(all_labels)
    predictions_array = np.asarray(all_predictions)
    probabilities_array = np.asarray(all_probabilities)

    tn, fp, fn, tp = confusion_matrix(
        labels_array,
        predictions_array,
        labels=[0, 1],
    ).ravel()

    metrics: dict[str, Any] = {
        "loss": float(total_loss / total_count),
        "accuracy": float(
            accuracy_score(labels_array, predictions_array)
        ),
        "precision": float(
            precision_score(
                labels_array,
                predictions_array,
                zero_division=0,
            )
        ),
        "sensitivity_recall": float(
            recall_score(
                labels_array,
                predictions_array,
                zero_division=0,
            )
        ),
        "specificity": (
            float(tn / (tn + fp))
            if (tn + fp)
            else 0.0
        ),
        "f1": float(
            f1_score(
                labels_array,
                predictions_array,
                zero_division=0,
            )
        ),
        "average_precision": float(
            average_precision_score(
                labels_array,
                probabilities_array,
            )
        ),
        "confusion_matrix": [
            [int(tn), int(fp)],
            [int(fn), int(tp)],
        ],
        "y_true": labels_array,
        "y_pred": predictions_array,
        "y_prob": probabilities_array,
    }

    try:
        metrics["roc_auc"] = float(
            roc_auc_score(
                labels_array,
                probabilities_array,
            )
        )
    except ValueError:
        metrics["roc_auc"] = None

    return metrics


def save_evaluation_artifacts(
    metrics: dict[str, Any],
    class_names: list[str],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    y_true = metrics["y_true"]
    y_pred = metrics["y_pred"]
    y_prob = metrics["y_prob"]

    report = classification_report(
        y_true,
        y_pred,
        target_names=class_names,
        zero_division=0,
        output_dict=True,
    )
    (output_dir / "classification_report.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        display_labels=class_names,
        cmap="Blues",
    )
    plt.tight_layout()
    plt.savefig(
        output_dir / "confusion_matrix.png",
        dpi=180,
        bbox_inches="tight",
    )
    plt.close()

    if len(np.unique(y_true)) == 2:
        RocCurveDisplay.from_predictions(
            y_true,
            y_prob,
            name="Validation ROC",
        )
        plt.tight_layout()
        plt.savefig(
            output_dir / "roc_curve.png",
            dpi=180,
            bbox_inches="tight",
        )
        plt.close()


def load_checkpoint(
    checkpoint_path: Path,
    model: nn.Module,
    optimizer: torch.optim.Optimizer,
    scheduler: ReduceLROnPlateau,
    device: torch.device,
) -> tuple[int, float, list[dict[str, Any]]]:
    checkpoint = torch.load(
        checkpoint_path,
        map_location=device,
    )

    model.load_state_dict(checkpoint["state_dict"])

    if "optimizer_state_dict" in checkpoint:
        optimizer.load_state_dict(
            checkpoint["optimizer_state_dict"]
        )

    if "scheduler_state_dict" in checkpoint:
        scheduler.load_state_dict(
            checkpoint["scheduler_state_dict"]
        )

    start_epoch = int(checkpoint.get("epoch", 0)) + 1
    best_score = float(
        checkpoint.get("best_validation_score", -1.0)
    )
    history = list(checkpoint.get("history", []))

    print(
        f"Resumed from {checkpoint_path} "
        f"at epoch {start_epoch}."
    )

    return start_epoch, best_score, history


def make_serializable_metrics(
    metrics: dict[str, Any],
) -> dict[str, Any]:
    return {
        key: value
        for key, value in metrics.items()
        if key not in {"y_true", "y_pred", "y_prob"}
    }


def main() -> None:
    args = parse_args()
    validate_args(args)
    seed_everything(args.seed)

    device = select_device()
    print(f"Device: {device}")

    (
        train_loader,
        validation_loader,
        class_names,
        validation_dir,
    ) = build_loaders(
        args.data_dir,
        args.image_size,
        args.batch_size,
        args.num_workers,
        device,
    )

    model = build_model(
        architecture=args.architecture,
        num_classes=len(class_names),
        pretrained=not args.no_pretrained,
        freeze_backbone=args.freeze_backbone,
    ).to(device)

    parameters = trainable_parameters(model)
    if not parameters:
        raise RuntimeError(
            "The model has no trainable parameters."
        )

    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(
        parameters,
        lr=args.learning_rate,
        weight_decay=args.weight_decay,
    )
    scheduler = ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=args.scheduler_factor,
        patience=args.scheduler_patience,
    )

    run_dir = args.output_dir / args.architecture
    run_dir.mkdir(parents=True, exist_ok=True)

    writer = create_summary_writer(
        args.tensorboard,
        run_dir / "tensorboard",
    )

    config = TrainingConfig(
        data_dir=str(args.data_dir.expanduser().resolve()),
        architecture=args.architecture,
        epochs=args.epochs,
        batch_size=args.batch_size,
        image_size=args.image_size,
        learning_rate=args.learning_rate,
        weight_decay=args.weight_decay,
        num_workers=args.num_workers,
        patience=args.patience,
        scheduler_patience=args.scheduler_patience,
        scheduler_factor=args.scheduler_factor,
        pretrained=not args.no_pretrained,
        freeze_backbone=args.freeze_backbone,
        seed=args.seed,
        output_dir=str(run_dir.resolve()),
        tensorboard=args.tensorboard,
    )

    (run_dir / "training_config.json").write_text(
        json.dumps(asdict(config), indent=2),
        encoding="utf-8",
    )

    start_epoch = 1
    best_validation_score = -1.0
    best_state = None
    history: list[dict[str, Any]] = []
    epochs_without_improvement = 0

    if args.resume is not None:
        (
            start_epoch,
            best_validation_score,
            history,
        ) = load_checkpoint(
            args.resume.expanduser().resolve(),
            model,
            optimizer,
            scheduler,
            device,
        )

    for epoch in range(start_epoch, args.epochs + 1):
        train_loss, train_accuracy = run_training_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
        )

        validation_metrics = evaluate_model(
            model,
            validation_loader,
            criterion,
            device,
        )

        validation_loss = validation_metrics["loss"]
        scheduler.step(validation_loss)

        current_learning_rate = float(
            optimizer.param_groups[0]["lr"]
        )
        validation_score = (
            validation_metrics["roc_auc"]
            if validation_metrics["roc_auc"] is not None
            else validation_metrics["accuracy"]
        )

        epoch_record = {
            "epoch": epoch,
            "train_loss": float(train_loss),
            "train_accuracy": float(train_accuracy),
            "validation_loss": float(validation_loss),
            "validation_accuracy": float(
                validation_metrics["accuracy"]
            ),
            "validation_roc_auc": (
                None
                if validation_metrics["roc_auc"] is None
                else float(validation_metrics["roc_auc"])
            ),
            "validation_f1": float(
                validation_metrics["f1"]
            ),
            "validation_sensitivity": float(
                validation_metrics["sensitivity_recall"]
            ),
            "validation_specificity": float(
                validation_metrics["specificity"]
            ),
            "learning_rate": current_learning_rate,
        }
        history.append(epoch_record)

        print(
            f"Epoch {epoch:02d}/{args.epochs} | "
            f"train loss={train_loss:.4f}, "
            f"train acc={train_accuracy:.4f} | "
            f"val loss={validation_loss:.4f}, "
            f"val acc={validation_metrics['accuracy']:.4f}, "
            f"val auc={validation_metrics['roc_auc']}, "
            f"val f1={validation_metrics['f1']:.4f} | "
            f"lr={current_learning_rate:.2e}"
        )

        if writer is not None:
            writer.add_scalar(
                "loss/train",
                train_loss,
                epoch,
            )
            writer.add_scalar(
                "loss/validation",
                validation_loss,
                epoch,
            )
            writer.add_scalar(
                "accuracy/train",
                train_accuracy,
                epoch,
            )
            writer.add_scalar(
                "accuracy/validation",
                validation_metrics["accuracy"],
                epoch,
            )
            writer.add_scalar(
                "f1/validation",
                validation_metrics["f1"],
                epoch,
            )
            if validation_metrics["roc_auc"] is not None:
                writer.add_scalar(
                    "auc/validation",
                    validation_metrics["roc_auc"],
                    epoch,
                )
            writer.add_scalar(
                "learning_rate",
                current_learning_rate,
                epoch,
            )

        latest_checkpoint = {
            "epoch": epoch,
            "architecture": args.architecture,
            "class_names": class_names,
            "image_size": args.image_size,
            "state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "best_validation_score": best_validation_score,
            "history": history,
            "config": asdict(config),
        }
        torch.save(
            latest_checkpoint,
            run_dir / "latest_checkpoint.pt",
        )

        if validation_score > best_validation_score:
            best_validation_score = float(validation_score)
            best_state = copy.deepcopy(model.state_dict())
            epochs_without_improvement = 0

            best_checkpoint = {
                "epoch": epoch,
                "architecture": args.architecture,
                "class_names": class_names,
                "image_size": args.image_size,
                "state_dict": best_state,
                "optimizer_state_dict": optimizer.state_dict(),
                "scheduler_state_dict": scheduler.state_dict(),
                "best_validation_score": best_validation_score,
                "history": history,
                "config": asdict(config),
            }
            torch.save(
                best_checkpoint,
                run_dir / "best_model.pt",
            )

            best_metrics = make_serializable_metrics(
                validation_metrics
            )
            (run_dir / "best_metrics.json").write_text(
                json.dumps(best_metrics, indent=2),
                encoding="utf-8",
            )
        else:
            epochs_without_improvement += 1

        (run_dir / "training_history.json").write_text(
            json.dumps(history, indent=2),
            encoding="utf-8",
        )

        if epochs_without_improvement >= args.patience:
            print(
                "Early stopping triggered after "
                f"{args.patience} epoch(s) without improvement."
            )
            break

    if best_state is None:
        best_state = copy.deepcopy(model.state_dict())

    model.load_state_dict(best_state)

    final_metrics = evaluate_model(
        model,
        validation_loader,
        criterion,
        device,
    )
    save_evaluation_artifacts(
        final_metrics,
        class_names,
        run_dir,
    )

    serializable_final_metrics = make_serializable_metrics(
        final_metrics
    )
    final_summary = {
        "architecture": args.architecture,
        "class_names": class_names,
        "image_size": args.image_size,
        "validation_directory": str(validation_dir),
        "best_validation_score": best_validation_score,
        "final_validation_metrics": serializable_final_metrics,
        "history": history,
        "note": (
            "Research and portfolio demonstration only; "
            "not for clinical deployment."
        ),
    }
    (run_dir / "run_summary.json").write_text(
        json.dumps(final_summary, indent=2),
        encoding="utf-8",
    )

    if writer is not None:
        writer.close()

    print()
    print(f"Best validation score: {best_validation_score:.4f}")
    print(f"Saved best model:      {run_dir / 'best_model.pt'}")
    print(f"Saved latest model:    {run_dir / 'latest_checkpoint.pt'}")
    print(f"Saved metrics:         {run_dir / 'best_metrics.json'}")
    print(f"Saved run summary:     {run_dir / 'run_summary.json'}")
    print(f"Saved plots in:        {run_dir}")


if __name__ == "__main__":
    main()
