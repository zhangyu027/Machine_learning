from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


def create_synthetic_metadata(labels, output_path):
    rng = np.random.default_rng(42)
    labels = np.array(labels).reshape(-1)
    n = len(labels)

    df = pd.DataFrame({
        "patient_id": [f"P{i:05d}" for i in range(n)],
        "age": rng.normal(55, 15, n).clip(18, 90).round(0),
        "sex": rng.integers(0, 2, n),
        "prior_condition": rng.binomial(1, 0.30, n),
        "scanner_site": rng.integers(0, 3, n),
        "label": labels,
    })

    # Mild signal for demo: positive cases have slightly higher prior condition probability.
    pos = df["label"] == 1
    df.loc[pos, "prior_condition"] = rng.binomial(1, 0.50, pos.sum())

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def normalize_metadata(df):
    meta = df[["age", "sex", "prior_condition", "scanner_site"]].copy()
    meta["age"] = (meta["age"] - meta["age"].mean()) / (meta["age"].std() + 1e-8)
    meta["scanner_site"] = meta["scanner_site"] / max(meta["scanner_site"].max(), 1)
    return meta.astype("float32").values


class ImageOnlyDataset(Dataset):
    def __init__(self, images, labels):
        self.images = images
        self.labels = np.array(labels).reshape(-1)

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.images[idx].astype("float32") / 255.0
        if image.ndim == 2:
            image = image[None, :, :]
        elif image.ndim == 3:
            image = image.transpose(2, 0, 1)
        if image.shape[0] == 3:
            image = image.mean(axis=0, keepdims=True)
        return torch.tensor(image), torch.tensor(self.labels[idx], dtype=torch.long)


class MultimodalDataset(Dataset):
    def __init__(self, images, labels, metadata):
        self.images = images
        self.labels = np.array(labels).reshape(-1)
        self.metadata = metadata

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        image = self.images[idx].astype("float32") / 255.0
        if image.ndim == 2:
            image = image[None, :, :]
        elif image.ndim == 3:
            image = image.transpose(2, 0, 1)
        if image.shape[0] == 3:
            image = image.mean(axis=0, keepdims=True)
        return torch.tensor(image), torch.tensor(self.metadata[idx]), torch.tensor(self.labels[idx], dtype=torch.long)
