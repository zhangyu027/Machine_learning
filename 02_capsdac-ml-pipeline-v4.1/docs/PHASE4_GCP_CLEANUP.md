# Phase 4 GCP Cleanup and Cost-Control Checklist

Use this after validating Cloud Build / Artifact Registry / Cloud Run / Vertex AI.

## 1. Check what exists

```bash
gcloud run services list --region=us-central1
gcloud ai custom-jobs list --region=us-central1
gcloud artifacts repositories list --location=us-central1
gcloud storage buckets list --project=capsdac2-ml
gcloud builds list --limit=5
```

## 2. Stop running compute

Cloud Run generally scales to zero, but delete the demo service if you do not need it:

```bash
gcloud run services delete capsdac-forecast-api --region=us-central1
```

Vertex AI custom jobs cannot be deleted from the CLI after completion. If a job is still running, cancel it:

```bash
gcloud ai custom-jobs cancel REAL_JOB_ID --region=us-central1
```

## 3. Delete demo storage buckets only if not needed

```bash
gcloud storage rm --recursive gs://REAL_BUCKET_NAME/**
gcloud storage buckets delete gs://REAL_BUCKET_NAME
```

Do not delete buckets that contain evidence/screenshots/artifacts you still need.

## 4. Delete Artifact Registry only when finished showing deployment evidence

```bash
gcloud artifacts repositories delete capsdac-ml --location=us-central1
```

For interview evidence, it is reasonable to keep one small Docker image temporarily.

## 5. Keep a billing alert

Use the Cloud Console Billing page to create a low monthly budget alert, such as $5 or $10.
