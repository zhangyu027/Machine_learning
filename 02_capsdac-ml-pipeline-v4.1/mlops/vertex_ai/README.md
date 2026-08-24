# Vertex AI Deployment Pattern

This folder contains the Vertex AI productionization pattern for the CAPSDAC forecasting model.

Recommended flow:
1. Train model using `forecasting/scripts/run_capsdac_pipeline.py`
2. Upload model artifact to Cloud Storage
3. Register model in Vertex AI Model Registry
4. Run batch prediction for statewide, vendor, and site forecasts
5. Monitor forecast drift and data quality
