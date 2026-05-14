from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
import joblib


STRUCTURED_COLS = ["age", "sex", "prior_condition", "site_id"]
LAB_COLS = ["lab_crp", "lab_wbc", "lab_creatinine", "oxygen_saturation"]


def prepare_features(
    csv_path="data/raw/synthetic_multimodal_patients.csv",
    image_path="data/raw/synthetic_images.npy",
    output_dir="data/processed",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)
    images = np.load(image_path).astype("float32")

    structured_scaler = StandardScaler()
    lab_scaler = StandardScaler()

    X_structured = structured_scaler.fit_transform(df[STRUCTURED_COLS]).astype("float32")
    X_labs = lab_scaler.fit_transform(df[LAB_COLS]).astype("float32")

    text_vectorizer = TfidfVectorizer(max_features=64, ngram_range=(1, 2))
    X_text = text_vectorizer.fit_transform(df["clinical_note"].fillna("")).toarray().astype("float32")

    y = df["high_risk"].values.astype("float32")
    subgroup_sex = df["sex"].values
    subgroup_site = df["site_id"].values

    np.savez_compressed(
        output_dir / "multimodal_features.npz",
        images=images,
        structured=X_structured,
        labs=X_labs,
        text=X_text,
        y=y,
        subgroup_sex=subgroup_sex,
        subgroup_site=subgroup_site,
    )

    joblib.dump(structured_scaler, output_dir / "structured_scaler.joblib")
    joblib.dump(lab_scaler, output_dir / "lab_scaler.joblib")
    joblib.dump(text_vectorizer, output_dir / "text_vectorizer.joblib")

    feature_metadata = {
        "structured_cols": STRUCTURED_COLS,
        "lab_cols": LAB_COLS,
        "text_features": int(X_text.shape[1]),
        "image_shape": list(images.shape[1:]),
        "n_patients": int(len(df)),
    }

    pd.Series(feature_metadata).to_json(output_dir / "feature_metadata.json", indent=2)

    return feature_metadata


if __name__ == "__main__":
    print(prepare_features())
