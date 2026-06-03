"""FastAPI service for V4 Principal Enterprise deployment."""

from __future__ import annotations

from typing import List

from fastapi import FastAPI
from pydantic import BaseModel, Field

from pharma_genai.pipeline_v4 import (
    analyze_many_v4,
    lookup_and_analyze,
)


class AnalyzeRequest(BaseModel):
    smiles: List[str] = Field(default_factory=lambda: ["CCO"])
    include_literature: bool = False


class LookupRequest(BaseModel):
    compound_name: str


app = FastAPI(
    title="Pharma GenAI Drug Discovery V4",
    version="4.0.0",
)


@app.get("/")
def root() -> dict:
    return {
        "project": "Pharma GenAI Drug Discovery V4",
        "version": "4.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health",
        "analyze": "/analyze",
        "lookup": "/lookup",
    }


@app.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "service": "pharma-genai-v4",
        "version": "4.0.0",
    }


@app.post("/analyze")
def analyze(req: AnalyzeRequest) -> dict:
    return {
        "results": analyze_many_v4(
            req.smiles,
            include_literature=req.include_literature,
        )
    }


@app.post("/lookup")
def lookup(req: LookupRequest):
    return lookup_and_analyze(req.compound_name)
