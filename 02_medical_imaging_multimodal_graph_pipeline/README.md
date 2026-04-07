# Medical Imaging Pipeline (CNN + Multi-Modal Graph Learning)

## Overview
This project regenerates your original CNN-based medical imaging pipeline into a **hybrid clinical AI project**:

- **CNN branch** for raw image understanding
- **Multi-modal fusion** for adding clinical/tabular features
- **Graph learning block** for reasoning over patient/image similarity inside each batch
- **FastAPI inference service** for deployment-style demos

It keeps the same portfolio-friendly structure as your original package:
- `config.py`
- `preprocessing/`
- `model/`
- `inference_api/`
- `README.md`
- `requirements.txt`

## Why this design
For clinical medical imaging:
- **CNN** is still the right first choice for pixel data
- **Graph / multi-modal learning** becomes useful when you also have:
  - demographics
  - vitals / labs
  - lesion attributes
  - prior exam metadata
  - study-level context

This project supports both:
- `MODEL_TYPE=cnn`
- `MODEL_TYPE=multimodal_graph`

## Project Structure
```text
02_medical_imaging_multimodal_graph_pipeline/
├── config.py
├── requirements.txt
├── README.md
├── artifacts/
├── data/
│   ├── train/
│   ├── val/
│   ├── test/
│   └── metadata/
│       └── sample_metadata.csv
├── inference_api/
│   └── main.py
├── model/
│   ├── cnn_backbone.py
│   ├── graph_fusion.py
│   ├── multimodal_model.py
│   ├── train.py
│   ├── evaluate.py
│   └── predict.py
└── preprocessing/
    ├── dataset.py
    └── graph_utils.py
```

## Data Layout
Images stay in the same folder layout:

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

Optional clinical metadata CSV:

```text
rel_path,age,sex_binary,bmi,lab_crp
train/negative/img001.png,54,0,24.2,3.1
train/positive/img002.png,67,1,31.4,9.7
val/positive/img003.png,72,1,28.1,12.2
test/negative/img004.png,48,0,22.5,2.0
```

- `rel_path` must match the image path relative to `data/`
- all other numeric columns are used as metadata features
- if no CSV is provided, the model still runs using zero metadata vectors

## Training
### CNN baseline
```bash
MODEL_TYPE=cnn python model/train.py
```

### Hybrid multi-modal graph model
```bash
MODEL_TYPE=multimodal_graph python model/train.py
```

## Evaluation
```bash
python model/evaluate.py
```

## Inference API
```bash
uvicorn inference_api.main:app --reload
```

POST `/predict` with:
- `file`: image file
- optional `metadata_json`: JSON dictionary with the same metadata fields used in training

Example:
```json
{"age": 63, "sex_binary": 1, "bmi": 29.1, "lab_crp": 8.4}
```

## Model Logic
1. **CNN backbone** extracts image embeddings
2. **Metadata encoder** transforms clinical features
3. **Fusion layer** concatenates image + metadata features
4. **Graph builder** connects similar samples using kNN
5. **Graph convolution blocks** propagate context across related cases
6. **Classifier head** predicts diagnosis

## Interview Story
You can describe this project like this:

> I first built a CNN medical imaging classifier, then extended it into a hybrid clinical AI system by incorporating structured patient metadata and a graph-learning layer. The CNN extracts visual features from medical images, while the graph module models relationships among clinically similar cases. This makes the system more realistic for healthcare AI, where image-only prediction is often not enough.

## Suggested Extensions
- DICOM reader support
- Grad-CAM / saliency maps
- temporal patient graphs
- report-text fusion
- experiment tracking
- Docker + CI/CD
