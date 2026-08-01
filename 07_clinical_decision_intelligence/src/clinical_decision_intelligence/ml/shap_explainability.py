import numpy as np
import pandas as pd
import shap

def compute_shap_feature_importance(model, X: pd.DataFrame, sample_size=1000, seed=42) -> pd.DataFrame:
    sample = X.sample(min(sample_size, len(X)), random_state=seed)
    explainer = shap.TreeExplainer(model)
    values = explainer.shap_values(sample)
    if isinstance(values, list):
        values = values[1]
    return pd.DataFrame({
        "feature": sample.columns,
        "mean_abs_shap": np.abs(values).mean(axis=0)
    }).sort_values("mean_abs_shap", ascending=False)
