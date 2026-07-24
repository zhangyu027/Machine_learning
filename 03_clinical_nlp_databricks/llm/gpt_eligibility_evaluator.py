"""GPT-compatible clinical eligibility evaluator with strict structured JSON output.

Supports OpenAI-compatible chat-completions clients. No clinical decision should be made
without qualified human review; this module is an interview demonstration only.
"""
from __future__ import annotations

import argparse
import json
import os
import time
from pathlib import Path
from typing import Literal

import pandas as pd
from pydantic import BaseModel, Field
from sklearn.metrics import accuracy_score, f1_score, recall_score

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "outputs" / "clinical_notes_processed.csv"
METRICS_PATH = ROOT / "outputs" / "gpt_metrics.json"
PREDICTIONS_PATH = ROOT / "outputs" / "gpt_predictions.csv"


class EligibilityResult(BaseModel):
    eligibility: Literal["eligible", "not_eligible", "needs_review"]
    confidence: float = Field(ge=0.0, le=1.0)
    matched_evidence: list[str]
    exclusion_evidence: list[str]
    missing_information: list[str]
    rationale: str
    requires_human_review: bool


SYSTEM_PROMPT = """You are a clinical-trial eligibility triage assistant.
Classify the note as eligible, not_eligible, or needs_review.
Use only information explicitly present in the note. Never invent medical facts.
When information is missing or ambiguous, choose needs_review.
Return JSON that exactly matches the provided schema. This is decision support only and
must always allow qualified human review."""


def build_user_prompt(note_text: str) -> str:
    return f"Clinical note:\n{note_text}\n\nEvaluate eligibility and return structured JSON."


def evaluate_note(note_text: str, model: str) -> tuple[EligibilityResult, float]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("Install the OpenAI client: pip install openai") from exc

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL") or None,
    )
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(note_text)},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "clinical_eligibility_result",
                "strict": True,
                "schema": EligibilityResult.model_json_schema(),
            },
        },
        temperature=0,
    )
    elapsed_ms = (time.perf_counter() - start) * 1000
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError("The model returned an empty response.")
    return EligibilityResult.model_validate_json(content), elapsed_ms


def benchmark(model: str, limit: int | None = None) -> None:
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is required for a genuine GPT benchmark.")
    df = pd.read_csv(DATA_PATH)
    if limit:
        df = df.head(limit)
    rows = []
    for row in df.itertuples(index=False):
        result, latency_ms = evaluate_note(str(row.clean_text), model)
        rows.append({
            "note_text": row.clean_text,
            "label": row.label,
            "prediction": result.eligibility,
            "confidence": result.confidence,
            "latency_ms": latency_ms,
            "structured_result": result.model_dump_json(),
        })
    pred_df = pd.DataFrame(rows)
    pred_df.to_csv(PREDICTIONS_PATH, index=False)
    metrics = {
        "status": "completed",
        "model_name": model,
        "accuracy": float(accuracy_score(pred_df.label, pred_df.prediction)),
        "macro_f1": float(f1_score(pred_df.label, pred_df.prediction, average="macro")),
        "eligible_recall": float(recall_score(
            pred_df.label, pred_df.prediction, labels=["eligible"], average="macro", zero_division=0
        )),
        "latency_ms_per_note": float(pred_df.latency_ms.mean()),
        "evaluated_rows": int(len(pred_df)),
        "cost_tier": "High",
        "explainability": "Medium",
        "cost_note": "Actual cost depends on provider, model, token volume, and date of execution.",
        "data_type": "synthetic_demo_data",
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default=os.environ.get("GPT_MODEL", "gpt-4.1-mini"))
    parser.add_argument("--note")
    parser.add_argument("--benchmark", action="store_true")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()
    if args.note:
        result, latency_ms = evaluate_note(args.note, args.model)
        print(json.dumps({**result.model_dump(), "latency_ms": latency_ms}, indent=2))
    elif args.benchmark:
        benchmark(args.model, args.limit)
    else:
        parser.error("Provide --note or --benchmark")


if __name__ == "__main__":
    main()
