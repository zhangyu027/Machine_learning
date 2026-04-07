import joblib
import pandas as pd
from config import MODELS_DIR

def predict_from_dataframe(input_df: pd.DataFrame) -> pd.DataFrame:
    model = joblib.load(MODELS_DIR / "xgboost.joblib")
    feature_columns = joblib.load(MODELS_DIR / "feature_columns.joblib")

    aligned = input_df.reindex(columns=feature_columns, fill_value=0)
    probs = model.predict_proba(aligned)[:, 1]
    preds = model.predict(aligned)

    result = aligned.copy()
    result["predicted_enrollment_flag"] = preds
    result["predicted_probability"] = probs
    return result
