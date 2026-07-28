"""Run the local healthcare multimodal demo pipeline.

This script is intentionally executable both ways:

    python scripts/run_pipeline.py
    python -m scripts.run_pipeline

The path bootstrap below keeps the portfolio demo easy to run from the
repository root without requiring package installation.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.healthcare_mm.ingestion.load_sources import load_sample_sources
from src.healthcare_mm.lakehouse.build_gold import build_gold_patient_encounter_table
from src.healthcare_mm.features.multimodal_features import build_feature_frame
from src.healthcare_mm.models.train_readmission_model import train_model
from src.healthcare_mm.mlops.model_card import write_model_card


def main() -> None:
    data_dir = PROJECT_ROOT / "data" / "sample"
    output_dir = PROJECT_ROOT / "outputs"
    model_dir = PROJECT_ROOT / "models"

    sources = load_sample_sources(data_dir)
    gold = build_gold_patient_encounter_table(sources)

    output_dir.mkdir(exist_ok=True)
    gold_path = output_dir / "gold_patient_encounter.csv"
    gold.to_csv(gold_path, index=False)

    features = build_feature_frame(gold)
    feature_path = output_dir / "model_features.csv"
    features.to_csv(feature_path, index=False)

    metrics = train_model(features, model_dir=model_dir, output_dir=output_dir)
    write_model_card(metrics, path=output_dir / "model_card.json")

    print("Healthcare multimodal pipeline completed successfully.")
    print(f"Gold table: {gold_path}")
    print(f"Feature table: {feature_path}")
    print(f"Metrics: {metrics}")


if __name__ == "__main__":
    main()
