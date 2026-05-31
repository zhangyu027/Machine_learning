# Artifacts

This folder is designed to hold generated project outputs.

## Folder structure

```text
artifacts/
├── models/
├── figures/
├── tables/
└── reports/
```

## What should be saved here

### models/

Saved PyTorch model files, for example:

```text
cnn_baseline.pt
multimodal_model.pt
```

### figures/

Visual outputs such as:

```text
confusion_matrix_multimodal.png
roc_curve_comparison.png
precision_recall_curve_comparison.png
gradcam_heatmap.png
model_comparison_bar_chart.png
```

### tables/

Evaluation tables such as:

```text
real_evaluation_table.csv
classification_report_multimodal.csv
```

### reports/

Clinical interpretation or summary reports.

## Why this folder matters

Keeping artifacts separate makes the GitHub project easier to review.  
A hiring manager or reviewer can quickly find the results without rerunning the notebook.
