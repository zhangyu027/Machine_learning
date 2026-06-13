"""Train a baseline TF-IDF + Logistic Regression model for clinical note triage."""
from pathlib import Path
import json
import pandas as pd
from joblib import dump
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "outputs" / "clinical_notes_processed.csv"
MODEL_DIR = ROOT / "models"
OUT_DIR = ROOT / "outputs"
MODEL_PATH = MODEL_DIR / "baseline_tfidf.joblib"
PRED_PATH = OUT_DIR / "baseline_predictions.csv"
METRICS_PATH = OUT_DIR / "model_metrics.json"
MODEL_DIR.mkdir(parents=True, exist_ok=True)
OUT_DIR.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    if not PROCESSED.exists():
        raise FileNotFoundError("Processed data not found. Run: python databricks_pipeline/spark_preprocess.py")
    df = pd.read_csv(PROCESSED)
    X_train, X_test, y_train, y_test = train_test_split(
        df["clean_text"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
    )
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(max_features=3000, ngram_range=(1, 2))),
        ("clf", LogisticRegression(max_iter=500)),
    ])
    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    metrics = {
        "accuracy": float(accuracy_score(y_test, preds)),
        "macro_f1": float(f1_score(y_test, preds, average="macro")),
        "test_rows": int(len(y_test)),
        "train_rows": int(len(y_train)),
        "model_type": "tfidf_logistic_regression",
        "data_type": "synthetic_demo_data",
    }
    pd.DataFrame({"label": y_test, "prediction": preds}).to_csv(PRED_PATH, index=False)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    (OUT_DIR / "classification_report.txt").write_text(classification_report(y_test, preds))
    dump(pipeline, MODEL_PATH)
    print(f"Saved model: {MODEL_PATH}")
    print(f"Metrics: {metrics}")
