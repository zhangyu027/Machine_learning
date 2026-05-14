# Transportation Telemetry Predictive Timing Platform

## Project Question

**Can a real-time transportation telemetry platform predict train delay timing and support predictive maintenance decision-making using sensor, location, and operational event data?**

This is a portfolio-ready transportation data engineering and ML project inspired by railway predictive maintenance research, a BNSF Sr/Staff Data Engineer job posting, and mock interview system-design questions.

## Why this project fits the role

The project demonstrates:

- real-time telemetry platform thinking
- Bronze / Silver / Gold lakehouse design
- batch pipeline that simulates streaming ingestion
- data quality and deduplication
- certified Gold feature dataset
- neural network predictive timing model
- operational evaluation and visual reporting
- Streamlit dashboard
- documentation for system design interviews

## Repository Structure

```text
06_transportation_telemetry_predictive_timing/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── raw/
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PROJECT_OVERVIEW.md
│   └── RESEARCH_ALIGNMENT.md
├── notebooks/
│   └── Transportation_Telemetry_Predictive_Timing_Demo.ipynb
├── outputs/
│   ├── figures/
│   ├── tables/
│   └── models/
├── scripts/
│   └── run_pipeline.py
├── src/
│   ├── data_generator.py
│   ├── pipeline.py
│   ├── model.py
│   └── visualization.py
├── requirements.txt
├── run_pipeline.sh
└── README.md
```

## How to Run

### 1. Create environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the full pipeline

```bash
python scripts/run_pipeline.py
```

Or:

```bash
bash run_pipeline.sh
```

### 4. Open the notebook

```bash
jupyter notebook notebooks/Transportation_Telemetry_Predictive_Timing_Demo.ipynb
```

### 5. Launch Streamlit dashboard

```bash
streamlit run app/streamlit_app.py
```

If Streamlit shows a watcher warning:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

## Pipeline

```text
Synthetic train telemetry
        ↓
Bronze raw immutable events
        ↓
Silver standardized telemetry
        ↓
Gold ML feature table
        ↓
Neural network predictive timing model
        ↓
Metrics, figures, dashboard
```

## Model

The neural network predicts:

1. **Delay risk**: binary classification
2. **Delay minutes**: regression

Input features include:

- scheduled minutes
- distance miles
- average speed
- brake pressure
- engine temperature
- vibration score
- weather severity
- route congestion
- cargo weight
- hour
- day of week

## Outputs

Tables:

```text
outputs/tables/model_metrics.json
outputs/tables/classification_report.csv
outputs/tables/predictions.csv
outputs/tables/training_loss.csv
```

Figures:

```text
outputs/figures/training_loss_curve.png
outputs/figures/confusion_matrix_delay_risk.png
outputs/figures/roc_curve_delay_risk.png
outputs/figures/precision_recall_delay_risk.png
outputs/figures/actual_vs_predicted_delay_minutes.png
outputs/figures/classification_metrics_bar_chart.png
```

## Interview Talking Points

This project supports answers to:

- How would you design a real-time train telemetry platform?
- How would you handle late-arriving streaming events?
- How do Bronze/Silver/Gold lakehouse layers work?
- How do certified datasets support analytics and ML?
- How would you monitor pipeline reliability?
- How can ML support predictive maintenance and delay prediction?

## Resume Bullet

Built a transportation telemetry data engineering and ML platform using synthetic train sensor events, a Bronze/Silver/Gold lakehouse pipeline, neural network predictive timing model, and Streamlit dashboard to predict delay risk and delay minutes for railway operations.


---

# Step-by-Step Quick Start Guide

## Step 1 — Download the Project

Unzip the package:

```bash
unzip 06_transportation_telemetry_predictive_timing.zip
cd 06_transportation_telemetry_predictive_timing
```

---

## Step 2 — Create a Python Virtual Environment

Mac/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## Step 3 — Install Required Libraries

```bash
pip install -r requirements.txt
```

---

## Step 4 — Run the Full Transportation Pipeline

This command automatically:

- generates synthetic IoT telemetry data
- creates Bronze/Silver/Gold datasets
- trains the neural network
- evaluates the model
- generates visualizations

Run:

```bash
python scripts/run_pipeline.py
```

Expected output:

```text
Step 1: Generate synthetic train telemetry
Step 2: Run Bronze/Silver/Gold pipeline
Step 3: Train neural network predictive timing model
Step 4: Generate figures
Done.
```

---

## Step 5 — Review Generated Outputs

### Tables

```text
outputs/tables/
```

Includes:

- predictions.csv
- classification_report.csv
- confusion_matrix.csv
- model_metrics.json
- training_loss.csv

---

### Figures

```text
outputs/figures/
```

Includes:

- confusion matrix
- ROC curve
- precision-recall curve
- training loss curve
- actual vs predicted delay plot
- metrics bar chart

---

## Step 6 — Open the Jupyter Notebook

```bash
jupyter notebook
```

Then open:

```text
notebooks/Transportation_Telemetry_Predictive_Timing_Demo.ipynb
```

The notebook walks through:

1. telemetry generation
2. Bronze/Silver/Gold pipeline
3. neural network training
4. evaluation
5. operational interpretation

---

## Step 7 — Launch the Streamlit Dashboard

Run:

```bash
streamlit run app/streamlit_app.py
```

Open in browser:

```text
http://localhost:8501
```

---

## Step 8 — If Streamlit Shows File Watcher Errors

Use:

```bash
streamlit run app/streamlit_app.py --server.fileWatcherType none
```

---

# Research References

This project is inspired by:

1. Railway predictive maintenance literature
2. Transportation telemetry systems
3. IoT sensor analytics
4. Real-time streaming architectures
5. Deep learning for operational forecasting

Recommended references:

- Davari et al. — Data-Driven Predictive Maintenance for Railways
- CNN-LSTM railway forecasting research
- Transportation telemetry predictive maintenance systems


---

# Phase 2 Research-Grade LSTM Upgrade

## What Phase 2 Adds

This package now includes a stronger research-aligned upgrade:

- true sequential telemetry windows
- LSTM predictive timing model
- delay-risk classification from prior train telemetry history
- delay-minute regression from prior train telemetry history
- LSTM evaluation outputs
- LSTM visualizations
- Phase 2 notebook
- Phase 2 run script

The original model is still included, but the LSTM model is the stronger research-facing version.

---

## Why This Upgrade Matters

The original feedforward neural network treats each train telemetry row independently.

The LSTM model uses a sequence of prior train telemetry observations, which is more realistic for transportation and railway predictive maintenance because delay risk and operational degradation develop over time.

The LSTM learns from patterns such as:

- speed history
- vibration history
- engine temperature trend
- route congestion progression
- braking behavior
- weather exposure
- train movement context

---

## Phase 2 Run Instructions

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the full Phase 2 LSTM pipeline

```bash
python scripts/run_phase2_lstm_pipeline.py
```

Or:

```bash
bash run_phase2_lstm_pipeline.sh
```

This command runs:

1. synthetic IoT-style train telemetry generation
2. Bronze/Silver/Gold data engineering pipeline
3. sequence-window feature engineering
4. LSTM model training
5. LSTM evaluation
6. LSTM visual generation

---

## Phase 2 Notebook

Open:

```bash
jupyter notebook notebooks/Phase2_LSTM_Transportation_Telemetry_Demo.ipynb
```

---

## Phase 2 Outputs

### Tables

```text
outputs/tables/lstm_model_metrics.json
outputs/tables/lstm_classification_report.csv
outputs/tables/lstm_predictions.csv
outputs/tables/lstm_training_loss.csv
outputs/tables/lstm_confusion_matrix.csv
outputs/tables/lstm_sequence_metadata.json
```

### Figures

```text
outputs/figures/lstm_training_loss_curve.png
outputs/figures/lstm_confusion_matrix_delay_risk.png
outputs/figures/lstm_roc_curve_delay_risk.png
outputs/figures/lstm_precision_recall_delay_risk.png
outputs/figures/lstm_actual_vs_predicted_delay_minutes.png
outputs/figures/lstm_classification_metrics_bar_chart.png
```

### Model

```text
outputs/models/lstm_delay_timing.pt
outputs/models/lstm_sequence_scaler.joblib
```

---

## Phase 2 Research Alignment

This upgrade makes the project closer to railway predictive maintenance and deep learning research because it models temporal dependencies instead of independent rows.

The project now better supports discussion of:

- IoT sensor telemetry
- sequential forecasting
- predictive maintenance
- LSTM time-series modeling
- delay-risk prediction
- operational AI systems
- Staff-level data engineering + ML platform ownership

See:

```text
docs/PHASE2_LSTM_RESEARCH_UPGRADE.md
```

---

## What Is Still Future Work

The project now includes the LSTM upgrade, but it does not yet include:

- CNN-LSTM hybrid model
- Kafka simulator
- Spark Structured Streaming
- Delta Lake / Iceberg
- geospatial route prediction
- late-arriving event handling
- online monitoring

These can become Phase 3.
