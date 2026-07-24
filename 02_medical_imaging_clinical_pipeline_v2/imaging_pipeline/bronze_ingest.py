from pathlib import Path
import numpy as np
import pandas as pd


def build_synthetic_imaging_source(output_path: str | Path, n: int = 240, seed: int = 42) -> pd.DataFrame:
    """Create synthetic imaging metadata and clinical attributes for local demo validation."""
    rng = np.random.default_rng(seed)
    patient_id = [f"P{i:05d}" for i in range(n)]
    study_id = [f"IMG{i:06d}" for i in range(n)]
    age = rng.normal(58, 14, n).clip(18, 90).round(0).astype(int)
    sex = rng.choice(["F", "M"], size=n)
    modality = rng.choice(["XRay", "CT", "MRI"], size=n, p=[0.55, 0.30, 0.15])
    scanner_site = rng.choice(["SITE_A", "SITE_B", "SITE_C"], size=n)
    image_quality_score = rng.normal(0.82, 0.10, n).clip(0.40, 1.00).round(3)
    prior_condition = rng.binomial(1, 0.32, n)
    abnormal_probability = 1 / (1 + np.exp(-(-2.0 + 0.025 * (age - 50) + 0.9 * prior_condition + 1.2 * (image_quality_score < 0.72))))
    label = rng.binomial(1, abnormal_probability)
    df = pd.DataFrame({
        "patient_id": patient_id,
        "study_id": study_id,
        "age": age,
        "sex": sex,
        "modality": modality,
        "scanner_site": scanner_site,
        "image_quality_score": image_quality_score,
        "prior_condition": prior_condition,
        "abnormal_label": label,
    })
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def run_bronze(output_dir: str | Path = "outputs/tables") -> Path:
    output_path = Path(output_dir) / "bronze_imaging_metadata.csv"
    build_synthetic_imaging_source(output_path)
    return output_path
