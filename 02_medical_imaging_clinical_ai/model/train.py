from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from config import cfg
from preprocessing.dataset import ImageFolderWithOptionalMetadata
from model.cnn_backbone import CNNClassifier
from model.multimodal_model import MultimodalGraphModel
from model.graph_fusion import SimpleKNNGraphRefiner
from model.utils import save_json, save_pickle, to_numpy

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def build_model():
    if cfg.model_type == "cnn":
        return CNNClassifier(num_classes=cfg.num_classes)
    if cfg.model_type == "multimodal_graph":
        return MultimodalGraphModel(
            metadata_dim=len(cfg.metadata_features),
            num_classes=cfg.num_classes,
        )
    raise ValueError(f"Unsupported MODEL_TYPE: {cfg.model_type}")

def forward_batch(model, batch):
    images = batch["image"].to(DEVICE)
    labels = batch["label"].to(DEVICE)

    if cfg.model_type == "cnn":
        logits, embeddings = model(images)
    else:
        metadata = batch["metadata"].to(DEVICE)
        logits, embeddings = model(images, metadata)
    return logits, embeddings, labels

def main():
    train_dataset = ImageFolderWithOptionalMetadata(cfg.train_dir, train=True)
    val_dataset = ImageFolderWithOptionalMetadata(cfg.val_dir, train=False)

    if len(train_dataset) == 0:
        print("No training images found. Add files under data/train/* and rerun.")
        return

    train_loader = DataLoader(train_dataset, batch_size=cfg.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=cfg.batch_size, shuffle=False) if len(val_dataset) else None

    model = build_model().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=cfg.learning_rate)
    criterion = nn.CrossEntropyLoss()

    best_val_loss = float("inf")
    history = []

    for epoch in range(cfg.epochs):
        model.train()
        running_loss = 0.0
        for batch in train_loader:
            optimizer.zero_grad()
            logits, _, labels = forward_batch(model, batch)
            loss = criterion(logits, labels)
            loss.backward()
            optimizer.step()
            running_loss += float(loss.item())

        avg_train_loss = running_loss / max(len(train_loader), 1)
        epoch_record = {"epoch": epoch + 1, "train_loss": avg_train_loss}

        if val_loader is not None:
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for batch in val_loader:
                    logits, _, labels = forward_batch(model, batch)
                    loss = criterion(logits, labels)
                    val_loss += float(loss.item())
            avg_val_loss = val_loss / max(len(val_loader), 1)
            epoch_record["val_loss"] = avg_val_loss
            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                torch.save(model.state_dict(), cfg.model_path)
        else:
            torch.save(model.state_dict(), cfg.model_path)

        history.append(epoch_record)
        print(epoch_record)

    # Build a lightweight graph cache from training embeddings for multimodal_graph mode.
    if cfg.model_type == "multimodal_graph":
        model.eval()
        all_embeddings = []
        all_probs = []
        all_paths = []
        with torch.no_grad():
            for batch in DataLoader(train_dataset, batch_size=cfg.batch_size, shuffle=False):
                logits, embeddings, _ = forward_batch(model, batch)
                probs = torch.softmax(logits, dim=1)
                all_embeddings.append(to_numpy(embeddings))
                all_probs.append(to_numpy(probs))
                all_paths.extend(batch["rel_path"])
        refiner = SimpleKNNGraphRefiner(k=cfg.knn_k, alpha=cfg.blend_alpha)
        refiner.fit(
            embeddings=np.vstack(all_embeddings),
            probabilities=np.vstack(all_probs),
            rel_paths=all_paths,
        )
        save_pickle(refiner, cfg.graph_cache_path)

    save_json({"history": history, "model_type": cfg.model_type}, cfg.artifacts_dir / "train_history.json")
    print(f"Saved model to {cfg.model_path}")

if __name__ == "__main__":
    main()
