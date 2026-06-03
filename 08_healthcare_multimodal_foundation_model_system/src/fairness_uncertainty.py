from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score


def subgroup_metrics(predictions_path="outputs/tables/predictions.csv", output_path="outputs/tables/fairness_subgroup_metrics.csv"):
    df = pd.read_csv(predictions_path)
    rows = []

    for group_col in ["sex", "site_id"]:
        for group_value, group in df.groupby(group_col):
            y = group["actual_high_risk"]
            pred = group["predicted_high_risk"]
            prob = group["predicted_probability"]

            row = {
                "subgroup_variable": group_col,
                "subgroup_value": group_value,
                "n": len(group),
                "positive_rate": float(y.mean()),
                "accuracy": float(accuracy_score(y, pred)),
                "f1": float(f1_score(y, pred, zero_division=0)),
            }

            if len(set(y)) > 1:
                row["auc"] = float(roc_auc_score(y, prob))
            else:
                row["auc"] = np.nan

            rows.append(row)

    out = pd.DataFrame(rows)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)
    return out


def uncertainty_table(predictions_path="outputs/tables/predictions.csv", output_path="outputs/tables/uncertainty_review_queue.csv"):
    df = pd.read_csv(predictions_path)
    df["uncertainty"] = 1 - abs(df["predicted_probability"] - 0.5) * 2
    review = df.sort_values("uncertainty", ascending=False).head(50)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    review.to_csv(output_path, index=False)
    return review


if __name__ == "__main__":
    print(subgroup_metrics())
    print(uncertainty_table().head())
