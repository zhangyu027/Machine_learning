"""Dataset and metadata utilities for the medical imaging demo."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset


METADATA_COLUMNS = ["age", "sex", "prior_condition", "scanner_site"]


def create_synthetic_metadata(
    labels: Any,
    output_path: str | Path,
) -> pd.DataFrame:
    """Create reproducible synthetic clinical metadata for demonstration use."""
    rng = np.random.default_rng(42)
    labels_array = np.asarray(labels).reshape(-1)
    sample_count = len(labels_array)

    dataframe = pd.DataFrame(
        {
            "patient_id": [f"P{i:05d}" for i in range(sample_count)],
            "age": rng.normal(55, 15, sample_count).clip(18, 90).round(0),
            "sex": rng.integers(0, 2, sample_count),
            "prior_condition": rng.binomial(1, 0.30, sample_count),
            "scanner_site": rng.integers(0, 3, sample_count),
            "label": labels_array,
        }
    )

    # Mild synthetic signal for demonstration only.
    positive_rows = dataframe["label"] == 1
    dataframe.loc[positive_rows, "prior_condition"] = rng.binomial(
        1,
        0.50,
        int(positive_rows.sum()),
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)
    return dataframe


def fit_metadata_normalizer(dataframe: pd.DataFrame) -> dict[str, float]:
    """Fit normalization statistics using training metadata only."""
    _validate_metadata_columns(dataframe)

    age_mean = float(dataframe["age"].mean())
    age_std = float(dataframe["age"].std())

    if not np.isfinite(age_std) or age_std <= 0:
        age_std = 1.0

    scanner_max = float(max(dataframe["scanner_site"].max(), 1))

    return {
        "age_mean": age_mean,
        "age_std": age_std,
        "scanner_max": scanner_max,
    }


def normalize_metadata(
    dataframe: pd.DataFrame,
    normalizer: dict[str, float] | None = None,
    *,
    return_normalizer: bool = False,
):
    """Normalize metadata without leaking validation/test statistics.

    Existing notebook compatibility is preserved: by default this returns only
    the NumPy feature matrix. Set ``return_normalizer=True`` when fitting the
    training split so the same statistics can be reused on validation/test data.
    """
    _validate_metadata_columns(dataframe)

    fitted_normalizer = (
        fit_metadata_normalizer(dataframe)
        if normalizer is None
        else normalizer
    )

    required_keys = {"age_mean", "age_std", "scanner_max"}
    missing_keys = required_keys.difference(fitted_normalizer)
    if missing_keys:
        raise ValueError(
            "Normalizer is missing required keys: "
            + ", ".join(sorted(missing_keys))
        )

    metadata = dataframe[METADATA_COLUMNS].copy()
    metadata["age"] = (
        metadata["age"] - fitted_normalizer["age_mean"]
    ) / fitted_normalizer["age_std"]
    metadata["scanner_site"] = (
        metadata["scanner_site"] / fitted_normalizer["scanner_max"]
    )

    values = metadata.astype("float32").to_numpy()

    if return_normalizer:
        return values, fitted_normalizer
    return values


def _validate_metadata_columns(dataframe: pd.DataFrame) -> None:
    missing = [column for column in METADATA_COLUMNS if column not in dataframe]
    if missing:
        raise ValueError(
            "Metadata is missing required columns: " + ", ".join(missing)
        )


def _prepare_image(image: Any) -> torch.Tensor:
    image_array = np.asarray(image, dtype=np.float32)

    if image_array.ndim == 2:
        image_array = image_array[None, :, :]
    elif image_array.ndim == 3:
        # Convert HWC to CHW when the channel dimension is last.
        if image_array.shape[-1] in (1, 3, 4):
            image_array = image_array.transpose(2, 0, 1)
    else:
        raise ValueError(
            f"Expected a 2D or 3D image, received shape {image_array.shape}."
        )

    # Remove alpha if present.
    if image_array.shape[0] == 4:
        image_array = image_array[:3]

    # This project uses one-channel image models.
    if image_array.shape[0] == 3:
        image_array = image_array.mean(axis=0, keepdims=True)

    if image_array.shape[0] != 1:
        raise ValueError(
            f"Expected one image channel after conversion; got {image_array.shape[0]}."
        )

    # Normalize common integer image ranges while preserving already normalized data.
    if image_array.size and image_array.max() > 1.0:
        image_array = image_array / 255.0

    return torch.as_tensor(image_array, dtype=torch.float32)


class ImageOnlyDataset(Dataset):
    """PyTorch dataset returning ``(image, label)``."""

    def __init__(self, images: Any, labels: Any):
        self.images = np.asarray(images)
        self.labels = np.asarray(labels).reshape(-1)

        if len(self.images) != len(self.labels):
            raise ValueError(
                "images and labels must contain the same number of records"
            )

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        return (
            _prepare_image(self.images[idx]),
            torch.as_tensor(self.labels[idx], dtype=torch.long),
        )


class MultimodalDataset(Dataset):
    """PyTorch dataset returning ``(image, metadata, label)``."""

    def __init__(self, images: Any, labels: Any, metadata: Any):
        self.images = np.asarray(images)
        self.labels = np.asarray(labels).reshape(-1)
        self.metadata = np.asarray(metadata, dtype=np.float32)

        record_count = len(self.labels)
        if len(self.images) != record_count:
            raise ValueError(
                "images and labels must contain the same number of records"
            )
        if len(self.metadata) != record_count:
            raise ValueError(
                "metadata and labels must contain the same number of records"
            )

    def __len__(self) -> int:
        return len(self.labels)

    def __getitem__(self, idx: int):
        return (
            _prepare_image(self.images[idx]),
            torch.as_tensor(self.metadata[idx], dtype=torch.float32),
            torch.as_tensor(self.labels[idx], dtype=torch.long),
        )
