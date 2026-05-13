"""
Preprocessing utilities for the Medical Imaging Clinical AI project.

Purpose:
- Load MedMNIST public image data.
- Create or load structured clinical metadata.
- Normalize metadata.
- Save reusable metadata CSV files.

This file is included so the project has a clear preprocessing layer instead
of putting all data preparation only inside the notebook.
"""

from pathlib import Path
import numpy as np
import pandas as pd


def create_synthetic_metadata(labels, output_path):
    """
    Create synthetic structured metadata for MedMNIST images.

    MedMNIST provides images and labels, but not full structured clinical metadata.
    This synthetic metadata is for portfolio demonstration only.

    Replace this function with real metadata loading for real clinical research.
    """
    rng = np.random.default_rng(42)
    labels = np.array(labels).reshape(-1)
    n = len(labels)

    metadata = pd.DataFrame({
        "patient_id": [f"P{i:05d}" for i in range(n)],
        "age": rng.normal(55, 15, n).clip(18, 90).round(0),
        "sex": rng.integers(0, 2, n),
        "prior_condition": rng.binomial(1, 0.30, n),
        "scanner_site": rng.integers(0, 3, n),
        "label": labels,
    })

    # Mild signal for demo: positive cases have slightly higher prior-condition probability.
    positive_mask = metadata["label"] == 1
    metadata.loc[positive_mask, "prior_condition"] = rng.binomial(
        1,
        0.50,
        positive_mask.sum()
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    metadata.to_csv(output_path, index=False)

    return metadata


def normalize_metadata(metadata_df):
    """
    Normalize structured metadata for multimodal modeling.
    """
    meta = metadata_df[["age", "sex", "prior_condition", "scanner_site"]].copy()

    meta["age"] = (meta["age"] - meta["age"].mean()) / (meta["age"].std() + 1e-8)
    meta["scanner_site"] = meta["scanner_site"] / max(meta["scanner_site"].max(), 1)

    return meta.astype("float32").values


def save_preprocessing_summary(train_metadata, test_metadata, output_path):
    """
    Save a simple preprocessing summary for the portfolio report.
    """
    summary = pd.DataFrame([
        {
            "split": "train",
            "n_rows": len(train_metadata),
            "mean_age": train_metadata["age"].mean(),
            "positive_rate": train_metadata["label"].mean(),
        },
        {
            "split": "test",
            "n_rows": len(test_metadata),
            "mean_age": test_metadata["age"].mean(),
            "positive_rate": test_metadata["label"].mean(),
        },
    ])

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)

    return summary
