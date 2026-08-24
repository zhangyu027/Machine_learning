#!/usr/bin/env bash
set -euo pipefail
export PYTHONPATH="$PWD/forecasting:$PWD"
python scripts/generate_demo_data.py
python forecasting/scripts/run_capsdac_pipeline.py "$@"
