"""Compare frozen classical single-task baselines against the multi-task ADMET MLP.

Inputs
------
reports/cross_endpoint_summary.csv
reports/multitask_admet_metrics.csv

Outputs
-------
reports/multitask_vs_classical.csv
reports/multitask_vs_classical_wins.csv
reports/multitask_vs_classical_summary.csv

Example
-------
python experiments/compare_multitask_vs_classical.py
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


CLASSICAL_PATH = Path("reports/cross_endpoint_summary.csv")
MULTITASK_PATH = Path("reports/multitask_admet_metrics.csv")

OUTPUT_DETAIL = Path("reports/multitask_vs_classical.csv")
OUTPUT_WINS = Path("reports/multitask_vs_classical_wins.csv")
OUTPUT_SUMMARY = Path("reports/multitask_vs_classical_summary.csv")


HIGHER_IS_BETTER = {
    "roc_auc": True,
    "average_precision": True,
    "balanced_accuracy": True,
    "f1": True,
    "accuracy": True,
    "brier_score": False,
    "ece_10bin": False,
}


def require_file(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            "Run the frozen classical comparison and multi-task experiment first."
        )
    return path


def best_classical_by_metric(classical: pd.DataFrame, endpoint: str, metric: str) -> pd.Series:
    subset = classical[classical["endpoint"] == endpoint].copy()
    if subset.empty:
        raise ValueError(f"No classical rows found for endpoint {endpoint}")

    subset = subset.dropna(subset=[metric])
    if subset.empty:
        raise ValueError(f"No valid classical values for {endpoint} / {metric}")

    if HIGHER_IS_BETTER[metric]:
        idx = subset[metric].idxmax()
    else:
        idx = subset[metric].idxmin()

    return subset.loc[idx]


def compare_metric(
    classical_value: float,
    multitask_value: float,
    metric: str,
) -> tuple[float, str]:
    delta = float(multitask_value - classical_value)

    if np.isnan(delta):
        return np.nan, "NA"

    if HIGHER_IS_BETTER[metric]:
        if delta > 0:
            verdict = "MULTITASK_WIN"
        elif delta < 0:
            verdict = "CLASSICAL_WIN"
        else:
            verdict = "TIE"
    else:
        # Lower is better for Brier / ECE.
        if delta < 0:
            verdict = "MULTITASK_WIN"
        elif delta > 0:
            verdict = "CLASSICAL_WIN"
        else:
            verdict = "TIE"

    return delta, verdict


def main() -> None:
    classical = pd.read_csv(require_file(CLASSICAL_PATH))
    multitask = pd.read_csv(require_file(MULTITASK_PATH))

    required_classical = {
        "endpoint",
        "model",
        "roc_auc",
        "average_precision",
        "balanced_accuracy",
        "f1",
        "accuracy",
        "brier_score",
    }
    missing = required_classical - set(classical.columns)
    if missing:
        raise ValueError(f"Classical summary missing columns: {sorted(missing)}")

    required_multitask = {
        "endpoint",
        "model",
        "roc_auc",
        "average_precision",
        "balanced_accuracy",
        "f1",
        "accuracy",
        "brier_score",
    }
    missing = required_multitask - set(multitask.columns)
    if missing:
        raise ValueError(f"Multi-task metrics missing columns: {sorted(missing)}")

    metrics = [
        "roc_auc",
        "average_precision",
        "balanced_accuracy",
        "f1",
        "accuracy",
        "brier_score",
    ]

    # Include ECE only if the multi-task output contains it.
    if "ece_10bin" in multitask.columns and "ece_10bin" in classical.columns:
        metrics.append("ece_10bin")

    detail_rows = []

    for mt in multitask.itertuples(index=False):
        endpoint = mt.endpoint

        for metric in metrics:
            classical_best = best_classical_by_metric(classical, endpoint, metric)

            classical_value = float(classical_best[metric])
            multitask_value = float(getattr(mt, metric))

            delta, verdict = compare_metric(
                classical_value,
                multitask_value,
                metric,
            )

            detail_rows.append({
                "endpoint": endpoint,
                "metric": metric,
                "classical_best_model": classical_best["model"],
                "classical_best_value": classical_value,
                "multitask_model": mt.model,
                "multitask_value": multitask_value,
                "delta_multitask_minus_classical": delta,
                "verdict": verdict,
            })

    detail_df = pd.DataFrame(detail_rows)

    # Endpoint-level win counts.
    win_rows = []
    for endpoint, group in detail_df.groupby("endpoint", sort=False):
        win_rows.append({
            "endpoint": endpoint,
            "multitask_wins": int((group["verdict"] == "MULTITASK_WIN").sum()),
            "classical_wins": int((group["verdict"] == "CLASSICAL_WIN").sum()),
            "ties": int((group["verdict"] == "TIE").sum()),
            "metrics_compared": int(len(group)),
        })

    wins_df = pd.DataFrame(win_rows)

    # Compact scientific summary focused on discrimination + imbalance-sensitive metrics.
    summary_rows = []
    for endpoint in multitask["endpoint"].tolist():
        mt_row = multitask[multitask["endpoint"] == endpoint].iloc[0]

        auc_best = best_classical_by_metric(classical, endpoint, "roc_auc")
        ap_best = best_classical_by_metric(classical, endpoint, "average_precision")
        bal_best = best_classical_by_metric(classical, endpoint, "balanced_accuracy")
        brier_best = best_classical_by_metric(classical, endpoint, "brier_score")

        summary_rows.append({
            "endpoint": endpoint,
            "multitask_model": mt_row["model"],
            "multitask_roc_auc": mt_row["roc_auc"],
            "best_classical_roc_auc_model": auc_best["model"],
            "best_classical_roc_auc": auc_best["roc_auc"],
            "delta_roc_auc": mt_row["roc_auc"] - auc_best["roc_auc"],
            "multitask_average_precision": mt_row["average_precision"],
            "best_classical_ap_model": ap_best["model"],
            "best_classical_average_precision": ap_best["average_precision"],
            "delta_average_precision": (
                mt_row["average_precision"] - ap_best["average_precision"]
            ),
            "multitask_balanced_accuracy": mt_row["balanced_accuracy"],
            "best_classical_balanced_accuracy_model": bal_best["model"],
            "best_classical_balanced_accuracy": bal_best["balanced_accuracy"],
            "delta_balanced_accuracy": (
                mt_row["balanced_accuracy"] - bal_best["balanced_accuracy"]
            ),
            "multitask_brier_score": mt_row["brier_score"],
            "best_classical_brier_model": brier_best["model"],
            "best_classical_brier_score": brier_best["brier_score"],
            "delta_brier_score": mt_row["brier_score"] - brier_best["brier_score"],
        })

    summary_df = pd.DataFrame(summary_rows)

    for path in [OUTPUT_DETAIL, OUTPUT_WINS, OUTPUT_SUMMARY]:
        path.parent.mkdir(parents=True, exist_ok=True)

    detail_df.to_csv(OUTPUT_DETAIL, index=False)
    wins_df.to_csv(OUTPUT_WINS, index=False)
    summary_df.to_csv(OUTPUT_SUMMARY, index=False)

    print("\n=== Multi-task vs classical summary ===")
    print(
        summary_df.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\n=== Win counts ===")
    print(wins_df.to_string(index=False))

    print("\nSaved:")
    print(f"  {OUTPUT_DETAIL}")
    print(f"  {OUTPUT_WINS}")
    print(f"  {OUTPUT_SUMMARY}")


if __name__ == "__main__":
    main()
