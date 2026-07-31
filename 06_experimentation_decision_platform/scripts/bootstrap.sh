#!/usr/bin/env bash
set -euo pipefail

python -m pip install --upgrade pip
python -m pip install -r requirements-all.txt
python -m pip install -e .

echo "Environment ready. Run: python -m scripts.run_full_pipeline"
echo "Then run: pytest -q"
