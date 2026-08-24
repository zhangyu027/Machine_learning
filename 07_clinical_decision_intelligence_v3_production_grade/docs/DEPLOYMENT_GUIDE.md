# Deployment Guide

## Local API

```bash
python -m pip install -r requirements-all.txt
export CDI_API_KEY=test-secret
uvicorn clinical_decision_intelligence.api.app:app --host 127.0.0.1 --port 8000
```

## Docker

```bash
export CDI_API_KEY=test-secret
docker compose build --no-cache
docker compose up -d
docker compose ps
curl --fail http://127.0.0.1:8000/health
curl --fail http://127.0.0.1:8000/ready
```

## Kubernetes

Create the secret outside source control:

```bash
kubectl create secret generic cdi-secrets --from-literal=api-key="$CDI_API_KEY"
kubectl apply --dry-run=client -f k8s/deployment.yaml
kubectl apply --dry-run=client -f k8s/hpa.yaml
```

Replace the placeholder image with a pinned immutable image digest before deployment.
