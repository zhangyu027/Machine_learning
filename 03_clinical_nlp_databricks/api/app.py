from pathlib import Path
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from clinical_entities.extractor import ClinicalEntityExtractor
from trial_matching.matcher import TrialDefinition, TrialMatcher
from joblib import load

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "models" / "baseline_tfidf.joblib"
DISTILBERT_PATH = ROOT / "models" / "distilbert_clinical_eligibility"
app = FastAPI(title="Clinical NLP Eligibility API", version="3.0")
entity_extractor = ClinicalEntityExtractor()
trial_matcher = TrialMatcher(entity_extractor)


class NoteRequest(BaseModel):
    note_text: str = Field(min_length=3, max_length=20000)
    model: Literal["tfidf", "distilbert"] = "tfidf"


class EntityRequest(BaseModel):
    note_text: str = Field(min_length=3, max_length=20000)


class TrialMatchRequest(BaseModel):
    note_text: str = Field(min_length=3, max_length=20000)
    trial: TrialDefinition


class TrialRankRequest(BaseModel):
    note_text: str = Field(min_length=3, max_length=20000)
    trials: list[TrialDefinition] = Field(min_length=1, max_length=100)


@app.get("/health")
def health():
    return {
        "status": "ok",
        "models": {
            "tfidf": BASELINE_PATH.exists(),
            "distilbert": DISTILBERT_PATH.exists(),
        },
    }


@app.post("/predict")
def predict(req: NoteRequest):
    if req.model == "tfidf":
        if not BASELINE_PATH.exists():
            raise HTTPException(status_code=503, detail="TF-IDF artifact not found; run the baseline pipeline")
        model = load(BASELINE_PATH)
        probabilities = model.predict_proba([req.note_text])[0]
        classes = model.classes_
        idx = int(probabilities.argmax())
        return {
            "model": "tfidf",
            "prediction": str(classes[idx]),
            "confidence": float(probabilities[idx]),
            "probabilities": {str(label): float(prob) for label, prob in zip(classes, probabilities)},
            "requires_human_review": str(classes[idx]) == "needs_review",
        }

    if not DISTILBERT_PATH.exists():
        raise HTTPException(status_code=503, detail="DistilBERT artifact not found; run transformer training")
    try:
        from transformers import pipeline
    except ImportError as exc:
        raise HTTPException(status_code=503, detail="Install transformer dependencies") from exc
    classifier = pipeline("text-classification", model=str(DISTILBERT_PATH), tokenizer=str(DISTILBERT_PATH), top_k=None)
    scores = classifier(req.note_text, truncation=True)[0]
    best = max(scores, key=lambda x: x["score"])
    return {
        "model": "distilbert",
        "prediction": best["label"],
        "confidence": float(best["score"]),
        "probabilities": {item["label"]: float(item["score"]) for item in scores},
        "requires_human_review": best["label"] == "needs_review",
    }


@app.post("/entities")
def extract_entities(req: EntityRequest):
    return entity_extractor.extract(req.note_text).model_dump()


@app.post("/match-trial")
def match_trial(req: TrialMatchRequest):
    return trial_matcher.match(req.note_text, req.trial).model_dump()


@app.post("/rank-trials")
def rank_trials(req: TrialRankRequest):
    return {"results": [result.model_dump() for result in trial_matcher.rank(req.note_text, req.trials)]}
