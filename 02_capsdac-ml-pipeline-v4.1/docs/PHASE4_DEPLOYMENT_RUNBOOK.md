# Phase 4 Deployment Runbook

## Completed locally

```bash
export PYTHONPATH=$PWD/forecasting
pytest
```

Expected result: tests pass.

## Cloud Build and Artifact Registry

Create Artifact Registry repository if needed:

```bash
gcloud artifacts repositories create capsdac-ml   --repository-format=docker   --location=us-central1   --description="CAPSDAC ML Docker images"
```

Submit build:

```bash
gcloud builds submit --config infrastructure/cloudbuild/cloudbuild.yaml .
```

Verify image:

```bash
gcloud artifacts docker images list   us-central1-docker.pkg.dev/capsdac2-ml/capsdac-ml
```

Expected image:

```text
us-central1-docker.pkg.dev/capsdac2-ml/capsdac-ml/capsdac-forecast-api
```

## Optional Cloud Run deployment

```bash
gcloud run deploy capsdac-forecast-api   --image=us-central1-docker.pkg.dev/capsdac2-ml/capsdac-ml/capsdac-forecast-api:latest   --region=us-central1   --platform=managed   --allow-unauthenticated
```

Test:

```bash
SERVICE_URL=$(gcloud run services describe capsdac-forecast-api --region=us-central1 --format='value(status.url)')
curl "$SERVICE_URL/health"
curl "$SERVICE_URL/forecasts/statewide"
```

## Low-cost stopping point

For portfolio purposes, Cloud Build success + Artifact Registry image existence is enough evidence that the CI/CD containerization path works. Cloud Run, Vertex AI, and BigQuery can remain as documented deployment paths unless you need screenshots.
