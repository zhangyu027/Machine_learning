# Medical Imaging Clinical AI Pipeline

A clean, portfolio-ready project that unifies:

- a **CNN baseline** for image classification
- a **multimodal model** that combines image + clinical metadata
- an optional **graph reasoning stage** that aggregates evidence from similar cases

This package is designed to be easy to explain in interviews and easy to extend into a real healthcare AI demo.

## Why merge the old projects?

Instead of keeping both `medical image pipeline` and `medical multimodal graph` as separate top-level projects, this package treats them as one evolving system:

1. **Baseline**: image-only CNN
2. **Multimodal**: image + structured clinical features
3. **Graph-enhanced**: use nearest-neighbor case relationships to refine predictions

That gives you a stronger story for interviews:
> "I started with a baseline medical imaging classifier, then extended it into a multimodal and graph-enhanced clinical AI system."

## Project structure

```text
02_medical_imaging_clinical_ai/
├── README.md
├── GRAPH_README.md
├── requirements.txt
├── config.py
├── .gitignore
├── preprocessing/
│   ├── __init__.py
│   ├── dataset.py
│   └── metadata.py
├── model/
│   ├── __init__.py
│   ├── cnn_backbone.py
│   ├── multimodal_model.py
│   ├── graph_fusion.py
│   ├── utils.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
├── inference_api/
│   ├── __init__.py
│   └── main.py
├── docs/
│   └── ARCHITECTURE_GRAPH.md
├── artifacts/
└── data/
    ├── train/
    ├── val/
    └── test/
```

## Modeling options

Set `MODEL_TYPE` in the environment or in `config.py`.

### 1) CNN baseline
- image-only classification
- simplest benchmark
- best first experiment

### 2) Multimodal
- image encoder
- metadata encoder
- fusion layer
- better reflects real clinical workflows

### 3) Multimodal + graph refinement
- use image/metadata embeddings
- find similar cases with k-nearest neighbors
- refine prediction with neighbor evidence

## Quick start

### Install

```bash
pip install -r requirements.txt
```

### Train CNN baseline

```bash
MODEL_TYPE=cnn python -m model.train
```

### Train multimodal model

```bash
MODEL_TYPE=multimodal_graph python -m model.train
```

### Evaluate

```bash
python -m model.evaluate
```

### Run API

```bash
uvicorn inference_api.main:app --reload
```

## Example metadata CSV

```csv
rel_path,age,sex_binary,bmi,lab_crp,label
train/negative/example1.png,54,0,24.2,3.1,0
train/positive/example2.png,67,1,31.4,9.7,1
```

## API example

POST `/predict`

- `file`: image upload
- `metadata_json`: optional JSON string

Example metadata payload:

```json
{"age": 63, "sex_binary": 1, "bmi": 29.1, "lab_crp": 8.4}
```

## Recommended interview demo flow

1. Explain the baseline CNN
2. Show why image-only is limited in healthcare
3. Add clinical metadata fusion
4. Add graph reasoning over similar cases
5. Deploy with FastAPI

## Recommended next upgrades

- DICOM support
- Grad-CAM visualization
- experiment tracking
- Docker
- CI tests
- threshold tuning
- calibration curves
- clinician-facing explanation output
