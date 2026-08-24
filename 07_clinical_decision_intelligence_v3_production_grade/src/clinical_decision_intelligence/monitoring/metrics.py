from prometheus_client import Counter, Histogram, Gauge
REQUESTS = Counter("cdi_requests_total","Prediction requests",["endpoint","status"])
LATENCY = Histogram("cdi_request_latency_seconds","Prediction latency",["endpoint"])
PREDICTION_RISK = Histogram("cdi_predicted_readmission_risk","Predicted risk distribution",buckets=(.1,.2,.3,.4,.5,.6,.7,.8,.9,1.0))
FEEDBACK = Counter("cdi_clinician_feedback_total","Clinician feedback",["decision"])
MODEL_LOADED = Gauge("cdi_model_loaded","Whether the model loaded successfully")
