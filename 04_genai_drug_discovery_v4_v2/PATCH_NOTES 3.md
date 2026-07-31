# V4 Repair Package

This package contains replacement and new files for the uploaded V4 project.
Copy the contents into the root of `04_genai_drug_discovery_v4_v2` while preserving paths.

## Implemented
1. Notebook unpacks all three evaluation return values.
2. Streamlit export is `admet_v4_predictions.csv`.
3. V4 no longer catches all exceptions or delegates to V3.
4. Added one Pydantic result schema.
5. V4 explicitly orchestrates ADMET, graph, explainability, literature, and lookup components.
6. Added RDKit validation/canonicalization/QED/Morgan diversity with explicit no-RDKit fallback.
7. Generator loss ignores padding and reports average epoch loss.
8. Split core, development, ML, and optional requirements.
9. Added output-directory and input-column validation.
10. Added focused tests.

## Important
The complete repository was not uploaded, so this patch assumes the existing modules imported by `pipeline_v4.py` remain at their current paths. Run the commands in `VALIDATION.md` from the repository root.
