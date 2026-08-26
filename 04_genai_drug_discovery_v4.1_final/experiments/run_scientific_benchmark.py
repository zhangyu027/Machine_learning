"""Run a reproducible baseline benchmark on a CSV with columns: smiles,target.

Example:
    python experiments/run_scientific_benchmark.py --input data/processed/herg.csv --target target
"""
from __future__ import annotations
import argparse, json
from pathlib import Path
import pandas as pd
from pharma_genai.data.scaffold_split import scaffold_split_indices, assert_no_scaffold_overlap
from pharma_genai.models.classical_baselines import build_baselines, descriptor_matrix, fingerprint_matrix, classification_metrics
from sklearn.metrics import roc_auc_score, average_precision_score
import numpy as np
from pharma_genai.evaluation.calibration import expected_calibration_error, reliability_table
from pharma_genai.evaluation.applicability_domain import ApplicabilityDomain


def bootstrap_ci(y_true, y_prob, metric_fn, n_bootstrap=2000, confidence=0.95, seed=42):
    """Return a stratified bootstrap confidence interval for a binary metric."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    rng = np.random.default_rng(seed)

    pos = np.flatnonzero(y_true == 1)
    neg = np.flatnonzero(y_true == 0)
    scores = []

    for _ in range(n_bootstrap):
        sample_pos = rng.choice(pos, size=len(pos), replace=True)
        sample_neg = rng.choice(neg, size=len(neg), replace=True)
        idx = np.concatenate([sample_pos, sample_neg])
        scores.append(metric_fn(y_true[idx], y_prob[idx]))

    alpha = (1.0 - confidence) / 2.0
    return (
        float(np.quantile(scores, alpha)),
        float(np.quantile(scores, 1.0 - alpha)),
    )


def prediction_uncertainty(prob):
    """Binary predictive uncertainty scaled to [0, 1]; 1 is maximally uncertain."""
    prob = np.asarray(prob, dtype=float)
    return 1.0 - np.abs(prob - 0.5) * 2.0


def reliability_label(prob, applicability_label):
    """Combine probability margin and chemical applicability domain into a review label."""
    u = float(prediction_uncertainty([prob])[0])

    # Out-of-domain chemistry is always routed to review regardless of probability.
    if applicability_label == "out_of_domain":
        return "REVIEW"

    # Near the decision boundary -> low reliability.
    if u >= 0.70:
        return "LOW"

    # Strong probability margin + chemically in-domain -> high reliability.
    if applicability_label == "in_domain" and u <= 0.30:
        return "HIGH"

    return "MEDIUM"


def safe_group_metrics(y_true, y_prob):
    """Metrics for a subset; ROC-AUC/AP are omitted when not statistically defined."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)

    if len(y_true) == 0:
        return {
            "n": 0,
            "accuracy": np.nan,
            "roc_auc": np.nan,
            "average_precision": np.nan,
        }

    pred = (y_prob >= 0.5).astype(int)
    accuracy = float((pred == y_true).mean())

    if len(np.unique(y_true)) < 2:
        roc_auc = np.nan
        average_precision = np.nan
    else:
        roc_auc = float(roc_auc_score(y_true, y_prob))
        average_precision = float(average_precision_score(y_true, y_prob))

    return {
        "n": int(len(y_true)),
        "accuracy": accuracy,
        "roc_auc": roc_auc,
        "average_precision": average_precision,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--target", default="target")
    p.add_argument("--output", default="reports/benchmark_table.csv")
    p.add_argument("--details-dir", default="reports/benchmark_details")
    args = p.parse_args()
    df = pd.read_csv(args.input).dropna(subset=["smiles", args.target]).reset_index(drop=True)
    smiles = df["smiles"].astype(str).tolist(); y = df[args.target].astype(int).to_numpy()
    tr, va, te = scaffold_split_indices(smiles); assert_no_scaffold_overlap(smiles, [tr, va, te])
    models = build_baselines(); rows = []; domain_rows = []; reliability_rows = []
    details_dir = Path(args.details_dir)
    details_dir.mkdir(parents=True, exist_ok=True)
    ad = ApplicabilityDomain([smiles[i] for i in tr], n_bits=256)
    feature_sets = {"logistic_rdkit_descriptors": descriptor_matrix(smiles), "random_forest_morgan": fingerprint_matrix(smiles)}
    for name, model in models.items():
        X = feature_sets[name]; model.fit(X[tr], y[tr]); prob = model.predict_proba(X[te])[:, 1]
        metrics = classification_metrics(y[te], prob)
        ece = expected_calibration_error(y[te], prob, n_bins=10)

        roc_low, roc_high = bootstrap_ci(
            y[te], prob, roc_auc_score, n_bootstrap=2000, seed=42
        )
        ap_low, ap_high = bootstrap_ci(
            y[te], prob, average_precision_score, n_bootstrap=2000, seed=43
        )

        # Save reliability/calibration bins for plotting and inspection.
        pd.DataFrame(reliability_table(y[te], prob, n_bins=10)).to_csv(
            details_dir / f"{name}_calibration.csv", index=False
        )

        # Assess chemical applicability domain for every held-out test molecule.
        ad_results = [ad.assess(smiles[i]) for i in te]
        detail_df = pd.DataFrame({
            "smiles": [smiles[i] for i in te],
            "y_true": y[te],
            "y_prob": prob,
            "predicted_label": (prob >= 0.5).astype(int),
            "prediction_uncertainty": prediction_uncertainty(prob),
            "nearest_similarity": [r.nearest_similarity for r in ad_results],
            "applicability_label": [r.label for r in ad_results],
            "nearest_training_smiles": [r.nearest_training_smiles for r in ad_results],
        })

        detail_df["reliability_label"] = [
            reliability_label(p, a)
            for p, a in zip(detail_df["y_prob"], detail_df["applicability_label"])
        ]
        detail_df["correct"] = (
            detail_df["predicted_label"] == detail_df["y_true"]
        ).astype(int)

        detail_df.to_csv(details_dir / f"{name}_test_predictions.csv", index=False)

        # Performance by chemical applicability-domain group.
        for domain_name in ["in_domain", "borderline", "out_of_domain"]:
            sub = detail_df[detail_df["applicability_label"] == domain_name]
            gm = safe_group_metrics(sub["y_true"].to_numpy(), sub["y_prob"].to_numpy())
            domain_rows.append({
                "model": name,
                "applicability_label": domain_name,
                **gm,
                "mean_uncertainty": float(sub["prediction_uncertainty"].mean()) if len(sub) else np.nan,
                "mean_nearest_tanimoto": float(sub["nearest_similarity"].mean()) if len(sub) else np.nan,
            })

        # Reliability summary supports direct Logistic-vs-RF comparison.
        for rel in ["HIGH", "MEDIUM", "LOW", "REVIEW"]:
            sub = detail_df[detail_df["reliability_label"] == rel]
            reliability_rows.append({
                "model": name,
                "reliability_label": rel,
                "n": int(len(sub)),
                "fraction_of_test": float(len(sub) / len(detail_df)),
                "accuracy": float(sub["correct"].mean()) if len(sub) else np.nan,
                "mean_uncertainty": float(sub["prediction_uncertainty"].mean()) if len(sub) else np.nan,
                "mean_probability": float(sub["y_prob"].mean()) if len(sub) else np.nan,
                "mean_nearest_tanimoto": float(sub["nearest_similarity"].mean()) if len(sub) else np.nan,
            })

        label_counts = detail_df["applicability_label"].value_counts()
        n_in = int(label_counts.get("in_domain", 0))
        n_border = int(label_counts.get("borderline", 0))
        n_ood = int(label_counts.get("out_of_domain", 0))

        rows.append({
            "model": name,
            "representation": "descriptors" if "descriptor" in name else "morgan_256",
            "split": "bemis_murcko_scaffold",
            "n_train": len(tr),
            "n_validation": len(va),
            "n_test": len(te),
            **metrics,
            "ece_10bin": ece,
            "roc_auc_ci95_low": roc_low,
            "roc_auc_ci95_high": roc_high,
            "average_precision_ci95_low": ap_low,
            "average_precision_ci95_high": ap_high,
            "ad_in_domain": n_in,
            "ad_borderline": n_border,
            "ad_out_of_domain": n_ood,
            "mean_nearest_tanimoto": float(detail_df["nearest_similarity"].mean()),
        })
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)

    domain_df = pd.DataFrame(domain_rows)
    reliability_df = pd.DataFrame(reliability_rows)

    domain_out = details_dir / "domain_performance.csv"
    reliability_out = details_dir / "reliability_comparison.csv"

    domain_df.to_csv(domain_out, index=False)
    reliability_df.to_csv(reliability_out, index=False)

    print(json.dumps(rows, indent=2))
    print(f"\nSaved benchmark: {out}")
    print(f"Saved domain performance: {domain_out}")
    print(f"Saved reliability comparison: {reliability_out}")

if __name__ == "__main__":
    main()
