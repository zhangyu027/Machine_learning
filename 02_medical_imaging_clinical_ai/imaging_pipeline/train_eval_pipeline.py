from pathlib import Path
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split

FEATURE_COLUMNS = [
    "age", "sex_code", "modality_code", "scanner_site_code",
    "image_quality_score", "prior_condition", "is_low_quality_image", "is_cross_sectional"
]


def train_and_evaluate(gold_path: str | Path, output_dir: str | Path = "outputs/tables", model_dir: str | Path = "models") -> dict:
    df = pd.read_csv(gold_path)
    X = df[FEATURE_COLUMNS]
    y = df["abnormal_label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=80, random_state=42, min_samples_leaf=3)
    model.fit(X_train, y_train)
    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs >= 0.5).astype(int)
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "roc_auc": float(roc_auc_score(y_test, probs)),
        "average_precision": float(average_precision_score(y_test, probs)),
        "test_rows": int(len(y_test)),
        "feature_count": int(len(FEATURE_COLUMNS)),
    }
    output_dir = Path(output_dir)
    model_dir = Path(model_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame([metrics]).to_csv(output_dir / "evaluation_metrics.csv", index=False)
    (model_dir / "baseline_imaging_model.json").write_text(json.dumps({
        "model_type": "RandomForestClassifier",
        "feature_columns": FEATURE_COLUMNS,
        "metrics": metrics,
        "note": "Synthetic-data demo model for pipeline validation, not clinical deployment."
    }, indent=2))
    return metrics
