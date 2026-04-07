# Medical Imaging Diagnosis Pipeline (CNN)

## Overview
This project implements an end-to-end CNN-based medical imaging diagnosis workflow, from image preprocessing to model training, evaluation, and serving inference via FastAPI.

## Highlights
- Transfer learning with ResNet18
- Image preprocessing and augmentation
- Test evaluation with confusion matrix
- FastAPI inference endpoint
- Portfolio-ready system design for healthcare AI interviews

## Structure
- `preprocessing/` dataset and transforms
- `model/` training, evaluation, prediction
- `inference_api/` deployment-ready API
- `artifacts/` saved weights and evaluation outputs

## Data Layout
Place your data in:

```text
data/
  train/
    negative/
    positive/
  val/
    negative/
    positive/
  test/
    negative/
    positive/
```

## Run
```bash
python model/train.py
python model/evaluate.py
uvicorn inference_api.main:app --reload
```

## Interview Story
I built a production-oriented medical imaging diagnosis pipeline using CNN transfer learning. I designed image preprocessing, trained a classifier using ResNet18, evaluated performance with clinical-style metrics, and exposed the model behind a FastAPI endpoint for inference. The project demonstrates healthcare AI modeling plus deployment thinking.

## Suggested Extensions
- Grad-CAM visualization
- DICOM reader pipeline
- AUC/ROC plotting
- model registry and experiment tracking
- Dockerfile + CI/CD
