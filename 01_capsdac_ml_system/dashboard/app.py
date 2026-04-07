import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from config import DATA_DIR, MODELS_DIR, TARGET_COLUMN

st.set_page_config(page_title="CAPSDAC Enrollment Prediction", layout="wide")
st.title("CAPSDAC Preschool Enrollment Prediction")

model = joblib.load(MODELS_DIR / "xgboost.joblib")
test_df = pd.read_csv(DATA_DIR / "test_features.csv")

X_test = test_df.drop(columns=[TARGET_COLUMN])
y_test = test_df[TARGET_COLUMN]

st.subheader("Sample Predictions")
sample_n = st.slider("Number of rows", 5, 50, 10)
sample_df = X_test.head(sample_n).copy()
sample_df["actual"] = y_test.head(sample_n).values
sample_df["predicted"] = model.predict(sample_df.drop(columns=["actual"]))
sample_df["probability"] = model.predict_proba(sample_df.drop(columns=["actual"]))[:, 1]

st.dataframe(sample_df)

st.subheader("Feature Importance")
importances = pd.DataFrame({
    "feature": X_test.columns,
    "importance": model.feature_importances_,
}).sort_values("importance", ascending=False).head(20)

st.bar_chart(importances.set_index("feature"))
