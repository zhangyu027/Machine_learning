from pathlib import Path
import pandas as pd
import streamlit as st
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from rag.document_loader import load_documents, create_chunks
from rag.vector_store import build_faiss_index, search_index
from rag.ollama_client import ask_ollama


st.set_page_config(page_title="Personal AI Assistant RAG System", layout="wide")

st.title("Personal AI Assistant RAG System")
st.caption("Local RAG assistant for private documents using Ollama, sentence-transformers, and FAISS.")

st.markdown("""
### Project question

**Can a local RAG assistant answer questions from private documents without sending data to paid cloud APIs?**
""")

DATA_DIR = ROOT / "data" / "uploaded_documents"
INDEX_DIR = ROOT / "vector_store"
DATA_DIR.mkdir(parents=True, exist_ok=True)
INDEX_DIR.mkdir(parents=True, exist_ok=True)

with st.sidebar:
    st.header("Settings")
    ollama_model = st.text_input("Ollama model", value="llama3.2")
    embedding_model = st.text_input("Embedding model", value="all-MiniLM-L6-v2")
    top_k = st.slider("Top-k retrieved chunks", min_value=1, max_value=10, value=5)
    chunk_size = st.slider("Chunk size", min_value=300, max_value=2000, value=900, step=100)
    chunk_overlap = st.slider("Chunk overlap", min_value=0, max_value=500, value=150, step=50)

tab_upload, tab_chat, tab_eval = st.tabs([
    "1. Upload & Index Documents",
    "2. Ask Questions",
    "3. Retrieval Evaluation"
])

with tab_upload:
    st.subheader("Upload local documents")
    uploaded_files = st.file_uploader(
        "Upload .txt or .pdf documents",
        type=["txt", "pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:
        for uploaded_file in uploaded_files:
            out_path = DATA_DIR / uploaded_file.name
            out_path.write_bytes(uploaded_file.getvalue())
        st.success(f"Saved {len(uploaded_files)} file(s) to {DATA_DIR}")

    st.write("Current document folder:", str(DATA_DIR))

    if st.button("Build / Rebuild FAISS Index"):
        documents = load_documents(str(DATA_DIR))

        if not documents:
            st.warning("No supported documents found. Upload .txt or .pdf files first.")
        else:
            chunks = create_chunks(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            build_faiss_index(chunks, str(INDEX_DIR), embedding_model_name=embedding_model)

            st.success(f"Indexed {len(documents)} document(s) into {len(chunks)} chunks.")
            st.write("Vector store:", str(INDEX_DIR))

with tab_chat:
    st.subheader("Ask questions from your private documents")

    question = st.text_input("Question", placeholder="What is this project about?")

    if st.button("Ask") and question:
        try:
            results = search_index(question, str(INDEX_DIR), top_k=top_k)
            answer = ask_ollama(question, results, model_name=ollama_model)

            st.markdown("### Answer")
            st.write(answer)

            st.markdown("### Retrieved sources")
            source_rows = []
            for item in results:
                source_rows.append({
                    "rank": item["rank"],
                    "filename": item["filename"],
                    "chunk_index": item["chunk_index"],
                    "score": round(item["score"], 4),
                    "preview": item["text"][:300]
                })

            st.dataframe(pd.DataFrame(source_rows), use_container_width=True)

            with st.expander("View full retrieved context"):
                for item in results:
                    st.markdown(f"**{item['rank']}. {item['filename']} — chunk {item['chunk_index']} — score {item['score']:.3f}**")
                    st.write(item["text"])

        except Exception as exc:
            st.error(str(exc))
            st.info("Make sure Ollama is running and the FAISS index has been built.")

with tab_eval:
    st.subheader("Retrieval evaluation")

    st.markdown("""
    This page evaluates whether the correct source appears in the top-k retrieved chunks.
    Add test questions below with expected source keywords.
    """)

    sample_eval = pd.DataFrame({
        "question": [
            "What is the project question?",
            "What tools does the local RAG system use?",
            "How can retrieval quality be evaluated?"
        ],
        "expected_source_keyword": [
            "personal_ai_assistant_overview",
            "personal_ai_assistant_overview",
            "rag_evaluation_notes"
        ]
    })

    edited_eval = st.data_editor(sample_eval, num_rows="dynamic", use_container_width=True)

    if st.button("Run retrieval evaluation"):
        rows = []

        for _, row in edited_eval.iterrows():
            q = str(row["question"])
            expected = str(row["expected_source_keyword"])

            results = search_index(q, str(INDEX_DIR), top_k=top_k)
            retrieved_sources = [item["filename"] for item in results]
            hit = any(expected in source for source in retrieved_sources)

            rows.append({
                "question": q,
                "expected_source_keyword": expected,
                "hit_in_top_k": hit,
                "top_sources": ", ".join(retrieved_sources)
            })

        eval_df = pd.DataFrame(rows)
        hit_rate = eval_df["hit_in_top_k"].mean() if len(eval_df) else 0

        st.metric("Top-k hit rate", f"{hit_rate:.1%}")
        st.dataframe(eval_df, use_container_width=True)
