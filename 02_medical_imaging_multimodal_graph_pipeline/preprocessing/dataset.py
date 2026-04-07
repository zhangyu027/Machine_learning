from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from config import (
    TRAIN_DIR, VAL_DIR, TEST_DIR, DATA_DIR, METADATA_CSV,
    IMAGE_SIZE, BATCH_SIZE, NUM_WORKERS
)

IMG_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".tif", ".tiff"}

def build_transforms(train: bool = True):
    if train:
        return transforms.Compose([
            transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
            transforms.RandomHorizontalFlip(),
            transforms.RandomRotation(10),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
    return transforms.Compose([
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225]),
    ])

def discover_classes(split_dir: Path) -> List[str]:
    return sorted([p.name for p in split_dir.iterdir() if p.is_dir()])

def discover_samples(split_dir: Path) -> Tuple[List[Tuple[Path, int, str]], List[str]]:
    classes = discover_classes(split_dir)
    class_to_idx = {name: i for i, name in enumerate(classes)}
    samples = []

    for class_name in classes:
        class_dir = split_dir / class_name
        for img_path in sorted(class_dir.rglob("*")):
            if img_path.is_file() and img_path.suffix.lower() in IMG_EXTS:
                rel_path = str(img_path.relative_to(DATA_DIR)).replace("\\", "/")
                samples.append((img_path, class_to_idx[class_name], rel_path))
    return samples, classes

def load_metadata() -> Tuple[Optional[pd.DataFrame], List[str]]:
    if not METADATA_CSV.exists():
        return None, []

    df = pd.read_csv(METADATA_CSV)
    if "rel_path" not in df.columns:
        raise ValueError("metadata.csv must contain a 'rel_path' column.")

    reserved = {"rel_path", "label", "split", "patient_id"}
    feature_cols = [c for c in df.columns if c not in reserved]
    if not feature_cols:
        return df[["rel_path"]].copy(), []

    for c in feature_cols:
        df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0.0)

    return df, feature_cols

class MedicalImageMultimodalDataset(Dataset):
    def __init__(self, split_dir: Path, train: bool, metadata_df=None, metadata_cols=None):
        self.samples, self.classes = discover_samples(split_dir)
        self.transform = build_transforms(train=train)
        self.metadata_df = metadata_df
        self.metadata_cols = metadata_cols or []
        self.metadata_lookup: Dict[str, List[float]] = {}

        if self.metadata_df is not None and self.metadata_cols:
            for _, row in self.metadata_df.iterrows():
                rel = str(row["rel_path"]).replace("\\", "/")
                self.metadata_lookup[rel] = [float(row[c]) for c in self.metadata_cols]

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        img_path, label, rel_path = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        image = self.transform(image)

        if self.metadata_cols:
            features = self.metadata_lookup.get(rel_path, [0.0] * len(self.metadata_cols))
        else:
            features = []

        metadata = torch.tensor(features, dtype=torch.float32)
        return image, torch.tensor(label, dtype=torch.long), metadata, rel_path

def build_dataloaders():
    metadata_df, metadata_cols = load_metadata()

    train_ds = MedicalImageMultimodalDataset(TRAIN_DIR, train=True, metadata_df=metadata_df, metadata_cols=metadata_cols)
    val_ds = MedicalImageMultimodalDataset(VAL_DIR, train=False, metadata_df=metadata_df, metadata_cols=metadata_cols)
    test_ds = MedicalImageMultimodalDataset(TEST_DIR, train=False, metadata_df=metadata_df, metadata_cols=metadata_cols)

    train_loader = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=NUM_WORKERS)
    val_loader = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)
    test_loader = DataLoader(test_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=NUM_WORKERS)

    info = {
        "classes": train_ds.classes,
        "metadata_dim": len(metadata_cols),
        "metadata_columns": metadata_cols,
        "train_size": len(train_ds),
        "val_size": len(val_ds),
        "test_size": len(test_ds),
    }
    return train_loader, val_loader, test_loader, info
