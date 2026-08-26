"""Audit class prevalence and label balance for all benchmark endpoints.

This script is intentionally separate from the frozen scientific benchmark.
It reuses the same scaffold-aware split function so prevalence is measured on
the same train/validation/test partitioning logic used by the benchmark.

Outputs:
- reports/endpoint_label_audit.csv
- reports/endpoint_label_audit_by_split.csv

Example:
    python experiments/audit_endpoint_labels.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np

from pharma_genai.data.scaffold_split import (
    scaffold_split_indices,
    assert_no_scaffold_overlap,
)


ENDPOINTS = {
    "hERG": "data/processed/herg.csv",
    "BBBP": "data/BBBP/bbbp.csv",
    "ClinTox": "data/ClinTox/clintox.csv",
    "Tox21": "data/Tox21/tox21_task0.csv",
}


def require_file(path: str) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Required dataset not found: {p}\n"
            "Run/download the endpoint dataset before auditing labels."
        )
    return p


def summarize_labels(y: np.ndarray) -> dict:
    y = np.asarray(y, dtype=int)
    n_total = int(len(y))
    n_positive = int((y == 1).sum())
    n_negative = int((y == 0).sum())
    positive_rate = float(n_positive / n_total) if n_total else np.nan

    return {
        "n_total": n_total,
        "n_positive": n_positive,
        "n_negative": n_negative,
        "positive_rate": positive_rate,
    }


def main() -> None:
    overall_rows = []
    split_rows = []

    for endpoint, path in ENDPOINTS.items():
        df = (
            pd.read_csv(require_file(path))
            .dropna(subset=["smiles", "target"])
            .reset_index(drop=True)
        )

        smiles = df["smiles"].astype(str).tolist()
        y = df["target"].astype(int).to_numpy()

        unique_labels = sorted(set(y.tolist()))
        if not set(unique_labels).issubset({0, 1}):
            raise ValueError(
                f"{endpoint}: target must be binary 0/1, found labels {unique_labels}"
            )

        tr, va, te = scaffold_split_indices(smiles)
        assert_no_scaffold_overlap(smiles, [tr, va, te])

        overall = summarize_labels(y)
        overall_rows.append({
            "endpoint": endpoint,
            "dataset_path": path,
            **overall,
            "train_positive_rate": summarize_labels(y[tr])["positive_rate"],
            "validation_positive_rate": summarize_labels(y[va])["positive_rate"],
            "test_positive_rate": summarize_labels(y[te])["positive_rate"],
            "train_n": int(len(tr)),
            "validation_n": int(len(va)),
            "test_n": int(len(te)),
        })

        for split_name, idx in [
            ("train", tr),
            ("validation", va),
            ("test", te),
        ]:
            stats = summarize_labels(y[idx])
            split_rows.append({
                "endpoint": endpoint,
                "split": split_name,
                **stats,
            })

    reports = Path("reports")
    reports.mkdir(parents=True, exist_ok=True)

    overall_df = pd.DataFrame(overall_rows)
    split_df = pd.DataFrame(split_rows)

    overall_out = reports / "endpoint_label_audit.csv"
    split_out = reports / "endpoint_label_audit_by_split.csv"

    overall_df.to_csv(overall_out, index=False)
    split_df.to_csv(split_out, index=False)

    print("\n=== Endpoint label audit ===")
    display_cols = [
        "endpoint",
        "n_total",
        "n_positive",
        "n_negative",
        "positive_rate",
        "train_positive_rate",
        "validation_positive_rate",
        "test_positive_rate",
    ]
    print(
        overall_df[display_cols].to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\n=== Split-level audit ===")
    print(
        split_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\nSaved:")
    print(f"  {overall_out}")
    print(f"  {split_out}")


if __name__ == "__main__":
    main()
