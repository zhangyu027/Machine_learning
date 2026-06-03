# Architecture

```text
Synthetic patient record
     ├── Image-like array
     ├── Clinical note
     ├── Lab values
     └── Structured EHR features
              ↓
Modality Encoders
     ├── CNN image encoder
     ├── Clinical text encoder
     ├── Lab encoder
     └── Structured EHR encoder
              ↓
Multimodal Fusion Layer
              ↓
Risk Prediction Head
              ↓
Evaluation
     ├── Accuracy / F1 / AUC
     ├── Confusion matrix
     ├── ROC / PR curves
     ├── Calibration
     ├── Fairness by subgroup
     └── Uncertainty estimation
              ↓
Streamlit Explainability Dashboard
```

## Production Upgrade Path

A production version could add:

- FHIR ingestion
- DICOM image ingestion
- ClinicalBERT or BioClinicalBERT
- Vision Transformer image encoder
- SHAP and Grad-CAM
- MLflow experiment tracking
- model registry
- external validation
- secure deployment
