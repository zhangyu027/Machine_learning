"""Training and evaluation helpers for image-only and multimodal models."""

from __future__ import annotations

from typing import Any

import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def _move_batch_to_device(
    batch: Any,
    device: str | torch.device,
):
    if not isinstance(batch, (tuple, list)):
        raise TypeError("A dataloader batch must be a tuple or list.")

    if len(batch) == 2:
        images, labels = batch
        return (
            images.to(device),
            None,
            labels.to(device).long().view(-1),
        )

    if len(batch) == 3:
        images, metadata, labels = batch
        return (
            images.to(device),
            metadata.to(device).float(),
            labels.to(device).long().view(-1),
        )

    raise ValueError(
        f"Expected a two-item or three-item batch, received {len(batch)} items."
    )


def train_image_model(
    model,
    loader,
    epochs: int = 2,
    lr: float = 1e-3,
    device: str | torch.device = "cpu",
):
    model.to(device)
    optimizer = torch.optim.AdamW(
        (parameter for parameter in model.parameters() if parameter.requires_grad),
        lr=lr,
    )
    loss_fn = nn.CrossEntropyLoss()
    history: list[float] = []

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for batch in loader:
            images, _, labels = _move_batch_to_device(batch, device)

            optimizer.zero_grad(set_to_none=True)
            logits = model(images)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / max(len(loader.dataset), 1)
        history.append(float(epoch_loss))
        print(f"Epoch {epoch + 1}/{epochs} loss={epoch_loss:.4f}")

    return history


def train_multimodal_model(
    model,
    loader,
    epochs: int = 2,
    lr: float = 1e-3,
    device: str | torch.device = "cpu",
):
    model.to(device)
    optimizer = torch.optim.AdamW(
        (parameter for parameter in model.parameters() if parameter.requires_grad),
        lr=lr,
    )
    loss_fn = nn.CrossEntropyLoss()
    history: list[float] = []

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0

        for batch in loader:
            images, metadata, labels = _move_batch_to_device(batch, device)

            if metadata is None:
                raise ValueError(
                    "Multimodal training requires batches containing "
                    "(images, metadata, labels)."
                )

            optimizer.zero_grad(set_to_none=True)
            logits = model(images, metadata)
            loss = loss_fn(logits, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * images.size(0)

        epoch_loss = running_loss / max(len(loader.dataset), 1)
        history.append(float(epoch_loss))
        print(
            f"Epoch {epoch + 1}/{epochs} "
            f"multimodal_loss={epoch_loss:.4f}"
        )

    return history


def compute_metrics(y_true, y_pred, y_prob):
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    y_prob = np.asarray(y_prob)

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(
            precision_score(y_true, y_pred, zero_division=0)
        ),
        "sensitivity_recall": float(
            recall_score(y_true, y_pred, zero_division=0)
        ),
        "specificity": (
            float(tn / (tn + fp))
            if (tn + fp)
            else 0.0
        ),
        "f1": float(f1_score(y_true, y_pred, zero_division=0)),
        "confusion_matrix": [
            [int(tn), int(fp)],
            [int(fn), int(tp)],
        ],
    }

    try:
        metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        metrics["average_precision"] = float(
            average_precision_score(y_true, y_prob)
        )
    except ValueError:
        metrics["roc_auc"] = None
        metrics["average_precision"] = None

    return metrics


@torch.no_grad()
def evaluate_image_model(
    model,
    loader,
    device: str | torch.device = "cpu",
):
    model.to(device).eval()
    y_true: list[int] = []
    y_pred: list[int] = []
    y_prob: list[float] = []

    for batch in loader:
        images, _, labels = _move_batch_to_device(batch, device)
        logits = model(images)
        probabilities = torch.softmax(logits, dim=1)[:, 1]

        y_true.extend(labels.detach().cpu().numpy().tolist())
        y_pred.extend(
            logits.argmax(dim=1).detach().cpu().numpy().tolist()
        )
        y_prob.extend(
            probabilities.detach().cpu().numpy().tolist()
        )

    arrays = tuple(
        np.asarray(values)
        for values in (y_true, y_pred, y_prob)
    )
    return compute_metrics(*arrays), *arrays


@torch.no_grad()
def evaluate_multimodal_model(
    model,
    loader,
    device: str | torch.device = "cpu",
):
    model.to(device).eval()
    y_true: list[int] = []
    y_pred: list[int] = []
    y_prob: list[float] = []

    for batch in loader:
        images, metadata, labels = _move_batch_to_device(batch, device)

        if metadata is None:
            raise ValueError(
                "Multimodal evaluation requires batches containing "
                "(images, metadata, labels)."
            )

        logits = model(images, metadata)
        probabilities = torch.softmax(logits, dim=1)[:, 1]

        y_true.extend(labels.detach().cpu().numpy().tolist())
        y_pred.extend(
            logits.argmax(dim=1).detach().cpu().numpy().tolist()
        )
        y_prob.extend(
            probabilities.detach().cpu().numpy().tolist()
        )

    arrays = tuple(
        np.asarray(values)
        for values in (y_true, y_pred, y_prob)
    )
    return compute_metrics(*arrays), *arrays
