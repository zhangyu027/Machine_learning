from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agents.router import route_question
from rag.vector_store import search_vector_store
from rag.ollama_client import ask_ollama
from tools.sql_tool import safe_sql_agent
from tools.confidence import citation_confidence, hallucination_risk_check


def answer_question(
    question: str,
    index_dir: str = "vector_store",
    db_path: str = "data/sql/enterprise_agent.db",
    model_name: str = "llama3.2",
    top_k: int = 5,
    use_ollama: bool = True,
):
    route = route_question(question)
    evidence = []
    sql_result = None
    sql_query = None

    if route == "sql_agent":
        sql_query, sql_result = safe_sql_agent(question, db_path=db_path)
        evidence.append({
            "filename": "project_portfolio_metrics.csv",
            "chunk_index": "sql",
            "score": 1.0,
            "text": sql_result.to_string(index=False),
            "modality": "sql",
        })
    else:
        evidence = search_vector_store(question, index_dir=index_dir, top_k=top_k)

    confidence = citation_confidence(evidence)

    if use_ollama:
        answer = ask_ollama(question, evidence, model_name=model_name)
    else:
        answer = (
            "Ollama disabled. Retrieved evidence summary:\\n\\n"
            + "\\n\\n".join([
                f"{e.get('filename')} chunk {e.get('chunk_index')}: {e.get('text', '')[:400]}"
                for e in evidence
            ])
        )

    hallucination = hallucination_risk_check(answer, evidence)

    return {
        "route": route,
        "answer": answer,
        "evidence": evidence,
        "confidence": confidence,
        "hallucination": hallucination,
        "sql_query": sql_query,
        "sql_result": sql_result,
    }
