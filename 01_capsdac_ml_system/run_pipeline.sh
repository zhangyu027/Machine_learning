#!/usr/bin/env bash

set -e

echo "Running CAPSDAC pipeline helper..."
python scripts/run_capsdac_pipeline.py

echo "Generating visualization inventory..."
python scripts/generate_visualization_report.py

echo "Done. Review outputs/reports/."
