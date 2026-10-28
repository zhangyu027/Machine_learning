# Interview Notes — Clinical Decision Intelligence V3

_Last updated: 2026-10-28. Synthetic-data reference implementation; not for clinical use._

## 60-second project narrative

“I built a clinical decision-intelligence reference platform around a synthetic 30-day hospital readmission prediction task. The platform combines model training and evaluation with authenticated FastAPI serving, FHIR-style risk output, clinician feedback, Prometheus monitoring, MLflow experiment tracking and registry, and Docker Compose orchestration. In a local end-to-end smoke test, I verified prediction, FHIR output, feedback acknowledgement, and Prometheus scraping. I then debugged the MLflow storage and client/server version issues and successfully logged and registered an XGBoost model. This is a production-oriented engineering demonstration, not a clinically validated or deployed system.”

## Results I can substantiate

- **Latest local MLflow run:** `defiant-cat-899` / `1164e2fd7bf94475b4b8791c4f3562c3`, experiment `clinical-decision-intelligence-v3`.
- **ROC-AUC:** `0.7432348468848465`; **average precision:** `0.5620893332451523`.
- **Registry:** `readmission-risk-xgboost`, model version `1`, created successfully.
- **Earlier separate package validation:** ROC-AUC `0.7434`, average precision `0.5619`; propensity-score matched ATT `-0.1092` across `18,572` matched pairs. Do not imply the causal estimate is a randomized treatment effect.
- **API:** `/health`, `/ready`, `/version` worked; authenticated `/v1/predict`, `/v1/predict/fhir`, `/v1/feedback` returned HTTP 200 for synthetic requests.
- **Prediction example:** synthetic encounter `SYNTHETIC-001`, risk `0.402451753616333`, moderate category, clinician review required; FHIR-style RiskAssessment probability `0.402452`.
- **Monitoring:** Prometheus target `http://api:8000/metrics` UP (1/1); Grafana login UI loaded, but dashboard queries and datasource configuration were not verified.
- **Not demonstrated by these checks:** external clinical validity, real EHR integration, durable feedback persistence, production security/operations, Kubernetes rollout, CI completion.

## Technical architecture and decisions

1. **Model:** XGBoost readmission-risk training on synthetic encounter data. ROC-AUC assesses discrimination across thresholds; average precision summarizes precision-recall performance. Neither proves calibration, subgroup fairness, causal effect, or patient benefit.
2. **Serving:** versioned FastAPI endpoints, API-key protected POST operations, readiness/health/version endpoints, FHIR R4-style RiskAssessment adapter. The response requires clinician review; this is not autonomous medical decision-making.
3. **Observability:** Prometheus scrapes API metrics over the Docker network; Grafana is included as a visualization service, with dashboard verification outstanding.
4. **Experiment tracking:** MLflow tracks metrics, feature-schema JSON and model artifacts; the registry holds `readmission-risk-xgboost` version 1. The Mac client and Docker server use MLflow 2.22.0.
5. **Tradeoffs:** synthetic vs clinical data; portable local JSONL feedback vs transactional audited persistence; FHIR-style output vs certified EHR integration; model discrimination vs calibration, drift, fairness and human oversight.

## Debugging story — a strong interview example

**Problem:** A working prediction API did not initially translate into a reproducible MLflow training record.

**Diagnosis and resolution:**
- The training script imported nonexistent `MLFLOW_TRACKING_URI` from `core.config`; changed it to use `settings.mlflow_tracking_uri`.
- MLflow initially created a run but artifact logging attempted a local `/mlflow-data` write from macOS, producing `Errno 30: Read-only file system`. Configured server-side artifact serving with `--serve-artifacts` and `--artifacts-destination /mlflow-data/artifacts`, then used a fresh experiment to avoid the old artifact URI.
- Model logging then failed with HTTP 404 on `/api/2.0/mlflow/logged-models`. The Mac MLflow client was 3.16.1, but the server was 2.22.0. Aligned the local client to 2.22.0 and pinned `mlflow==2.22.0` in `requirements.txt`.
- Retried successfully: metrics printed, model registered as version 1. The log warned that the model lacked an input example and signature, which remains a future improvement.

**Lesson:** Validate not only service health but the full artifact lifecycle (tracking URI, artifact transport, model registry API compatibility, reproducible dependency versions).

## Likely interview questions

**Q: Is ROC-AUC 0.743 good enough for deployment?**  
A: It shows some discrimination in the synthetic test setting, not clinical readiness. I would require prospective/external validation, calibration, subgroup analysis, drift monitoring, workflow evaluation, security/privacy review, and clinical governance before any real-world use.

**Q: Why MLflow and a registry?**  
A: They make run metrics, artifacts and model versions discoverable. I verified model registration, but deployment promotion, lineage governance and rollback processes are not yet proven.

**Q: Why did artifact logging fail?**  
A: The experiment's artifact URI pointed to a path inside Docker that a Mac client could not write. Server-proxied artifacts solved the cross-environment boundary; a new experiment was used because old experiment artifact URIs can persist.

**Q: What caused the 404?**  
A: A 3.16.1 client invoked a logged-model endpoint unavailable on the 2.22.0 server. Matching the versions fixed it.

**Q: What would you improve next?**  
A: Add a model signature/input example; verify Grafana datasource and dashboards; automate a fresh-environment Docker smoke test; validate model/calibration/fairness on appropriate datasets; strengthen feedback persistence, privacy and auditability; verify CI and Kubernetes separately.

## Honest portfolio positioning

Call this a **production-oriented synthetic-data reference platform**, not a hospital production deployment, approved medical device, or clinically validated model. Report the specific local smoke tests and MLflow run evidence; do not claim unexecuted gates passed.
