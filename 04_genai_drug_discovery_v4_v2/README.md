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
| Multi-task ADMET architecture | Scientific Morgan-MLP benchmark completed; legacy proxy layer retained for demo compatibility |
| Molecular GNN | GraphConv scientific baseline benchmark completed |
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

`pharma_v4` is a recommended Conda environment name, not a package requirement. Any isolated Python 3.10+ environment can run the project.

```bash
conda create -n pharma_v4 python=3.11 -y
conda activate pharma_v4
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .
```

Confirm that Python and pip refer to the same environment:

```bash
which python
python -c "import sys; print(sys.executable)"
python -m pip --version
```

For RDKit chemistry support:

```bash
conda install -c conda-forge rdkit
```

Optional extended stack:

```bash
python -m pip install -r requirements-v4-optional.txt
```

## Run a scientific baseline benchmark

The benchmark expects a versioned CSV with `smiles` and a binary target column.

### Acquire the TDC hERG dataset without changing the V4 environment

PyTDC is used only for data acquisition and can conflict with newer NLP dependencies. Keep it in a small data-only environment:

```bash
conda create -n tdc_data python=3.10 -y
conda run -n tdc_data python -m pip install "setuptools<81" "PyTDC==1.1.15"
conda run -n tdc_data python data/download_herg_tdc.py \
  --output data/processed/herg.csv
```

Verify:

```bash
python - <<'PY2'
import pandas as pd
df = pd.read_csv("data/processed/herg.csv")
print(df.shape)
print(df.columns.tolist())
print(df["target"].value_counts(dropna=False))
PY2
```

Run the benchmark from the main V4 environment:

```bash
python experiments/run_scientific_benchmark.py \
  --input data/processed/herg.csv \
  --target target \
  --output reports/herg_benchmark.csv
```

The script:

1. builds a scaffold-aware train/validation/test split;
2. verifies that scaffolds do not overlap;
3. compares descriptor logistic regression with a Morgan-fingerprint random forest;
4. reports ROC-AUC, PR-AUC, Brier score, and ECE;
5. writes actual results to a versioned report.

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
# Benchmark module patch

Copy the included `pharma_genai/data` and `pharma_genai/models` folders into the root-level `pharma_genai` package.

Then run:

```bash
pip install -e .
python experiments/run_scientific_benchmark.py \
  --input data/demo_smiles.csv \
  --target target
```

The input CSV must contain both `smiles` and `target`, and `target` must be a binary 0/1 label.
{
  "version": "4.0.0",
  "project_folder": "04_genai_drug_discovery_v4_principal_enterprise",
  "fixed": [
    "Renamed visible V3 titles and headers to V4",
    "Updated Streamlit imports to pipeline_v4",
    "Added pipeline_v4 public wrapper",
    "Kept pipeline_v3 only for backward compatibility",
    "Removed stale egg-info and __pycache__",
    "Removed active rdkit-pypi packaging dependency",
    "Added V4 install/run notes",
    "Added FastAPI root route where possible"
  ],
  "run_streamlit": "PYTHONPATH=. streamlit run app/streamlit_app.py",
  "run_api": "PYTHONPATH=. uvicorn pharma_genai.api:app --reload",
  "test": "pytest -q"
}

## V4.1 completed scientific benchmark

The V4.1 experimental phase is complete for **hERG, BBBP, ClinTox, and Tox21**.
All model families were evaluated with the same scaffold-aware scientific framing.

### Final model-family comparison

| Endpoint | Best ROC-AUC | Best average precision | Best balanced accuracy | Best Brier score |
|---|---|---|---|---|
| hERG | RF Morgan — 0.8856 | RF Morgan — 0.9183 | Logistic/RDKit — 0.7949 | Logistic/RDKit — 0.1509 |
| BBBP | Logistic/RDKit — 0.8731 | Logistic/RDKit — 0.9387 | Logistic/RDKit — 0.8367 | RF Morgan — 0.1290 |
| ClinTox | RF Morgan — 0.9375 | RF Morgan — 0.9982* | Logistic/RDKit — 0.8715 | RF Morgan — 0.0263 |
| Tox21 | Logistic/RDKit — 0.7124 | **Multi-task Morgan MLP — 0.3153** | RF Morgan — 0.6472 | RF Morgan — 0.0143 |

\* ClinTox AP must be interpreted with its extreme test prevalence (144 positive,
4 negative).

Across the 24 endpoint × metric winner comparisons used in the frozen final
comparison, classical models won **23/24**: random forest won 13, logistic
regression won 10, and the multi-task MLP won one. The simple GraphConv GNN won
none.

The scientifically important conclusion is **not** that neural models are
intrinsically worse. Rather, increased architectural complexity did not
automatically improve scaffold-held-out generalization in this benchmark.
Multi-task learning showed a targeted benefit for rare-positive Tox21 retrieval.

### Class-prevalence audit

| Endpoint | Overall positive rate | Train | Validation | Test |
|---|---:|---:|---:|---:|
| hERG | 68.66% | 70.25% | 64.62% | 60.00% |
| BBBP | 76.51% | 77.01% | 75.49% | 73.53% |
| ClinTox | 93.65% | 93.07% | 94.59% | 97.30% |
| Tox21 | 4.24% | 4.84% | 2.34% | 1.38% |

This audit is required context for interpreting ClinTox and Tox21. Raw accuracy
alone is not a suitable headline metric under these distributions.

### Frozen experiment sequence

```text
run_scientific_benchmark.py
        ↓
compare_endpoints.py
        ↓
audit_endpoint_labels.py
        ↓
run_multitask_admet.py
        ↓
compare_multitask_vs_classical.py
        ↓
run_gnn_benchmark.py
        ↓
compare_all_models.py
```

The benchmark scripts are retained as historical/reproducible experiment
orchestration. Reusable V4.1 scientific model definitions are also exposed under
`pharma_genai.models`.

## Current limitations and next validation step

V4.1 remains a research/portfolio prototype. The benchmark does not yet include
independent external validation, temporal validation, prospective experimental
confirmation, medicinal-chemistry sign-off, or regulatory/clinical validation.

The next scientifically defensible milestone is **external or temporal
validation and endpoint-specific error/chemotype analysis**, not additional
test-driven tuning of the frozen V4.1 models.

See:

- `docs/01_scientific/SCIENTIFIC_METHODOLOGY.md`
- `docs/01_scientific/LIMITATIONS.md`
- `reports/README.md`
