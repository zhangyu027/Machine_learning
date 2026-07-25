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
| Multi-task ADMET architecture | Implemented demonstration architecture; endpoint benchmark pending |
| Molecular GNN | Optional architecture; scientific benchmark pending |
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

```bash
cd 04_genai_drug_discovery_v4
conda create -n pharma_v4 python=3.11 -y
conda activate pharma_v4
python -m pip install --upgrade pip
python -m pip install -e .
python -m pytest -q
```

For true scaffold extraction and chemistry-standardized evaluation:

```bash
conda install -c conda-forge rdkit
```

Optional extended stack:

```bash
python -m pip install -r requirements-v4-optional.txt
```

## Run a scientific baseline benchmark

Prepare a versioned CSV containing `smiles` and a binary endpoint column, such as `target`:

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
