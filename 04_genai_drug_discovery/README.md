# Generative AI Drug Discovery — Pharmaceutical ML V2

This project is a portfolio-ready pharmaceutical machine learning package for small-molecule drug discovery. It extends the original GenAI drug discovery folder with ADMET prediction, molecular property prediction, toxicity screening, RDKit feature engineering, reliability scoring, and a Streamlit UI.

## Main Features

- **ADMET prediction**: oral absorption, solubility risk, BBB penetration, CYP inhibition risk.
- **Molecular property prediction**: MW, LogP, TPSA, HBD/HBA, rotatable bonds, QED, rings, fraction CSP3.
- **Toxicity prediction**: hERG risk, hepatotoxicity risk, AMES-like mutagenicity proxy, combined toxicity risk.
- **RDKit feature engineering**: uses RDKit when installed; includes a lightweight fallback for simple demos.
- **Reliability scoring**: Wenkel Liang-style prediction reliability analysis with uncertainty, applicability domain, ensemble-proxy disagreement, and beta-binomial style confidence communication.
- **Streamlit UI**: interactive candidate ranking and CSV export.
- **Portfolio documentation**: model card, project brief, CLI, tests, example data.

## Quick Start

```bash
pip install -r requirements.txt
pip install -e .
```

Score one molecule:

```bash
python -m pharma_genai.cli score "CC(=O)Oc1ccccc1C(=O)O"
```

Score a CSV file:

```bash
python -m pharma_genai.cli batch examples/example_smiles.csv --output outputs/admet_v2_predictions.csv
```

Launch the Streamlit UI:

```bash
streamlit run app/streamlit_app.py
```

Run tests:

```bash
pytest -q
```

## Project Structure

```text
pharma_genai/
  featurization.py      # RDKit descriptors + fallback descriptors
  admet.py              # ADMET, molecular property, toxicity scoring
  reliability.py        # uncertainty and reliability scoring
  pipeline.py           # end-to-end batch analysis
  cli.py                # command line interface
app/
  streamlit_app.py      # portfolio UI
examples/
  example_smiles.csv
docs/
  PORTFOLIO_PROJECT_BRIEF.md
MODEL_CARD.md
```

## Professional Positioning

This project is designed for pharmaceutical AI / computational chemistry portfolios. It highlights practical skills in cheminformatics, machine learning pipelines, uncertainty-aware model interpretation, candidate ranking, and product-style deployment.

## Important Limitation

The current V2 package is a portfolio-grade framework with transparent heuristic models. For production pharmaceutical use, retrain and calibrate the models on validated ADMET datasets such as TDC, ChEMBL, Tox21, ClinTox, or proprietary assay data.
