"""FastAPI service for V3 enterprise deployment."""
from __future__ import annotations
from typing import List
from pydantic import BaseModel, Field
from fastapi import FastAPI

from pharma_genai.pipeline_v3 import analyze_many_v3, lookup_and_analyze


class AnalyzeRequest(BaseModel):
    smiles: List[str] = Field(default_factory=lambda: ["CCO"])
    include_literature: bool = False


class LookupRequest(BaseModel):
    compound_name: str


app = FastAPI(title="Pharma GenAI Drug Discovery V4", version="3.0.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "pharma-genai-v3"}


@app.post("/analyze")
def analyze(req: AnalyzeRequest) -> dict:
    return {"results": analyze_many_v3(req.smiles, include_literature=req.include_literature)}


@app.post("/lookup")
def lookup(req: LookupRequest) -> dict:
    return lookup_and_analyze(req.compound_name)
