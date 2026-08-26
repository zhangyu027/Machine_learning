"""Compare all frozen model families across ADMET endpoints.

Inputs
------
reports/cross_endpoint_summary.csv
reports/multitask_admet_metrics.csv
reports/gnn_benchmark.csv

Outputs
-------
reports/all_models_long.csv
reports/all_models_endpoint_summary.csv
reports/all_models_metric_winners.csv
reports/all_models_overall_win_counts.csv

Example
-------
python experiments/compare_all_models.py
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd


CLASSICAL_PATH = Path("reports/cross_endpoint_summary.csv")
MULTITASK_PATH = Path("reports/multitask_admet_metrics.csv")
GNN_PATH = Path("reports/gnn_benchmark.csv")

OUT_LONG = Path("reports/all_models_long.csv")
OUT_ENDPOINT = Path("reports/all_models_endpoint_summary.csv")
OUT_WINNERS = Path("reports/all_models_metric_winners.csv")
OUT_COUNTS = Path("reports/all_models_overall_win_counts.csv")


METRICS = [
    "roc_auc",
    "average_precision",
    "balanced_accuracy",
    "f1",
    "accuracy",
    "brier_score",
]

HIGHER_IS_BETTER = {
    "roc_auc": True,
    "average_precision": True,
    "balanced_accuracy": True,
    "f1": True,
    "accuracy": True,
    "brier_score": False,
}


def require_file(path: Path) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}\n"
            "Run the corresponding frozen experiment before comparing all models."
        )
    return path


def normalize_classical(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["model_family"] = np.where(
        out["model"].str.contains("logistic", case=False, na=False),
        "classical_logistic",
        "classical_random_forest",
    )
    return out


def normalize_multitask(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["model_family"] = "multitask_mlp"
    return out


def normalize_gnn(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["model_family"] = "graphconv_gnn"
    return out


def select_common_columns(df: pd.DataFrame) -> pd.DataFrame:
    base = [
        "endpoint",
        "model_family",
        "model",
        "representation",
        "n_train",
        "n_validation",
        "n_test",
        "accuracy",
        "balanced_accuracy",
        "f1",
        "brier_score",
        "roc_auc",
        "average_precision",
    ]
    present = [c for c in base if c in df.columns]
    return df[present].copy()


def winner_for_metric(group: pd.DataFrame, metric: str) -> pd.Series:
    valid = group.dropna(subset=[metric]).copy()
    if valid.empty:
        raise ValueError(f"No valid values for metric {metric}")

    if HIGHER_IS_BETTER[metric]:
        idx = valid[metric].idxmax()
    else:
        idx = valid[metric].idxmin()

    return valid.loc[idx]


def build_metric_winners(all_models: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for endpoint, group in all_models.groupby("endpoint", sort=False):
        for metric in METRICS:
            winner = winner_for_metric(group, metric)
            rows.append({
                "endpoint": endpoint,
                "metric": metric,
                "winner_model_family": winner["model_family"],
                "winner_model": winner["model"],
                "winner_value": float(winner[metric]),
            })

    return pd.DataFrame(rows)


def build_endpoint_summary(
    all_models: pd.DataFrame,
    winners: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for endpoint, group in all_models.groupby("endpoint", sort=False):
        wg = winners[winners["endpoint"] == endpoint]

        counts = (
            wg["winner_model_family"]
            .value_counts()
            .to_dict()
        )

        best_auc = wg[wg["metric"] == "roc_auc"].iloc[0]
        best_ap = wg[wg["metric"] == "average_precision"].iloc[0]
        best_bal = wg[wg["metric"] == "balanced_accuracy"].iloc[0]
        best_brier = wg[wg["metric"] == "brier_score"].iloc[0]

        rows.append({
            "endpoint": endpoint,
            "best_roc_auc_family": best_auc["winner_model_family"],
            "best_roc_auc_model": best_auc["winner_model"],
            "best_roc_auc": best_auc["winner_value"],
            "best_average_precision_family": best_ap["winner_model_family"],
            "best_average_precision_model": best_ap["winner_model"],
            "best_average_precision": best_ap["winner_value"],
            "best_balanced_accuracy_family": best_bal["winner_model_family"],
            "best_balanced_accuracy_model": best_bal["winner_model"],
            "best_balanced_accuracy": best_bal["winner_value"],
            "best_brier_family": best_brier["winner_model_family"],
            "best_brier_model": best_brier["winner_model"],
            "best_brier_score": best_brier["winner_value"],
            "classical_logistic_wins": int(counts.get("classical_logistic", 0)),
            "classical_random_forest_wins": int(counts.get("classical_random_forest", 0)),
            "multitask_mlp_wins": int(counts.get("multitask_mlp", 0)),
            "graphconv_gnn_wins": int(counts.get("graphconv_gnn", 0)),
            "metrics_compared": int(len(wg)),
        })

    return pd.DataFrame(rows)


def build_overall_win_counts(winners: pd.DataFrame) -> pd.DataFrame:
    counts = (
        winners.groupby("winner_model_family")
        .size()
        .reset_index(name="metric_wins")
        .rename(columns={"winner_model_family": "model_family"})
    )

    counts["fraction_of_all_metric_wins"] = (
        counts["metric_wins"] / len(winners)
    )

    return counts.sort_values(
        ["metric_wins", "model_family"],
        ascending=[False, True],
    ).reset_index(drop=True)


def print_endpoint_leaderboard(all_models: pd.DataFrame) -> None:
    display_cols = [
        "endpoint",
        "model_family",
        "roc_auc",
        "average_precision",
        "balanced_accuracy",
        "f1",
        "brier_score",
    ]

    print("\n=== All-model endpoint leaderboard ===")
    print(
        all_models[display_cols]
        .sort_values(["endpoint", "model_family"])
        .to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )


def main() -> None:
    classical = normalize_classical(
        pd.read_csv(require_file(CLASSICAL_PATH))
    )
    multitask = normalize_multitask(
        pd.read_csv(require_file(MULTITASK_PATH))
    )
    gnn = normalize_gnn(
        pd.read_csv(require_file(GNN_PATH))
    )

    frames = [
        select_common_columns(classical),
        select_common_columns(multitask),
        select_common_columns(gnn),
    ]

    all_models = pd.concat(frames, ignore_index=True)

    # Keep a stable endpoint order if present.
    endpoint_order = ["hERG", "BBBP", "ClinTox", "Tox21"]
    all_models["endpoint"] = pd.Categorical(
        all_models["endpoint"],
        categories=endpoint_order,
        ordered=True,
    )
    all_models = (
        all_models
        .sort_values(["endpoint", "model_family"])
        .reset_index(drop=True)
    )
    all_models["endpoint"] = all_models["endpoint"].astype(str)

    winners = build_metric_winners(all_models)
    endpoint_summary = build_endpoint_summary(all_models, winners)
    overall_counts = build_overall_win_counts(winners)

    for path in [OUT_LONG, OUT_ENDPOINT, OUT_WINNERS, OUT_COUNTS]:
        path.parent.mkdir(parents=True, exist_ok=True)

    all_models.to_csv(OUT_LONG, index=False)
    endpoint_summary.to_csv(OUT_ENDPOINT, index=False)
    winners.to_csv(OUT_WINNERS, index=False)
    overall_counts.to_csv(OUT_COUNTS, index=False)

    print_endpoint_leaderboard(all_models)

    print("\n=== Endpoint summary ===")
    print(
        endpoint_summary.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\n=== Overall metric win counts ===")
    print(
        overall_counts.to_string(
            index=False,
            float_format=lambda x: f"{x:.4f}",
        )
    )

    print("\nSaved:")
    print(f"  {OUT_LONG}")
    print(f"  {OUT_ENDPOINT}")
    print(f"  {OUT_WINNERS}")
    print(f"  {OUT_COUNTS}")


if __name__ == "__main__":
    main()
