"""Cross-endpoint comparison and reporting for V4.1 scientific benchmarks.

Reads frozen benchmark outputs for hERG, BBBP, ClinTox, and Tox21, then writes:
- reports/cross_endpoint_summary.csv
- reports/cross_endpoint_reliability.csv
- reports/cross_endpoint_domain_performance.csv
- reports/cross_endpoint_best_models.csv

Example:
    python experiments/compare_endpoints.py
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd
import numpy as np


ENDPOINTS = {
    "hERG": {
        "benchmark": "reports/herg_benchmark.csv",
        "reliability": "reports/herg_details/reliability_comparison.csv",
        "domain": "reports/herg_details/domain_performance.csv",
    },
    "BBBP": {
        "benchmark": "reports/bbbp_benchmark.csv",
        "reliability": "reports/bbbp_details/reliability_comparison.csv",
        "domain": "reports/bbbp_details/domain_performance.csv",
    },
    "ClinTox": {
        "benchmark": "reports/clintox_benchmark.csv",
        "reliability": "reports/clintox_details/reliability_comparison.csv",
        "domain": "reports/clintox_details/domain_performance.csv",
    },
    "Tox21": {
        "benchmark": "reports/tox21_benchmark.csv",
        "reliability": "reports/tox21_details/reliability_comparison.csv",
        "domain": "reports/tox21_details/domain_performance.csv",
    },
}


def require_file(path: str) -> Path:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"Required file not found: {p}\n"
            "Run the frozen scientific benchmark for this endpoint first."
        )
    return p


def load_benchmarks() -> pd.DataFrame:
    frames = []
    for endpoint, paths in ENDPOINTS.items():
        df = pd.read_csv(require_file(paths["benchmark"]))
        df.insert(0, "endpoint", endpoint)

        if "n_test" in df.columns:
            df["ad_in_domain_fraction"] = df["ad_in_domain"] / df["n_test"]
            df["ad_borderline_fraction"] = df["ad_borderline"] / df["n_test"]
            df["ad_out_of_domain_fraction"] = df["ad_out_of_domain"] / df["n_test"]

        frames.append(df)

    return pd.concat(frames, ignore_index=True)


def load_reliability() -> pd.DataFrame:
    frames = []
    for endpoint, paths in ENDPOINTS.items():
        df = pd.read_csv(require_file(paths["reliability"]))
        df.insert(0, "endpoint", endpoint)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def load_domain_performance() -> pd.DataFrame:
    frames = []
    for endpoint, paths in ENDPOINTS.items():
        df = pd.read_csv(require_file(paths["domain"]))
        df.insert(0, "endpoint", endpoint)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def choose_best_models(bench: pd.DataFrame) -> pd.DataFrame:
    """Create an endpoint-level model-selection summary without hiding tradeoffs."""
    rows = []

    for endpoint, group in bench.groupby("endpoint", sort=False):
        group = group.copy()

        best_auc = group.loc[group["roc_auc"].idxmax()]
        best_ap = group.loc[group["average_precision"].idxmax()]
        best_bal = group.loc[group["balanced_accuracy"].idxmax()]
        best_brier = group.loc[group["brier_score"].idxmin()]
        best_ece = group.loc[group["ece_10bin"].idxmin()]

        rows.append({
            "endpoint": endpoint,
            "best_roc_auc_model": best_auc["model"],
            "best_roc_auc": best_auc["roc_auc"],
            "best_average_precision_model": best_ap["model"],
            "best_average_precision": best_ap["average_precision"],
            "best_balanced_accuracy_model": best_bal["model"],
            "best_balanced_accuracy": best_bal["balanced_accuracy"],
            "best_brier_model": best_brier["model"],
            "best_brier_score": best_brier["brier_score"],
            "best_ece_model": best_ece["model"],
            "best_ece_10bin": best_ece["ece_10bin"],
            "model_tradeoff_present": len({
                best_auc["model"],
                best_ap["model"],
                best_bal["model"],
                best_brier["model"],
                best_ece["model"],
            }) > 1,
        })

    return pd.DataFrame(rows)


def reliability_model_summary(rel: pd.DataFrame) -> pd.DataFrame:
    """Summarize reliability groups for direct model comparison."""
    pivot = rel.pivot_table(
        index=["endpoint", "model"],
        columns="reliability_label",
        values=["n", "fraction_of_test", "accuracy", "mean_uncertainty"],
        aggfunc="first",
    )

    pivot.columns = [
        f"{metric}_{label.lower()}"
        for metric, label in pivot.columns
    ]
    return pivot.reset_index()


def print_compact_summary(bench: pd.DataFrame, best: pd.DataFrame) -> None:
    cols = [
        "endpoint",
        "model",
        "roc_auc",
        "average_precision",
        "balanced_accuracy",
        "brier_score",
        "ece_10bin",
        "ad_out_of_domain_fraction",
    ]
    print("\n=== Cross-endpoint benchmark ===")
    print(
        bench[cols]
        .sort_values(["endpoint", "model"])
        .to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )

    print("\n=== Endpoint-level best metrics ===")
    print(
        best.to_string(index=False, float_format=lambda x: f"{x:.4f}")
    )


def main() -> None:
    reports = Path("reports")
    reports.mkdir(parents=True, exist_ok=True)

    bench = load_benchmarks()
    rel = load_reliability()
    domain = load_domain_performance()

    best = choose_best_models(bench)
    rel_summary = reliability_model_summary(rel)

    bench.to_csv(reports / "cross_endpoint_summary.csv", index=False)
    rel.to_csv(reports / "cross_endpoint_reliability.csv", index=False)
    domain.to_csv(reports / "cross_endpoint_domain_performance.csv", index=False)
    best.to_csv(reports / "cross_endpoint_best_models.csv", index=False)
    rel_summary.to_csv(reports / "cross_endpoint_reliability_summary.csv", index=False)

    print_compact_summary(bench, best)

    print("\nSaved:")
    print("  reports/cross_endpoint_summary.csv")
    print("  reports/cross_endpoint_reliability.csv")
    print("  reports/cross_endpoint_domain_performance.csv")
    print("  reports/cross_endpoint_best_models.csv")
    print("  reports/cross_endpoint_reliability_summary.csv")


if __name__ == "__main__":
    main()
