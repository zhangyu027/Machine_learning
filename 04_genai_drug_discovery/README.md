# Generative AI Drug Discovery — Pharmaceutical ML V2.1

Portfolio-ready pharmaceutical machine learning package for small-molecule drug discovery. This version adds ADMET prediction, molecular property prediction, toxicity screening, RDKit-style feature engineering, reliability scoring, Wenkel Liang–style uncertainty estimation, CLI tools, tests, and a Streamlit UI.

## What This Package Includes

- **ADMET prediction**: oral absorption, solubility risk, BBB penetration, CYP inhibition risk.
- **Molecular property prediction**: molecular weight, LogP, TPSA, HBD/HBA, rotatable bonds, QED-like drug-likeness, ring count, fraction CSP3.
- **Toxicity prediction**: hERG risk, hepatotoxicity risk, AMES-like mutagenicity proxy, and combined toxicity risk.
- **RDKit feature engineering**: uses RDKit when available; includes a lightweight fallback so the project can run for demo/portfolio use without RDKit.
- **Reliability scoring**: uncertainty, applicability domain, model-agreement proxy, and beta-binomial style confidence communication.
- **Streamlit UI**: interactive molecule scoring and candidate ranking.
- **Portfolio documentation**: model card, project brief, examples, tests, and CLI.

---

## Recommended Setup on Mac / Conda

From the project root folder:

```bash
cd /Users/yuzhang/projects/Machine_learning/04_genai_drug_discovery_v2_pharma_grade
```

Create and activate a clean conda environment:

```bash
conda create -n pharma_v2 python=3.11 -y
conda activate pharma_v2
```

Install the package and dependencies into the active conda environment:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip install pytest streamlit
```

Why use `python -m pip`? It guarantees packages are installed into the currently active `pharma_v2` Python environment.

Your terminal prompt should show only:

```text
(pharma_v2)
```

Avoid running with both environments active, for example:

```text
(pharma_v2) (venv)
```

If you see `(venv)`, deactivate or remove the local venv before continuing.

---

## Run Tests

Use:

```bash
python -m pytest
```

Optional shorter version:

```bash
python -m pytest -q
```

Expected result:

```text
passed
```

---

## Launch Streamlit UI

The Streamlit app is located at:

```text
app/streamlit_app.py
```

Run:

```bash
streamlit run app/streamlit_app.py
```

Then open the local browser URL shown by Streamlit, usually:

```text
http://localhost:8501
```

---

## Command Line Usage

Score one molecule:

```bash
python -m pharma_genai.cli score "CC(=O)Oc1ccccc1C(=O)O"
```

Score a CSV file:

```bash
python -m pharma_genai.cli batch examples/example_smiles.csv --output outputs/admet_v2_predictions.csv
```

Example molecules:

```text
CCO
```

Ethanol

```text
CC(=O)OC1=CC=CC=C1C(=O)O
```

Aspirin

```text
CN1C=NC2=C1C(=O)N(C(=O)N2C)C
```

Caffeine

---

## Project Structure

```text
04_genai_drug_discovery_v2_pharma_grade/
│
├── app/
│   └── streamlit_app.py          # Streamlit dashboard
│
├── pharma_genai/
│   ├── __init__.py
│   ├── featurization.py          # RDKit descriptors + fallback descriptors
│   ├── admet.py                  # ADMET, molecular property, toxicity scoring
│   ├── reliability.py            # uncertainty and reliability scoring
│   ├── pipeline.py               # end-to-end molecule analysis
│   └── cli.py                    # command line interface
│
├── tests/
│   ├── test_pharma_genai.py
│   └── test_pharma_genai_v2.py
│
├── examples/
│   └── example_smiles.csv
│
├── docs/
│   └── PORTFOLIO_PROJECT_BRIEF.md
│
├── MODEL_CARD.md
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## Troubleshooting

### Error: `No module named pytest`

Install pytest into the active environment:

```bash
python -m pip install pytest
python -m pytest
```

### Error: `No module named pharma_genai`

Install the package in editable mode from the project root:

```bash
python -m pip install -e .
python -m pytest
```

### Error: `File does not exist: streamlit_app.py`

Use the correct app path:

```bash
streamlit run app/streamlit_app.py
```

### Check where the app is located

```bash
find app pharma_genai src -type f | grep -E "streamlit|app.py|ui.py"
```

### Check your active Python and pip

```bash
which python
python -m pip --version
```

Both should point to the `pharma_v2` conda environment.

---

## Professional Positioning

This project is designed for pharmaceutical AI / computational chemistry portfolios. It highlights practical skills in cheminformatics, machine learning pipelines, uncertainty-aware model interpretation, candidate ranking, and product-style deployment.

It is especially aligned with a pharmaceutical data science profile involving ADMET modeling, computational chemistry, ensemble modeling, reliability analysis, Python, and applied machine learning.

---

## Important Limitation

This V2.1 package is a portfolio-grade framework with transparent heuristic models and demo-ready prediction logic. For production pharmaceutical use, retrain and calibrate the models on validated ADMET and toxicity datasets such as TDC, ChEMBL, Tox21, ClinTox, or proprietary assay data.
