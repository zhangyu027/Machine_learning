from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
import pandas as pd



def reciprocal_rank(results: list[dict], expected: str) -> float:
    for item in results:
        if expected.lower() in item["filename"].lower():
            return 1.0 / item["rank"]
    return 0.0


def token_overlap(answer: str, context: str) -> float:
    answer_tokens = set(re.findall(r"\w+", answer.lower()))
    context_tokens = set(re.findall(r"\w+", context.lower()))
    return len(answer_tokens & context_tokens) / max(len(answer_tokens), 1)


def citation_rate(answer: str, results: list[dict]) -> float:
    """Check whether an answer cites at least one actual retrieved source/chunk."""
    citations = re.findall(
        r"\[Source:\s*([^|\]]+?)\s*\|\s*Chunk:\s*(\d+)\s*\]",
        answer,
        re.I,
    )
    valid = {
        (str(item["filename"]).strip().lower(), int(item["chunk_index"]))
        for item in results
    }
    return float(any((name.strip().lower(), int(chunk)) in valid for name, chunk in citations))

def evaluate(eval_file: str, index_dir: str, top_k: int, model: str, generate_answers: bool):
    from rag.ollama_client import ask_ollama
    from rag.vector_store import search_index
    df = pd.read_csv(eval_file)
    from rag.vector_store import load_faiss_index
    required = {"question", "expected_source_keyword"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Evaluation CSV missing columns: {sorted(missing)}")
    _, metadata = load_faiss_index(index_dir)
    filenames = {str(chunk["filename"]).lower() for chunk in metadata["chunks"]}
    expected = {str(v).strip().lower() for v in df["expected_source_keyword"].dropna() if str(v).strip()}
    absent = sorted(v for v in expected if not any(v in name for name in filenames))
    if absent:
        raise ValueError(
            f"Evaluation/index mismatch: no indexed filenames match {absent}. "
            f"Indexed filenames: {sorted(filenames)}. "
            "Build the sample index using --input-dir data/sample_documents "
            "--index-dir vector_store_eval and evaluate against vector_store_eval."
        )
    rows = []
    for _, row in df.iterrows():
        question = str(row["question"])
        expected = str(row["expected_source_keyword"])
        results = search_index(question, index_dir, top_k=top_k)
        relevant = [expected.lower() in item["filename"].lower() for item in results]
        recall_at_k = float(any(relevant))
        precision_at_k = sum(relevant) / max(len(results), 1)
        mrr = reciprocal_rank(results, expected)
        hit_at_1 = float(any(relevant[:1]))
        hit_at_3 = float(any(relevant[:3]))

        answer = ""
        groundedness = None
        has_citation = None
        if generate_answers:
            answer = ask_ollama(question, results, model_name=model)
            context = " ".join(item["text"] for item in results)
            groundedness = token_overlap(answer, context)
            has_citation = citation_rate(answer, results)

        rows.append({
            "question": question,
            "expected_source_keyword": expected,
            "recall_at_k": recall_at_k,
            "precision_at_k": precision_at_k,
            "reciprocal_rank": mrr,
            "hit_at_1": hit_at_1,
            "hit_at_3": hit_at_3,
            "groundedness_proxy": groundedness,
            "citation_present": has_citation,
            "top_sources": ", ".join(item["filename"] for item in results),
            "answer": answer,
        })

    out = pd.DataFrame(rows)
    summary = {
        "questions": len(out),
        "recall_at_k": float(out["recall_at_k"].mean()) if len(out) else 0,
        "precision_at_k": float(out["precision_at_k"].mean()) if len(out) else 0,
        "mrr": float(out["reciprocal_rank"].mean()) if len(out) else 0,
        "hit_at_1": float(out["hit_at_1"].mean()) if len(out) else 0,
        "hit_at_3": float(out["hit_at_3"].mean()) if len(out) else 0,
        "groundedness_proxy": float(out["groundedness_proxy"].mean()) if generate_answers and len(out) else None,
        "citation_rate": float(out["citation_present"].mean()) if generate_answers and len(out) else None,
    }
    output_dir = Path(__file__).resolve().parent
    out.to_csv(output_dir / "rag_evaluation_results.csv", index=False)
    (output_dir / "rag_evaluation_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return out, summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-file", default="evaluation/sample_eval_questions.csv")
    parser.add_argument("--index-dir", default="vector_store")
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--model", default="llama3.2")
    parser.add_argument("--generate-answers", action="store_true")
    args = parser.parse_args()
    evaluate(args.eval_file, args.index_dir, args.top_k, args.model, args.generate_answers)
