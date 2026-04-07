import joblib
import pandas as pd
import shap
import matplotlib.pyplot as plt
from config import DATA_DIR, MODELS_DIR, TARGET_COLUMN, OUTPUT_DIR

def main() -> None:
    model = joblib.load(MODELS_DIR / "xgboost.joblib")
    test_df = pd.read_csv(DATA_DIR / "test_features.csv")

    X_test = test_df.drop(columns=[TARGET_COLUMN])

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    plt.figure()
    shap.summary_plot(shap_values, X_test, show=False)
    out_path = OUTPUT_DIR / "shap_summary.png"
    plt.savefig(out_path, bbox_inches="tight")
    print(f"Saved SHAP summary to {out_path}")

if __name__ == "__main__":
    main()
