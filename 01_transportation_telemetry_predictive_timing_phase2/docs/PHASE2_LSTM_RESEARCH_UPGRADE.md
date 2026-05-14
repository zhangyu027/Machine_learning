# Phase 2 LSTM Research Upgrade

## What was added

This upgrade adds a sequence-based LSTM model to make the transportation telemetry project more research-aligned.

## Why LSTM matters

The original project used a feedforward neural network. That is useful for a portfolio demo, but it treats each telemetry event as independent.

Railway and transportation telemetry is naturally sequential:

- train speed evolves over time
- vibration patterns develop over time
- delay risk accumulates over time
- engine temperature and braking behavior have temporal patterns
- maintenance risk depends on recent operational history

An LSTM can learn from a window of previous telemetry events.

## New files

```text
src/sequence_features.py
src/lstm_model.py
src/lstm_visualization.py
scripts/run_phase2_lstm_pipeline.py
notebooks/Phase2_LSTM_Transportation_Telemetry_Demo.ipynb
docs/PHASE2_LSTM_RESEARCH_UPGRADE.md
run_phase2_lstm_pipeline.sh
```

## New outputs

```text
data/gold/train_delay_sequences.npz
outputs/models/lstm_delay_timing.pt
outputs/models/lstm_sequence_scaler.joblib
outputs/tables/lstm_model_metrics.json
outputs/tables/lstm_classification_report.csv
outputs/tables/lstm_predictions.csv
outputs/tables/lstm_training_loss.csv
outputs/tables/lstm_confusion_matrix.csv
outputs/figures/lstm_training_loss_curve.png
outputs/figures/lstm_confusion_matrix_delay_risk.png
outputs/figures/lstm_roc_curve_delay_risk.png
outputs/figures/lstm_precision_recall_delay_risk.png
outputs/figures/lstm_actual_vs_predicted_delay_minutes.png
outputs/figures/lstm_classification_metrics_bar_chart.png
```

## Research framing

The project now supports discussion of:

- IoT-style train telemetry
- sequential time-series modeling
- predictive maintenance
- delay-risk forecasting
- neural network sequence learning
- research-grade evaluation

## Future upgrade

A future Phase 3 could add:

- CNN-LSTM hybrid
- Kafka simulator
- Spark Structured Streaming
- Delta Lake / Iceberg
- geospatial route modeling
- late-arriving event handling
- online model monitoring
