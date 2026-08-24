# CAPSDAC Phase 4 GCP Deployment Guide

This guide turns the CAPSDAC ML platform from a local forecasting project into a cloud-ready Principal Data Engineer portfolio project.

## 1. Validate locally

```bash
export PYTHONPATH=$PWD/forecasting
python forecasting/scripts/run_capsdac_pipeline.py
python forecasting/scripts/generate_visualization_report.py
pytest
```

Expected local validation:

```text
2 passed
```

## 2. Configure GCP

```bash
export PATH="$HOME/google-cloud-sdk/bin:$PATH"
gcloud config set project capsdac2-ml
gcloud services enable \
  aiplatform.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  run.googleapis.com
```

## 3. Deploy infrastructure

```bash
cd infrastructure/terraform
terraform init
terraform apply -auto-approve \
  -var="project_id=capsdac2-ml" \
  -var="region=us-central1" \
  -var="bucket_name=capsdac2-ml-yuzhang"
```

## 4. Deploy Cloud Run API

```bash
bash infrastructure/cloudrun/deploy_cloud_run.sh capsdac2-ml us-central1 capsdac-forecast-api
```

## 5. Submit Vertex AI training job

```bash
python mlops/vertex_ai/submit_custom_training_job.py \
  --project capsdac2-ml \
  --region us-central1 \
  --bucket capsdac2-ml-yuzhang \
  --display-name capsdac-forecast-train
```

## 6. Load forecast outputs to BigQuery

```bash
bash infrastructure/bigquery/load_forecasts_to_bigquery.sh capsdac2-ml capsdac_analytics
```

## 7. Run monitoring checks

```bash
python mlops/monitoring/forecast_monitoring.py
```

## Interview positioning

This project now demonstrates:

- governed data lake and BigQuery analytics layer
- batch forecasting pipeline
- reusable feature engineering package
- model training and artifact management
- Cloud Run serving API
- Vertex AI custom training path
- Terraform infrastructure as code
- forecast monitoring and data quality checks
