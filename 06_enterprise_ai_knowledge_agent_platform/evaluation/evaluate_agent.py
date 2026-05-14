from pathlib import Path
import sys
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agents.orchestrator import answer_question


def evaluate_agent(eval_path="evaluation/eval_questions.csv", output_path="outputs/tables/agent_evaluation_results.csv"):
    df = pd.read_csv(eval_path)
    rows = []

    for _, row in df.iterrows():
        question = row["question"]
        expected = row["expected_source_keyword"]

        result = answer_question(question, use_ollama=False)

        evidence_sources = [item.get("filename", "") for item in result["evidence"]]
        hit = any(expected.lower() in source.lower() for source in evidence_sources)

        rows.append({
            "question": question,
            "expected_source_keyword": expected,
            "route": result["route"],
            "hit_in_sources": hit,
            "confidence_score": result["confidence"]["confidence_score"],
            "confidence_label": result["confidence"]["confidence_label"],
            "hallucination_risk": result["hallucination"]["risk_level"],
            "sources": ", ".join(evidence_sources),
        })

    out = pd.DataFrame(rows)
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(output_path, index=False)

    summary = pd.DataFrame([{
        "hit_rate": out["hit_in_sources"].mean(),
        "average_confidence": out["confidence_score"].mean(),
        "n_questions": len(out),
    }])
    summary.to_csv(output_path.parent / "agent_evaluation_summary.csv", index=False)

    print(summary)
    return out, summary


if __name__ == "__main__":
    evaluate_agent()
