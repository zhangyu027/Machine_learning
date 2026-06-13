from pathlib import Path
import pandas as pd

FEATURE_COLUMNS = [
    "age", "sex_code", "modality_code", "scanner_site_code",
    "image_quality_score", "prior_condition", "is_low_quality_image", "is_cross_sectional"
]


def create_gold_feature_table(silver_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    """Build Gold patient-imaging feature table for model validation."""
    df = pd.read_csv(silver_path)
    gold = df[["patient_id", "study_id", *FEATURE_COLUMNS, "abnormal_label"]].copy()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    gold.to_csv(output_path, index=False)
    return gold


def run_gold(silver_path: str | Path, output_dir: str | Path = "outputs/tables") -> Path:
    output_path = Path(output_dir) / "gold_patient_imaging_features.csv"
    create_gold_feature_table(silver_path, output_path)
    return output_path
