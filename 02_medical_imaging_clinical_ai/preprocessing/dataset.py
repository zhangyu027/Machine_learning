from __future__ import annotations

from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision import datasets, transforms

from config import cfg
from preprocessing.metadata import build_metadata_lookup, load_metadata_table, metadata_dict_to_vector

def default_transform(train: bool = True):
    if train:
        return transforms.Compose([
            transforms.Resize((cfg.image_size, cfg.image_size)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ])
    return transforms.Compose([
        transforms.Resize((cfg.image_size, cfg.image_size)),
        transforms.ToTensor(),
    ])

class ImageFolderWithOptionalMetadata(Dataset):
    def __init__(self, root_dir: Path, train: bool = True):
        self.root_dir = Path(root_dir)
        self.base_dataset = datasets.ImageFolder(self.root_dir, transform=default_transform(train))
        metadata_df = load_metadata_table()
        self.metadata_lookup = build_metadata_lookup(metadata_df) if not metadata_df.empty else {}

    def __len__(self) -> int:
        return len(self.base_dataset)

    def __getitem__(self, idx: int):
        image_tensor, label = self.base_dataset[idx]
        image_path, _ = self.base_dataset.samples[idx]
        rel_path = str(Path(image_path).relative_to(cfg.data_dir)).replace("\\", "/")
        metadata = self.metadata_lookup.get(rel_path, {feat: 0.0 for feat in cfg.metadata_features})
        metadata_tensor = torch.tensor(metadata_dict_to_vector(metadata), dtype=torch.float32)
        return {
            "image": image_tensor,
            "metadata": metadata_tensor,
            "label": torch.tensor(label, dtype=torch.long),
            "rel_path": rel_path,
        }

def load_pil_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")
