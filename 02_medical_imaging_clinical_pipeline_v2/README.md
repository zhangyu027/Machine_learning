# Medical Imaging Clinical AI — Production-Oriented Portfolio Project

This repository demonstrates an end-to-end healthcare AI system:

```text
Clinical/image data → Bronze → Silver → Gold → CNN training → evaluation → FastAPI inference → monitoring
```

It preserves a lightweight, CPU-friendly lakehouse demo while adding a production-oriented ResNet50/EfficientNet training path, clinical evaluation artifacts, Docker deployment, CI, drift monitoring, and governance documentation.

## Interview Requirements Covered

- Bronze/Silver/Gold medical imaging data pipeline
- Image preprocessing and augmentation
- ResNet50 or EfficientNet-B0 transfer learning
- ROC-AUC, average precision, sensitivity, specificity, F1, confusion matrix, calibration
- False-positive and false-negative error analysis
- FastAPI image upload and prediction endpoint
- Docker and GitHub Actions CI
- Input/prediction drift monitoring
- Model card, limitations, intended use, and clinical disclaimer
- Streamlit review application

## Repository Structure

```text
api/                    FastAPI inference service
app/                    Streamlit review app
imaging_pipeline/       Bronze, Silver, Gold, baseline model pipeline
src/                    CNN models, training, and evaluation code
evaluation/             Metrics and report generation
monitoring/             PSI-based drift checks
models/checkpoints/     Local CNN checkpoints (not committed)
docs/                   Architecture, model card, error analysis, governance
.github/workflows/      CI pipeline
tests/                  Smoke, API, and monitoring tests
```

## 1. Run the Lightweight Lakehouse Demo

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
streamlit run app/streamlit_app.py
```

This path uses synthetic metadata and validates the data engineering workflow without requiring deep-learning dependencies.

## 2. Train the CNN

Install deployment/deep-learning dependencies:

```bash
pip install -r requirements-api.txt
```

Arrange de-identified or public data as:

```text
data/images/
├── train/
│   ├── normal/
│   └── abnormal/
└── val/
    ├── normal/
    └── abnormal/
```

Train ResNet50:

```bash
python -m src.train_cnn --architecture resnet50 --epochs 5
```

Or EfficientNet-B0:

```bash
python -m src.train_cnn --architecture efficientnet_b0 --epochs 5
```

The training command writes a checkpoint under `models/checkpoints/` and metrics under `evaluation/`.

## 3. Generate Evaluation and Error-Analysis Artifacts

`evaluation/generate_report.py` creates:

- ROC curve
- Precision-recall curve
- Confusion matrix
- Calibration curve
- Ranked misclassified cases CSV

The evaluation strategy is documented in `docs/ERROR_ANALYSIS.md`. Review false negatives first, then false positives, and analyze performance by image quality, modality, scanner site, and patient subgroup when those fields are available.

## 4. Run the FastAPI Inference Service

After a ResNet50 checkpoint exists:

```bash
uvicorn api.main:app --reload
```

Endpoints:

```text
GET  /health
POST /predict
```

Example:

```bash
curl -X POST http://localhost:8000/predict \
  -F "file=@sample_image.png"
```

The response includes predicted class, confidence, class probabilities, latency, and a clinical-use disclaimer.

## 5. Docker Deployment

```bash
docker compose up --build
```

The API is exposed on port `8000`. The model directory is mounted read-only.

## 6. Monitoring

`monitoring/drift_monitor.py` implements Population Stability Index checks:

- PSI below 0.10: stable
- PSI from 0.10 to 0.25: review
- PSI above 0.25: significant drift and revalidation trigger

Production monitoring should also track image-quality failures, missing metadata, scanner/site mix, prediction distribution, confidence, latency, API errors, and subgroup performance.

## Clinical and Governance Positioning

This is a portfolio and educational project—not a medical device and not a diagnostic system. It uses synthetic metadata in the local pipeline and requires public or properly governed de-identified images for CNN training. It has not undergone prospective validation, regulatory review, external-site validation, or clinical workflow approval. See `docs/MODEL_CARD.md`.

## Interview Narrative

> I designed an end-to-end medical imaging clinical AI platform rather than only a model notebook. I built governed Bronze, Silver, and Gold data layers, integrated a ResNet50/EfficientNet training path, added clinically meaningful evaluation and error analysis, served predictions through FastAPI, containerized the service, and added CI and drift monitoring. I explicitly separated portfolio validation from clinical use and documented dataset-shift, calibration, subgroup, and human-oversight risks.

## Recommended Interview Demo

1. Show the architecture and lakehouse layers.
2. Run `python scripts/run_pipeline.py` and show generated evaluation metrics.
3. Explain the CNN training path and model choice tradeoffs.
4. Show ROC, calibration, confusion matrix, and misclassified cases.
5. Call `/health` and `/predict`.
6. Explain Docker, CI, drift thresholds, model limitations, and human oversight.
