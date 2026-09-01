# V4.1 Documentation Index

This folder is reorganized for scientific review, portfolio use, setup, and release management.

## 00_overview
- `README_V4.1.md` — snapshot of the project README included with this documentation package.

## 01_scientific
- `SCIENTIFIC_METHODOLOGY.md` — completed experimental protocol and final benchmark interpretation.
- `LIMITATIONS.md` — scientific, data, modeling, evaluation, and validation limitations.
- `DATA_CARD.md` — dataset expectations and leakage controls.
- `MODEL_CARD.md` — intended use, validation expectations, and human oversight.
- `EXPERIMENT_REPORT_LEGACY.md` — earlier pre-benchmark experiment plan retained for provenance.

## 02_validation
- `VALIDATION.md`
- `DATA_README.md`

## 03_portfolio
- `V4_EXECUTIVE_NARRATIVE.md` — concise updated interview narrative.
- `Drug_Discovery_V4.1_Scientific_Interview_Narrative.docx` — updated polished interview report with actual V4.1 benchmark findings.
- `Drug_Discovery_V4_Enterprise_Presentation.pptx` — existing presentation retained unchanged.

## 04_setup
Installation notes and dependency lists.

## 05_release
GitHub checklist and historical patch notes.

## examples
End-to-end demonstration notebook.

## Current scientific status

The classical, multi-task Morgan MLP, and GraphConv GNN benchmark phases are complete for hERG, BBBP, ClinTox, and Tox21. Classical models won 23 of 24 endpoint × metric comparisons. The multi-task model's one win was Tox21 average precision. External/temporal validation remains future work.
