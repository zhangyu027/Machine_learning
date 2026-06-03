from pathlib import Path
import sys
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from agents.orchestrator import answer_question

st.set_page_config(page_title="Enterprise AI Knowledge Agent Platform", layout="wide")

st.title("Enterprise AI Knowledge Agent Platform")
st.caption("Local/private RAG + SQL agent + image notes + confidence scoring + hallucination checks")

st.markdown("""
## Project Question

**Can a private enterprise AI agent platform answer questions across documents, SQL tables, and image notes with citations, confidence scoring, and hallucination checks?**
""")

with st.sidebar:
    st.header("Settings")
    model_name = st.text_input("Ollama model", value="llama3.2")
    use_ollama = st.checkbox("Use Ollama", value=False)
    top_k = st.slider("Top-k evidence chunks", 1, 10, 5)

tab_agent, tab_eval, tab_arch = st.tabs(["Ask Agent", "Evaluation", "Architecture"])

with tab_agent:
    question = st.text_input("Ask a question", value="Which portfolio projects have the highest priority and why?")

    if st.button("Run Agent"):
        result = answer_question(question, model_name=model_name, top_k=top_k, use_ollama=use_ollama)

        st.subheader("Agent Route")
        st.write(result["route"])

        st.subheader("Answer")
        st.write(result["answer"])

        st.subheader("Citation Confidence")
        st.json(result["confidence"])

        st.subheader("Hallucination Risk")
        st.json(result["hallucination"])

        st.subheader("Evidence")
        rows = []
        for item in result["evidence"]:
            rows.append({
                "filename": item.get("filename"),
                "chunk_index": item.get("chunk_index"),
                "score": round(float(item.get("score", 0)), 3),
                "modality": item.get("modality"),
                "preview": item.get("text", "")[:300],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        if result["sql_query"]:
            st.subheader("SQL Query")
            st.code(result["sql_query"], language="sql")
            st.dataframe(result["sql_result"], use_container_width=True)

with tab_eval:
    eval_path = ROOT / "outputs/tables/agent_evaluation_results.csv"
    summary_path = ROOT / "outputs/tables/agent_evaluation_summary.csv"

    st.markdown("Run evaluation first:")
    st.code("python evaluation/evaluate_agent.py")

    if summary_path.exists():
        st.subheader("Evaluation Summary")
        st.dataframe(pd.read_csv(summary_path), use_container_width=True)

    if eval_path.exists():
        st.subheader("Evaluation Results")
        st.dataframe(pd.read_csv(eval_path), use_container_width=True)

with tab_arch:
    st.markdown((ROOT / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8"))
