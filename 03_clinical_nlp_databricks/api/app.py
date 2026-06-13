from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "baseline_tfidf.joblib"
app = FastAPI(title="Clinical NLP Databricks Demo API")

class NoteRequest(BaseModel):
    note_text: str

@app.get("/health")
def health():
    return {"status": "ok", "model_available": MODEL_PATH.exists()}

@app.post("/predict")
def predict(req: NoteRequest):
    if not MODEL_PATH.exists():
        return {"prediction": "needs_review", "warning": "model artifact not found; run local pipeline first"}
    model = load(MODEL_PATH)
    pred = model.predict([req.note_text])[0]
    return {"prediction": str(pred)}
