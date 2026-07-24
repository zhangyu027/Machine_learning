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


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True)
    p.add_argument("--target", default="target")
    p.add_argument("--output", default="reports/benchmark_table.csv")
    args = p.parse_args()
    df = pd.read_csv(args.input).dropna(subset=["smiles", args.target]).reset_index(drop=True)
    smiles = df["smiles"].astype(str).tolist(); y = df[args.target].astype(int).to_numpy()
    tr, va, te = scaffold_split_indices(smiles); assert_no_scaffold_overlap(smiles, [tr, va, te])
    models = build_baselines(); rows = []
    feature_sets = {"logistic_rdkit_descriptors": descriptor_matrix(smiles), "random_forest_morgan": fingerprint_matrix(smiles)}
    for name, model in models.items():
        X = feature_sets[name]; model.fit(X[tr], y[tr]); prob = model.predict_proba(X[te])[:, 1]
        metrics = classification_metrics(y[te], prob)
        rows.append({"model": name, "representation": "descriptors" if "descriptor" in name else "morgan_256", "split": "bemis_murcko_scaffold", "n_train": len(tr), "n_validation": len(va), "n_test": len(te), **metrics})
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out, index=False)
    print(json.dumps(rows, indent=2))

if __name__ == "__main__":
    main()
