# Benchmark Dataset Documentation

This folder should contain separate files for demo molecules and supervised benchmark datasets.

## Keep demo and benchmark data separate

- `demo_smiles.csv` is an unlabeled demonstration dataset for UI and molecule-generation flows.
- Scientific benchmarks require a labeled file with `smiles` and a binary endpoint column such as `target`.

## Recommended local files

| File | Purpose | Commit? |
|---|---|---|
| `demo_smiles.csv` | Unlabeled demo molecules | Yes |
| `bbbp.csv` | BBBP benchmark exported from DeepChem MoleculeNet | Yes if size/license acceptable |
| `clintox.csv` | ClinTox benchmark exported from DeepChem MoleculeNet | Yes if size/license acceptable |
| `tox21_task0.csv` | One selected Tox21 endpoint | Yes if endpoint is documented |
| `demo_benchmark_labeled.csv` | Smoke test only | Optional; do not report as science |

## Dataset source policy

Every benchmark result should document source dataset and version, extraction script or command, target column and endpoint definition, missing-label handling, target distribution, split strategy, evaluation date, and software versions.

## Scientific warning

Do not invent binary labels simply to make a benchmark run. A smoke-test dataset can validate code execution, but it cannot support a scientific performance claim.
