from __future__ import annotations
import pandas as pd
import streamlit as st

from pharma_genai.pipeline_v3 import analyze_many_v3, dataframe_from_results, lookup_and_analyze

st.set_page_config(page_title="Pharmaceutical GenAI Drug Discovery V3", layout="wide")
st.title("Pharmaceutical GenAI Drug Discovery V3")
st.caption("GNN-ready molecular AI • Multi-task ADMET • Toxicity • Reliability • SHAP-style attribution • PubMed RAG • FastAPI/MLOps-ready")

with st.sidebar:
    st.header("V3 Enterprise Modules")
    st.markdown("""
    - RDKit feature engineering with fallback
    - GNN-ready graph embeddings
    - ChEMBL/PubChem/DrugBank integration layer
    - Multi-task ADMET and toxicity prediction
    - Conformal-style uncertainty intervals
    - SHAP-style explainability fallback
    - PubMed-style RAG evidence retrieval
    - FastAPI and MLflow-ready services
    """)
    include_lit = st.checkbox("Include literature RAG context", value=True)

smiles_text = st.text_area(
    "Enter SMILES, one per line",
    "CCO\nCC(=O)Oc1ccccc1C(=O)O\nCn1cnc2c1c(=O)n(C)c(=O)n2C",
    height=120,
)

compound_lookup = st.text_input("Optional compound lookup by name using PubChem/demo connector", "")

if st.button("Run V3 Enterprise Analysis", type="primary"):
    rows = []
    if compound_lookup.strip():
        try:
            rows.append(lookup_and_analyze(compound_lookup.strip()))
        except Exception as exc:
            st.warning(str(exc))
    rows.extend(analyze_many_v3([s.strip() for s in smiles_text.splitlines() if s.strip()], include_literature=include_lit))
    df = dataframe_from_results(rows)
    st.subheader("Ranked candidates")
    display_cols = [
        "smiles", "development_priority", "drug_likeness_score", "overall_toxicity_risk",
        "oral_absorption_probability", "bbb_penetration_probability", "cyp_inhibition_risk",
        "confidence_score", "uncertainty_score", "reliability_label", "graph_backend"
    ]
    st.dataframe(df[[c for c in display_cols if c in df.columns]], use_container_width=True)
    st.download_button("Download V3 CSV", df.to_csv(index=False).encode("utf-8"), "admet_v3_predictions.csv", "text/csv")

    for r in rows:
        with st.expander(f"{r['smiles']} — {r['development_priority']} / reliability: {r['reliability_label']}"):
            c1, c2 = st.columns(2)
            with c1:
                st.write("**Reliability explanation**")
                st.json(r.get("reliability_explanation", []))
                st.write("**Feature attributions**")
                st.dataframe(pd.DataFrame(r.get("feature_attributions", [])), use_container_width=True)
            with c2:
                st.write("**Graph embedding summary**")
                st.json({"backend": r.get("graph_backend"), "nodes": r.get("graph_n_nodes"), "edges": r.get("graph_n_edges"), "embedding": r.get("graph_embedding")})
                if include_lit and "literature_context" in r:
                    st.write("**PubMed-style RAG evidence**")
                    st.json(r["literature_context"]["evidence"])

st.info("Scientific disclaimer: this is a portfolio and decision-support prototype. It is not a validated clinical or regulatory system.")
