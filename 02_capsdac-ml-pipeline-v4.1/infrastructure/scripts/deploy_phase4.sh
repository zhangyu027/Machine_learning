#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID=${1:-capsdac2-ml}
REGION=${2:-us-central1}
BUCKET=${3:-capsdac2-ml-yuzhang}

export PATH="$HOME/google-cloud-sdk/bin:$PATH"
gcloud config set project "$PROJECT_ID"

gcloud services enable \
  aiplatform.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  run.googleapis.com

if ! gsutil ls -b "gs://$BUCKET" >/dev/null 2>&1; then
  gsutil mb -p "$PROJECT_ID" -l "$REGION" "gs://$BUCKET"
fi

# Terraform is optional but recommended for repeatable infrastructure.
if command -v terraform >/dev/null 2>&1; then
  (cd infrastructure/terraform && \
    terraform init && \
    terraform apply -auto-approve \
      -var="project_id=$PROJECT_ID" \
      -var="region=$REGION" \
      -var="bucket_name=$BUCKET")
else
  echo "Terraform not installed; skipping Terraform apply. Install Terraform to create full IaC-managed resources."
fi

# Local validation before cloud deployment.
export PYTHONPATH=$PWD/forecasting
python forecasting/scripts/run_capsdac_pipeline.py
python forecasting/scripts/generate_visualization_report.py
pytest

# Build and deploy Cloud Run API.
bash infrastructure/cloudrun/deploy_cloud_run.sh "$PROJECT_ID" "$REGION" capsdac-forecast-api

echo "Phase 4 deployment starter complete."
