# Healthcare Multimodal Foundation Model System

## Project Question

**Can multimodal healthcare AI combine medical images, clinical notes, labs, and structured EHR data to improve risk prediction and clinical interpretability?**

This is a flagship healthcare AI portfolio package tailored to Yu Zhang's background in medical imaging, clinical NLP, analytics, public-sector data governance, and explainable AI.

---

## What This Package Includes

- synthetic multimodal healthcare dataset
- image-like clinical signal
- clinical note text
- lab values
- structured EHR features
- multimodal PyTorch fusion model
- risk prediction
- fairness evaluation
- uncertainty estimation
- clinical interpretation report
- Streamlit dashboard
- Jupyter notebook
- architecture documentation

---

## Architecture

```text
Patient Record
 ├── Image-like clinical signal
 ├── Clinical note text
 ├── Lab values
 └── Structured EHR features
        ↓
Modality Encoders
        ↓
Multimodal Fusion Layer
        ↓
Risk Prediction
        ↓
Evaluation + Explainability + Fairness + Uncertainty
```

---

## Step-by-Step Run Instructions

### Step 1: Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the full pipeline

```bash
python scripts/run_pipeline.py
```

This runs:

1. synthetic healthcare data generation
2. image/text/lab/EHR feature preparation
3. multimodal model training
4. fairness evaluation
5. uncertainty review queue
6. visualization generation

### Step 4: Open notebook

```bash
jupyter notebook notebooks/Healthcare_Multimodal_Foundation_Model_Demo.ipynb
```

### Step 5: Launch dashboard

```bash
streamlit run app/streamlit_app.py
```

If Streamlit has watcher issues:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```
```
git status
git add .
git commit -m "Add Healthcare Multimodal Foundation Model Demo"
git push origin main
```
---

## Outputs

### Tables

```text
outputs/tables/model_metrics.json
outputs/tables/classification_report.csv
outputs/tables/confusion_matrix.csv
outputs/tables/predictions.csv
outputs/tables/fairness_subgroup_metrics.csv
outputs/tables/uncertainty_review_queue.csv
```

### Figures

```text
outputs/figures/training_loss_curve.png
outputs/figures/confusion_matrix.png
outputs/figures/roc_curve.png
outputs/figures/precision_recall_curve.png
outputs/figures/model_metrics_bar_chart.png
outputs/figures/fairness_accuracy_by_sex.png
```

### Model

```text
outputs/models/multimodal_risk_model.pt
```

---

## Important Clinical Limitation

This is a synthetic educational and portfolio project. It is not a medical device and should not be used for diagnosis or patient care.

---

## Research/Production Upgrade Path

Future upgrades:

- replace TF-IDF with ClinicalBERT or BioClinicalBERT
- replace CNN with Vision Transformer
- add SHAP explanations
- add Grad-CAM heatmaps
- add MLflow experiment tracking
- add FHIR-style schema
- add calibration curves
- add external validation
- add privacy and governance audit logs

---

## Resume Bullet

Built a multimodal healthcare AI risk prediction platform combining medical image-like data, clinical notes, lab values, and structured EHR features with PyTorch fusion modeling, fairness evaluation, uncertainty estimation, clinical interpretation documentation, and a Streamlit dashboard.
