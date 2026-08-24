#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-capsdac2-ml}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-capsdac-forecast-api}"
REPOSITORY="${REPOSITORY:-capsdac-ml}"

echo "Using project: $PROJECT_ID"
gcloud config set project "$PROJECT_ID"

echo "Cloud Run services:"
gcloud run services list --region="$REGION" || true

echo "Vertex AI custom jobs:"
gcloud ai custom-jobs list --region="$REGION" || true

echo "Artifact Registry repositories:"
gcloud artifacts repositories list --location="$REGION" || true

echo "Storage buckets:"
gcloud storage buckets list --project="$PROJECT_ID" || true

echo
echo "Optional cleanup commands:"
echo "gcloud run services delete $SERVICE_NAME --region=$REGION"
echo "gcloud artifacts repositories delete $REPOSITORY --location=$REGION"
echo "gcloud storage rm --recursive gs://REAL_BUCKET_NAME/** && gcloud storage buckets delete gs://REAL_BUCKET_NAME"
