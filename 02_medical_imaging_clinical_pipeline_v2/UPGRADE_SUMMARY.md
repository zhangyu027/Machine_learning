# Upgrade Summary

## Added

- ResNet50 and EfficientNet-B0 transfer-learning model support
- Runnable CNN training entry point with checkpoint metadata
- FastAPI `/health` and `/predict` endpoints for image upload
- ROC, precision-recall, confusion-matrix, calibration, and misclassification report generator
- Sensitivity, specificity, precision, F1, ROC-AUC, and average-precision metrics
- PSI-based drift monitoring and review thresholds
- Dockerfile and Docker Compose deployment
- GitHub Actions continuous integration
- Model card and structured clinical error-analysis plan
- API and monitoring tests

## Preserved

- Bronze/Silver/Gold lakehouse pipeline
- Synthetic-data local demo
- Streamlit review application
- Existing architecture and interview documentation

## Validation Performed

- `python scripts/run_pipeline.py`: passed
- `pytest -q`: 3 passed
- Python compile check: passed

## Important Result Interpretation

The synthetic baseline run showed high specificity but low sensitivity. This is not presented as clinical performance. It is retained as a realistic demonstration of why accuracy alone is insufficient and why threshold tuning, class imbalance, calibration, and false-negative review are required.
