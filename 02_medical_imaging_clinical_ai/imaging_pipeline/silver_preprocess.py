from pathlib import Path
import pandas as pd


def create_silver_features(bronze_path: str | Path, output_path: str | Path) -> pd.DataFrame:
    """Standardize imaging metadata and create Silver feature-ready records."""
    df = pd.read_csv(bronze_path)
    df = df.drop_duplicates(subset=["patient_id", "study_id"]).copy()
    df["age_group"] = pd.cut(df["age"], bins=[0, 40, 65, 120], labels=["18_40", "41_65", "66_plus"])
    df["is_low_quality_image"] = (df["image_quality_score"] < 0.70).astype(int)
    df["is_cross_sectional"] = df["modality"].isin(["CT", "MRI"]).astype(int)
    df["sex_code"] = df["sex"].map({"F": 0, "M": 1}).fillna(-1).astype(int)
    df["modality_code"] = df["modality"].map({"XRay": 0, "CT": 1, "MRI": 2}).fillna(-1).astype(int)
    df["scanner_site_code"] = df["scanner_site"].map({"SITE_A": 0, "SITE_B": 1, "SITE_C": 2}).fillna(-1).astype(int)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


def run_silver(bronze_path: str | Path, output_dir: str | Path = "outputs/tables") -> Path:
    output_path = Path(output_dir) / "silver_imaging_features.csv"
    create_silver_features(bronze_path, output_path)
    return output_path
