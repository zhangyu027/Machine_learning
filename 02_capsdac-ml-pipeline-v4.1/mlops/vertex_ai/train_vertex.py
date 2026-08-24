"""Vertex AI training entrypoint for CAPSDAC forecasting.

This wrapper preserves the same code path as local validation and can run inside
Vertex AI custom training. It writes model artifacts and metrics to the repo
workspace; production jobs can copy these outputs to GCS after training.
"""
from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if __name__ == "__main__":
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "forecasting")
    subprocess.check_call(["python", str(ROOT / "forecasting" / "scripts" / "run_capsdac_pipeline.py")], env=env)
