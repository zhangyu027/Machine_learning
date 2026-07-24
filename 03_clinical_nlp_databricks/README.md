# Clinical Trial Eligibility NLP — Databricks-Compatible Pipeline

A production-oriented portfolio project for clinical-note preprocessing, eligibility triage, transformer fine-tuning, structured LLM evaluation, model comparison, and API inference.

> **Safety:** This repository uses synthetic demonstration data. It is not a medical device and must not be used for autonomous clinical decisions.

## Architecture

```text
Clinical notes
   ↓
Spark / Databricks-compatible preprocessing
   ↓
Silver clean-text table
   ├── TF-IDF + Logistic Regression baseline
   ├── DistilBERT / ClinicalBERT fine-tuning
   └── GPT-compatible structured evaluator
   ↓
Metrics + honest comparison table
   ↓
FastAPI inference and human-review routing
```

## What is implemented

- Runnable TF-IDF baseline with Macro-F1, eligible-class recall, and measured latency
- Real Hugging Face DistilBERT training and evaluation script
- Optional ClinicalBERT training by changing `--model-name`
- GPT-compatible evaluator with strict JSON-schema output
- Genuine comparison table populated only by completed runs
- FastAPI inference for TF-IDF and saved DistilBERT artifacts
- Synthetic GitHub-safe data and smoke tests

## 1. Run the lightweight baseline

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
pytest -q
```

This produces `outputs/model_comparison.md`. Missing transformer or GPT runs remain explicitly marked **Not run**.

## 2. Train DistilBERT

```bash
pip install -r requirements-transformers.txt
python nlp_models/train_distilbert_classifier.py \
  --model-name distilbert-base-uncased \
  --epochs 2 \
  --batch-size 8
python evaluation/build_model_comparison.py
python evaluation/evaluate_models.py
```

ClinicalBERT alternative:

```bash
python nlp_models/train_distilbert_classifier.py \
  --model-name emilyalsentzer/Bio_ClinicalBERT \
  --epochs 2
```

The first run downloads model weights. Training on CPU can be slow; Databricks GPU compute is preferred.

## 3. Run the GPT-compatible structured evaluator

```bash
pip install -r requirements-gpt.txt
export OPENAI_API_KEY="..."
export GPT_MODEL="your-structured-output-capable-model"
# Optional for another OpenAI-compatible provider:
# export OPENAI_BASE_URL="https://provider.example/v1"

python llm/gpt_eligibility_evaluator.py \
  --note "Adult patient with documented diagnosis; required laboratory values are missing."

python llm/gpt_eligibility_evaluator.py --benchmark --limit 30
python evaluation/build_model_comparison.py
python evaluation/evaluate_models.py
```

The evaluator returns:

```json
{
  "eligibility": "needs_review",
  "confidence": 0.72,
  "matched_evidence": ["adult patient", "documented diagnosis"],
  "exclusion_evidence": [],
  "missing_information": ["required laboratory values"],
  "rationale": "Required criteria are incomplete.",
  "requires_human_review": true
}
```

## Comparison methodology

| Model | Macro-F1 | Eligible recall | Latency | Cost | Explainability |
|---|---:|---:|---:|---|---|
| TF-IDF | Measured locally | Measured locally | Measured locally | Low | High |
| DistilBERT | Added after a completed training run | Added after a completed run | Measured | Medium | Medium |
| GPT | Added after a credentialed benchmark | Added after a credentialed benchmark | Measured API latency | High | Medium |

No metric is filled with a fabricated value. Costs are qualitative tiers because actual API pricing and infrastructure costs vary over time and by provider.

## API

```bash
uvicorn api.app:app --reload
```

- `GET /health`
- `POST /predict`

Example:

```json
{
  "note_text": "Patient meets age criterion but laboratory values are missing.",
  "model": "tfidf"
}
```

## Interview positioning

A defensible explanation is:

> I started with an interpretable TF-IDF baseline, then implemented a fine-tunable DistilBERT path and a GPT-compatible structured evaluator. I compare Macro-F1, eligible-class recall, latency, cost tier, and explainability. The project deliberately leaves unavailable metrics as not run rather than presenting fabricated results. In a clinical workflow, low-confidence or incomplete cases are routed to human review.

## 4. Clinical entity extraction

The dependency-light extractor converts narrative notes into auditable structured fields:

- age
- diagnoses and negated diagnoses
- medications
- laboratory values and units
- recent hospitalization status
- missing-information flags
- source evidence snippets

```bash
python - <<'PY'
from clinical_entities.extractor import ClinicalEntityExtractor
print(ClinicalEntityExtractor().extract(
    "Patient age 58 with diabetes. HbA1c 8.2%. On metformin. No recent hospitalization."
).model_dump_json(indent=2))
PY
```

This rules-based implementation is transparent and fully runnable without model downloads. For real clinical deployment, it should be validated against annotated notes and may be augmented with scispaCy, MedCAT, or a fine-tuned clinical NER model.

## 5. Patient-to-trial matching

Trial definitions use explicit inclusion and exclusion criteria. Each criterion is evaluated independently and returned as:

- `matched_criteria`
- `failed_criteria`
- `unknown_criteria`

The final status is:

- `eligible` when all required criteria are satisfied
- `not_eligible` when at least one criterion fails
- `needs_review` when no criterion fails but required evidence is missing

```bash
python scripts/run_entity_matching_demo.py
```

The demo writes `outputs/trial_match_demo.json`. Trial examples are stored in `data/sample/trials.json`.

### Matching API endpoints

- `POST /entities`
- `POST /match-trial`
- `POST /rank-trials`

The matcher is deterministic and evidence-based. It does not replace clinician or trial-coordinator review.
