# Scientific ML Drug Discovery Platform V4.1

An end-to-end molecular AI platform for **compound representation, scaffold-aware ADMET benchmarking, uncertainty-aware candidate prioritization, explainability, evidence retrieval, and reproducible ML deployment**.

> **Scientific disclaimer:** This is a portfolio and decision-support research prototype. It is not a validated medicinal-chemistry, clinical, regulatory, or production system. Proxy predictions and example outputs must not be interpreted as experimental evidence.

## Scientific question

> **Can uncertainty-aware multi-task molecular machine learning improve the reliability of early-stage ADMET candidate prioritization compared with classical single-task baselines?**

The repository is organized around that question rather than around a collection of unrelated technologies.

## Scientific workflow

```text
Public molecular data
        ↓
SMILES validation and standardization
        ↓
RDKit descriptors / Morgan fingerprints / molecular graphs
        ↓
Bemis–Murcko scaffold-aware splitting
        ↓
Classical baselines → multi-task models → GNN models
        ↓
Discrimination / error metrics + calibration + confidence intervals
        ↓
Uncertainty + applicability-domain analysis
        ↓
Explainability and error analysis
        ↓
Transparent multi-objective candidate prioritization
        ↓
Citation-backed literature evidence
        ↓
Scientist review
```

## What changed in V4.1

V4.1 shifts the project from a broad enterprise-architecture demonstration toward a scientifically defensible experimental framework.

### Implemented in this upgrade

- Leakage-aware **Bemis–Murcko scaffold splitting** when RDKit is installed
- Deterministic fallback grouping for base software tests, clearly marked as non-scientific
- Descriptor and Morgan-fingerprint classical baselines
- ROC-AUC, PR-AUC, Brier score, and expected calibration error
- Bootstrap confidence-interval utility
- Nearest-neighbor **Tanimoto applicability domain**
- In-domain, borderline, and out-of-domain reliability categories
- Transparent candidate priority score incorporating utility, uncertainty, OOD risk, and toxicity
- Evidence-support interface that separates predictions from literature evidence
- `DATA_CARD.md`, `MODEL_CARD.md`, and `EXPERIMENT_REPORT.md`
- Versioned benchmark-table template that intentionally contains no invented metrics
- New tests for scaffold leakage, calibration, applicability domain, and prioritization

### Existing V4 capabilities retained

- Molecular descriptor and fingerprint featurization
- Multi-task ADMET/toxicity demonstration layer
- GNN-ready optional PyTorch Geometric module
- SHAP-ready explainability components
- Public chemistry connector patterns
- PubMed-style retrieval components
- FastAPI and Streamlit interfaces
- Docker, MLflow-ready tracking, and GitHub Actions patterns

## Honest maturity statement

| Capability | Current maturity |
|---|---|
| Molecular validation and featurization | Implemented; RDKit optional |
| Classical baseline framework | Implemented |
| Scaffold-aware split | Implemented; RDKit required for true Bemis–Murcko scaffolds |
| Multi-task ADMET architecture | Benchmarked on hERG, BBBP, ClinTox, and Tox21 |
| Molecular GNN | GraphConv benchmark completed on hERG, BBBP, ClinTox, and Tox21 |
| Calibration metrics | Implemented |
| Bootstrap confidence intervals | Implemented |
| Applicability domain | Implemented |
| Candidate prioritization | Implemented as configurable decision-support logic |
| SHAP explainability | Optional/ready; endpoint analysis pending |
| Literature evidence support | Implemented interface/pattern; not scientific validation |
| External or temporal validation | Pending selected versioned dataset |

## Repository map

```text
pharma_genai/
├── data/
│   └── scaffold_split.py
├── representations/
├── models/
│   └── classical_baselines.py
├── evaluation/
│   ├── metrics.py
│   ├── calibration.py
│   ├── bootstrap_ci.py
│   └── applicability_domain.py
├── prioritization/
│   └── candidate_ranking.py
├── evidence/
│   └── literature_retrieval.py
├── gnn/
├── explainability/
├── rag/
├── api/
└── mlops/

experiments/
└── run_scientific_benchmark.py

reports/
└── benchmark_table.csv
```

## Installation

V4.1 does **not** require a Conda environment with a specific name. `pharma_v4` is only the recommended local environment name. The important requirement is to use one consistent Python interpreter and install the project dependencies into that interpreter.

```bash
cd 04_genai_drug_discovery_v4_v2_patched
conda create -n pharma_v4 python=3.11 -y
conda activate pharma_v4
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Verify the interpreter before installing packages:

```bash
which python
python -c "import sys; print(sys.executable)"
python -m pip --version
```

On macOS, prefer `python -m pip` over plain `pip` so packages are installed into the active interpreter rather than an unrelated Homebrew Python.

For true Bemis–Murcko scaffold extraction:

```bash
conda install -c conda-forge rdkit
```

Optional extended stack:

```bash
python -m pip install -r requirements-v4-optional.txt
```

## Download the hERG benchmark dataset

The repository does not ship a fabricated `herg.csv`. The hERG benchmark should be created reproducibly from Therapeutics Data Commons (TDC). To avoid PyTDC dependency conflicts with the main V4 NLP/ML stack, use a small separate environment only for data acquisition.

Create it once:

```bash
conda create -n tdc_data python=3.10 -y
conda run -n tdc_data python -m pip install "setuptools<81" "PyTDC==1.1.15"
```

From the project root, confirm that the downloader exists:

```bash
ls -l data/download_herg_tdc.py
```

Then download and normalize hERG:

```bash
conda run -n tdc_data python data/download_herg_tdc.py \
  --output data/processed/herg.csv
```

Verify the generated dataset:

```bash
ls -lh data/processed/herg.csv
python - <<'PY'
import pandas as pd
df = pd.read_csv("data/processed/herg.csv")
print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.head())
print("target distribution:")
print(df["target"].value_counts(dropna=False))
PY
```

The normalized benchmark file must contain at least `smiles` and binary `target` columns.

## Run the hERG scientific benchmark

Return to the main project environment:

```bash
conda activate pharma_v4
```

Run:

```bash
python experiments/run_scientific_benchmark.py \
  --input data/processed/herg.csv \
  --target target \
  --output reports/herg_benchmark.csv
```

```
experiments/run_scientific_benchmark.py
```
python experiments/run_scientific_benchmark.py \
  --input data/processed/herg.csv \
  --target target \
  --output reports/herg_benchmark.csv
```

```
python experiments/run_scientific_benchmark.py \
  --input data/BBBP/bbbp.csv \
  --target target \
  --output reports/bbbp_benchmark.csv \
  --details-dir reports/bbbp_details
```


```
python experiments/run_scientific_benchmark.py \
  --input data/ClinTox/clintox.csv \
  --target target \
  --output reports/clintox_benchmark.csv \
  --details-dir reports/clintox_details
```

```
python experiments/run_scientific_benchmark.py \
  --input data/Tox21/tox21_task0.csv \
  --target target \
  --output reports/tox21_benchmark.csv \
  --details-dir reports/tox21_details
```


                 FROZEN V4.1 BENCHMARK PROTOCOL
                           │
          ┌────────────────┼────────────────┐
          ↓                ↓                ↓
        hERG             BBBP           ClinTox          Tox21
          │                │                │               │
          └────────────────┴────────┬───────┴───────────────┘
                                   ↓
                       Cross-endpoint comparison
                                   ↓
                         Multi-task ADMET model
                                   ↓
                              GNN model
                                   ↓
                 Classical vs Multi-task vs GNN

The benchmark:

1. builds a scaffold-aware train/validation/test split;
2. verifies that scaffolds do not overlap;
3. compares descriptor logistic regression with a Morgan-fingerprint random forest;
4. reports ROC-AUC, PR-AUC, Brier score, and ECE;
5. writes actual results to a versioned report.

After the run, inspect the result:

```bash
cat reports/herg_benchmark.csv
```

### Next validation steps

The V4.1 benchmark sequence has now been completed for hERG, BBBP, ClinTox, and Tox21, including bootstrap confidence intervals, calibration/applicability-domain analysis, label-prevalence auditing, multi-task comparison, and a GraphConv GNN benchmark. Future validation should focus on external or temporal datasets, richer graph architectures only when scientifically motivated, and endpoint-specific error analysis. Only experimentally generated metrics should be promoted into this README or the portfolio report.

## V4.1 benchmark results

The frozen V4.1 protocol compared endpoint-specific classical baselines, a shared multi-task Morgan-fingerprint MLP, and a GraphConv molecular GNN under scaffold-held-out evaluation. The main result is that increased model complexity did **not** consistently improve generalization. Across 24 endpoint × metric comparisons (ROC-AUC, average precision, balanced accuracy, F1, accuracy, and Brier score), classical models won 23 comparisons: random forest won 13, logistic regression won 10, the multi-task MLP won 1, and GraphConv won 0.

### Best model by endpoint and metric

| Endpoint | Best ROC-AUC | Best AP | Best balanced accuracy | Best Brier score ↓ |
|---|---:|---:|---:|---:|
| hERG | Random Forest — **0.886** | Random Forest — **0.918** | Logistic — **0.795** | Logistic — **0.151** |
| BBBP | Logistic — **0.873** | Logistic — **0.939** | Logistic — **0.837** | Random Forest — **0.129** |
| ClinTox | Random Forest — **0.938** | Random Forest — **0.998** | Logistic — **0.872** | Random Forest — **0.026** |
| Tox21 | Logistic — **0.712** | Multi-task MLP — **0.315** | Random Forest — **0.647** | Random Forest — **0.014** |

### Interpretation

- **hERG:** Random forest provided the strongest discrimination, while descriptor logistic regression provided stronger balanced accuracy and probability error, demonstrating a discrimination-versus-calibration/classification tradeoff.
- **BBBP:** Descriptor logistic regression was the strongest discriminator and balanced classifier; random forest produced the lowest Brier score.
- **ClinTox:** The test split was extremely positive-heavy (144 positive, 4 negative; 97.3% positive). Therefore accuracy, F1, and especially very high AP must be interpreted alongside balanced accuracy and prevalence.
- **Tox21:** The test split was extremely negative-heavy (10 positive, 716 negative; 1.38% positive). The multi-task MLP produced the only overall multi-task win, increasing AP to **0.315** versus the best classical AP of **0.260**, suggesting possible positive transfer for rare-event retrieval.
- **GraphConv GNN:** The simple GNN did not win any of the 24 endpoint × metric comparisons. This is retained as a scientifically useful negative result: greater architectural complexity did not automatically improve scaffold-held-out generalization.

### Label prevalence and scaffold-shift audit

| Endpoint | Overall positive rate | Train | Validation | Test |
|---|---:|---:|---:|---:|
| hERG | 68.66% | 70.25% | 64.62% | 60.00% |
| BBBP | 76.51% | 77.01% | 75.49% | 73.53% |
| ClinTox | 93.65% | 93.07% | 94.59% | 97.30% |
| Tox21 | 4.24% | 4.84% | 2.34% | 1.38% |

The scaffold split therefore tests more than random holdout performance: for some endpoints it also introduces meaningful chemical and label-prevalence shift. For this reason, raw accuracy is not treated as the primary model-selection metric for highly imbalanced ClinTox or Tox21.

### Scientific conclusion

Under this V4.1 scaffold-held-out benchmark, endpoint-specific classical models generally provided the strongest discrimination, balanced classification, and probability quality. Multi-task learning did not improve all endpoints, but it produced a targeted improvement in average precision for the sparse-positive Tox21 task. The simple GraphConv baseline did not outperform the strongest classical models. These results support the project's central principle: model complexity should be justified by reproducible out-of-scaffold evidence rather than assumed to be beneficial.

The benchmark results are research/portfolio evidence only and should not be interpreted as experimental, clinical, medicinal-chemistry, or regulatory validation.

## Endpoint plan

The multi-task framework is intended to support explicit, measurable endpoints rather than the vague claim that it “predicts ADMET.” Candidate endpoints include:

- **Absorption:** solubility, permeability
- **Distribution:** BBB penetration, plasma-protein binding
- **Metabolism:** CYP inhibition endpoints
- **Excretion:** clearance endpoints
- **Toxicity:** hERG, hepatotoxicity, Ames mutagenicity

Each endpoint report should include dataset size, prevalence or target distribution, missing labels, assay definition, split strategy, baseline and final model, appropriate metrics, calibration, confidence intervals, applicability domain, and limitations.

## Candidate prioritization—not automated scientific decisions

The platform separates prediction from prioritization:

```text
Molecule → chemistry checks → endpoint predictions → calibration
→ uncertainty → applicability domain → multi-objective ranking
→ literature evidence → scientist review
```

A high predicted score is not treated as a validated drug candidate. The ranking layer can penalize uncertainty, out-of-domain chemistry, and toxicity risk. Out-of-domain candidates are routed to **REVIEW**, not automatically advanced.

## Evidence retrieval—not a chatbot claim

Literature retrieval is used to provide citation-backed evidence associated with a target, compound class, mechanism, or predicted liability. Model predictions and retrieved publications remain explicitly separate. Retrieved literature does not validate a model prediction.

## Streamlit, CLI, and API

```bash
streamlit run app/streamlit_app.py
python -m pharma_genai.cli_v4 --smiles "CCO" "CC(=O)Oc1ccccc1C(=O)O" --literature
uvicorn pharma_genai.api.service:app --reload --port 8000
```

## Interview positioning

> I developed an evolving Scientific ML Drug Discovery Platform. V2 established molecular data processing, RDKit-style features, ADMET/toxicity prediction, and reliability scoring. V3 expanded toward multi-task learning, molecular graphs, uncertainty, explainability, APIs, and MLOps. V4.1 integrates those components into a scientifically stronger workflow centered on scaffold-aware validation, honest baseline comparison, calibration, confidence intervals, applicability-domain analysis, uncertainty-aware candidate ranking, and evidence-supported scientist review.

The central lesson is transferable to clinical AI: **the model is not the final decision**. Scientific value comes from leakage-safe evaluation, reproducibility, calibration, uncertainty, domain-of-validity checks, explainability, and clear limitations.

## Evidence policy

No performance result should be promoted to the main README unless it is generated from a versioned dataset through a reproducible experiment. Planned features must be labeled as planned; optional architectures must not be described as validated models.
