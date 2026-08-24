#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID=${1:-capsdac2-ml}
REGION=${2:-us-central1}
SERVICE=${3:-capsdac-forecast-api}
IMAGE="$REGION-docker.pkg.dev/$PROJECT_ID/capsdac-ml/$SERVICE:latest"

gcloud builds submit --tag "$IMAGE" .
gcloud run deploy "$SERVICE" \
  --image "$IMAGE" \
  --region "$REGION" \
  --platform managed \
  --allow-unauthenticated \
  --memory 1Gi \
  --cpu 1 \
  --set-env-vars PROJECT_ID="$PROJECT_ID"
