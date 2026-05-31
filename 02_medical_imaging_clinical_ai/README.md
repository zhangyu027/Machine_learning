# Medical Imaging Clinical AI

## Project Question

**Can combining medical images with structured clinical metadata improve disease-risk prediction compared with image-only AI?**

This package is a portfolio-ready clinical AI project using **MedMNIST**, a public medical imaging benchmark that is easy to download and run locally.

The project compares:

| Model | Input | Clinical meaning |
|---|---|---|
| CNN baseline | Image only | Imaging-only benchmark |
| Multimodal | Image + metadata | Closer to clinical workflow |
| Graph-enhanced | Similar cases | Adds case-based reasoning concept |

## What is included

- Main notebook: `notebooks/Medical_Imaging_Clinical_AI_End_to_End_Demo.ipynb`
- MedMNIST public dataset loading
- Synthetic clinical metadata CSV generation
- CNN image-only baseline
- Multimodal image + metadata model
- Real evaluation table
- Confusion matrix
- ROC curve
- Precision-recall curve
- Grad-CAM heatmap
- Model comparison bar chart
- Clinical interpretation document

## How to run

```bash
cd 02_medical_imaging_clinical_ai
pip install -r requirements.txt
jupyter notebook notebooks/Medical_Imaging_Clinical_AI_End_to_End_Demo.ipynb
```

Run the notebook cells sequentially.


---

## How to Run the App

This package includes a lightweight Streamlit app for viewing notebook outputs.

### Step 1: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the main notebook first
cd /Users/yuzhang/Library/CloudStorage/Dropbox/MachineLearning/
python3 -m venv .venv311
source .venv311/bin/activate
pip install -r requirements.txt




```bash
jupyter notebook notebooks/Medical_Imaging_Clinical_AI_End_to_End_Demo.ipynb
```

Run all cells. This creates:

```text
outputs/figures/
outputs/tables/
data/train_metadata.csv
data/test_metadata.csv
```

### Step 3: Launch the Streamlit app

```bash
streamlit run app/streamlit_app.py
```

Then open:

```text
http://localhost:8501
```

### If Streamlit shows a Torch watcher warning

Use:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

---

## Additional Project Components

### preprocessing/

Contains preprocessing utilities for:

- synthetic metadata generation
- metadata normalization
- preprocessing summary output

Main file:

```text
preprocessing/preprocess_medmnist.py
```

### graph/

Contains the graph-enhanced clinical reasoning extension.

Main files:

```text
graph/README.md
graph/case_similarity_graph.py
```

This is a conceptual extension for similar-case reasoning. It is intentionally lightweight because MedMNIST does not include full clinical records.

### artifacts/

Designed to store final reusable outputs:

```text
artifacts/models/
artifacts/figures/
artifacts/tables/
artifacts/reports/
```

The notebook writes primary outputs to `outputs/`, while `artifacts/` is included as a clean place to copy final deliverables for GitHub review.


## Outputs

Figures are saved to:

```text
outputs/figures/
```

Tables are saved to:

```text
outputs/tables/
```

Clinical interpretation is saved to:

```text
docs/CLINICAL_INTERPRETATION.md
```

## Important clinical limitation

This is a portfolio and education project. It is **decision support, not diagnosis**.

The MedMNIST dataset is real public medical imaging data, but the structured metadata in this package is synthetic for demonstration. Replace it with real clinical metadata for real research.

## Resume bullet

Built a clinical multimodal AI pipeline using MedMNIST to compare image-only CNN prediction with image-plus-metadata prediction, including confusion matrix, ROC/PR curves, Grad-CAM explainability, and clinical interpretation documentation.
