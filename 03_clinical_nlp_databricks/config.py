from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data" / "sample"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = PROJECT_ROOT / "models"
RAW_DATA_PATH = DATA_DIR / "clinical_notes_raw.csv"
PROCESSED_DATA_PATH = OUTPUT_DIR / "clinical_notes_processed.csv"
FEATURE_DATA_PATH = OUTPUT_DIR / "clinical_nlp_features.csv"
PREDICTIONS_PATH = OUTPUT_DIR / "baseline_predictions.csv"
METRICS_PATH = OUTPUT_DIR / "model_metrics.json"
EVALUATION_SUMMARY_PATH = OUTPUT_DIR / "evaluation_summary.json"
MODEL_PATH = MODEL_DIR / "baseline_tfidf.joblib"
