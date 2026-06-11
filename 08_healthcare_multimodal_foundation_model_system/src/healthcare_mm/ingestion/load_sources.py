"""Synthetic source loaders for the local portfolio demo."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd


def load_sample_sources(base_path: str | Path = "data/sample") -> Dict[str, pd.DataFrame]:
    """Load synthetic FHIR-style, notes, vitals, and imaging metadata sources."""
    base = Path(base_path)
    return {
        "patients": pd.read_csv(base / "fhir" / "patient.csv"),
        "encounters": pd.read_csv(base / "fhir" / "encounter.csv"),
        "labs": pd.read_csv(base / "fhir" / "labs.csv"),
        "vitals": pd.read_csv(base / "vitals" / "vitals.csv"),
        "notes": pd.read_csv(base / "notes" / "clinical_notes.csv"),
        "images": pd.read_csv(base / "imaging_metadata" / "imaging_manifest.csv"),
    }
