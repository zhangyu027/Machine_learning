"""Submit CAPSDAC forecasting training as a Vertex AI custom job.

Usage:
  python mlops/vertex_ai/submit_custom_training_job.py \
    --project capsdac2-ml \
    --region us-central1 \
    --bucket capsdac2-ml-yuzhang \
    --display-name capsdac-forecast-train
"""
from __future__ import annotations

import argparse
from google.cloud import aiplatform


def submit_job(project: str, region: str, bucket: str, display_name: str) -> None:
    aiplatform.init(project=project, location=region, staging_bucket=f"gs://{bucket}")
    job = aiplatform.CustomJob.from_local_script(
        display_name=display_name,
        script_path="mlops/vertex_ai/train_vertex.py",
        container_uri="us-docker.pkg.dev/vertex-ai/training/sklearn-cpu.1-3:latest",
        requirements=["pandas", "numpy", "scikit-learn", "joblib", "pyyaml", "matplotlib"],
        replica_count=1,
        machine_type="n1-standard-4",
    )
    job.run(sync=True)
    print(f"Submitted Vertex AI job: {display_name}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--region", default="us-central1")
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--display-name", default="capsdac-forecast-train")
    args = parser.parse_args()
    submit_job(args.project, args.region, args.bucket, args.display_name)


if __name__ == "__main__":
    main()
