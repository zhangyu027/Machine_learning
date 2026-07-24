# Model Card — Medical Imaging Clinical AI Classifier

## Intended Use

This model is a portfolio demonstration of binary medical-image classification, evaluation, API serving, and monitoring. It is intended for engineering interviews, education, and reproducibility exercises.

## Out-of-Scope Use

The model must not be used for diagnosis, triage, treatment decisions, or unsupervised clinical deployment. It has not undergone prospective clinical validation, regulatory review, external-site validation, or fairness validation on representative patient populations.

## Model Architecture

The production-oriented training path supports ResNet50 and EfficientNet-B0 transfer learning. Images are converted to grayscale, resized, normalized, augmented during training, and classified into two demonstration classes.

## Data

The lightweight lakehouse pipeline uses synthetic metadata. The optional CNN path expects public or properly governed de-identified image data arranged in an ImageFolder structure. No PHI should be committed to the repository.

## Evaluation

Recommended reporting includes ROC-AUC, average precision, sensitivity, specificity, precision, F1, confusion matrix, calibration, and false-positive/false-negative review. Performance must also be assessed by relevant subgroups and acquisition sites before any real-world consideration.

## Limitations and Risks

- Dataset shift across scanners, sites, protocols, and patient populations
- Label noise and uncertain ground truth
- Class imbalance and threshold sensitivity
- Potential demographic and access-related bias
- Poor calibration outside the training distribution
- Explainability artifacts such as Grad-CAM do not establish causal reasoning

## Monitoring

Track input quality, missingness, acquisition-site mix, prediction distribution, confidence, latency, errors, and PSI-based drift. Trigger review when PSI exceeds 0.1 and investigate/revalidate when it exceeds 0.25.

## Human Oversight

Any clinical research use requires qualified clinical review, documented operating thresholds, audit logs, incident response, and an approved governance process.
