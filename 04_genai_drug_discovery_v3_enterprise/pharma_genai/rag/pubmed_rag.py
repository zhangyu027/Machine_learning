"""PubMed-style Retrieval Augmented Generation layer.

The implementation is fully offline for portfolio demos. It can be replaced with
PubMed/Entrez search and vector databases in production.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class LiteratureChunk:
    source: str
    title: str
    text: str
    url: str = ""


DEFAULT_CORPUS = [
    LiteratureChunk("PubMed-demo", "ADMET screening in early discovery", "ADMET and toxicity filters are used early in drug discovery to reduce downstream attrition from poor pharmacokinetics or safety risks."),
    LiteratureChunk("PubMed-demo", "Graph neural networks for molecular property prediction", "Graph neural networks represent atoms as nodes and bonds as edges, enabling learned molecular representations for property prediction."),
    LiteratureChunk("PubMed-demo", "Uncertainty estimation for pharmaceutical ML", "Applicability domain, ensemble disagreement, Bayesian methods, and conformal prediction can help quantify reliability of computational predictions."),
    LiteratureChunk("PubMed-demo", "Explainable AI in chemistry", "SHAP and substructure attribution help scientists interpret model decisions and identify molecular features contributing to predicted risk."),
]


class PubMedRAG:
    def __init__(self, corpus: List[LiteratureChunk] | None = None):
        self.corpus = corpus or DEFAULT_CORPUS
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.matrix = self.vectorizer.fit_transform([c.title + " " + c.text for c in self.corpus])

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, object]]:
        q = self.vectorizer.transform([query])
        sims = cosine_similarity(q, self.matrix)[0]
        idxs = sims.argsort()[::-1][:k]
        results = []
        for i in idxs:
            row = asdict(self.corpus[int(i)])
            row["score"] = round(float(sims[int(i)]), 3)
            results.append(row)
        return results

    def answer(self, query: str) -> Dict[str, object]:
        chunks = self.retrieve(query)
        summary = " ".join([c["text"] for c in chunks])
        return {"query": query, "summary": summary, "evidence": chunks}
