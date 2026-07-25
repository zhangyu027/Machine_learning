from __future__ import annotations
import time
from collections import defaultdict, deque
from fastapi import FastAPI, Depends, Header, HTTPException, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from src.api.schemas import PatientFeatures, PredictionResponse, FeedbackRequest
from src.core.config import MODEL_PATH, API_KEY, RATE_LIMIT_PER_MINUTE
from src.ml.predictor import ReadmissionPredictor
from src.integrations.fhir import patient_features_to_fhir_risk_assessment
from src.integrations.feedback import ClinicianFeedbackStore
from src.monitoring.metrics import REQUESTS, LATENCY, PREDICTION_RISK, FEEDBACK, MODEL_LOADED
from pathlib import Path

app=FastAPI(title="Clinical Decision Intelligence API",version="3.0.0")
predictor=None
feedback_store=ClinicianFeedbackStore(Path("data/feedback/clinician_feedback.jsonl"))
requests_by_key=defaultdict(deque)

def authenticate(x_api_key: str=Header(default="")):
    if x_api_key != API_KEY: raise HTTPException(401,"Invalid API key")
    now=time.time(); q=requests_by_key[x_api_key]
    while q and q[0] < now-60: q.popleft()
    if len(q)>=RATE_LIMIT_PER_MINUTE: raise HTTPException(429,"Rate limit exceeded")
    q.append(now)

@app.on_event("startup")
def startup():
    global predictor
    predictor=ReadmissionPredictor(MODEL_PATH); MODEL_LOADED.set(1)

@app.get("/health")
def health(): return {"status":"ok","model_loaded":predictor is not None}

@app.get("/metrics")
def metrics(): return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)

def category(r): return "high" if r>=.7 else "moderate" if r>=.4 else "low"

@app.post("/v1/predict",response_model=PredictionResponse,dependencies=[Depends(authenticate)])
def predict(patient: PatientFeatures):
    start=time.perf_counter()
    try:
        risk=predictor.predict([patient.model_dump(exclude={"patient_id"})])[0]
        PREDICTION_RISK.observe(risk); REQUESTS.labels("predict","ok").inc()
        return PredictionResponse(patient_id=patient.patient_id,predicted_readmission_risk=risk,risk_category=category(risk))
    except Exception as exc:
        REQUESTS.labels("predict","error").inc(); raise HTTPException(400,str(exc))
    finally: LATENCY.labels("predict").observe(time.perf_counter()-start)

@app.post("/v1/predict/fhir",dependencies=[Depends(authenticate)])
def predict_fhir(patient: PatientFeatures):
    risk=predictor.predict([patient.model_dump(exclude={"patient_id"})])[0]
    return patient_features_to_fhir_risk_assessment(patient.patient_id,risk)

@app.post("/v1/feedback",dependencies=[Depends(authenticate)])
def feedback(item: FeedbackRequest):
    decision="accepted" if item.accepted else "rejected"; FEEDBACK.labels(decision).inc()
    return feedback_store.append(item.model_dump())
