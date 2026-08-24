#!/usr/bin/env bash
set -euo pipefail
PROJECT_ID=${1:-capsdac2-ml}
DATASET=${2:-capsdac_analytics}

bq --project_id "$PROJECT_ID" load --replace --source_format=CSV --skip_leading_rows=1 \
  "$DATASET.statewide_forecast" outputs/forecasts/statewide_forecast.csv

bq --project_id "$PROJECT_ID" load --replace --source_format=CSV --skip_leading_rows=1 \
  "$DATASET.vendor_forecast" outputs/forecasts/vendor_forecast.csv
