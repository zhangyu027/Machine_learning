import pandas as pd
import streamlit as st
from pharma_genai.pipeline import analyze_smiles, analyze_many

st.set_page_config(page_title="Pharma GenAI V2", layout="wide")
st.title("Pharmaceutical GenAI Drug Discovery V2")
st.caption("ADMET prediction • Molecular property prediction • Toxicity risk • RDKit feature engineering • Reliability scoring")

smiles_text = st.text_area("Enter SMILES, one per line", "CCO\nCC(=O)Oc1ccccc1C(=O)O\nCn1cnc2c1c(=O)n(C)c(=O)n2C")
if st.button("Run ADMET Reliability Analysis"):
    smiles=[s.strip() for s in smiles_text.splitlines() if s.strip()]
    df=analyze_many(smiles)
    st.subheader("Ranked candidates")
    st.dataframe(df[["smiles","development_priority","drug_likeness_score","overall_toxicity_risk","oral_absorption_probability","confidence_score","reliability_label","domain_applicability","mol_wt","logp","tpsa","qed"]], use_container_width=True)
    st.download_button("Download CSV", df.to_csv(index=False), file_name="admet_v2_predictions.csv")
    for _, row in df.iterrows():
        with st.expander(f"{row['smiles']} — {row['development_priority']} / reliability: {row['reliability_label']}"):
            st.write("Notes:", row.get("notes", []))
            st.write("Reliability explanation:", row.get("explanation", []))
