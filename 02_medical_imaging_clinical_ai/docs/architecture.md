# Medical Imaging Clinical AI Architecture

## Data Flow

```text
Synthetic Imaging Metadata
        ↓
Bronze: raw imaging metadata and clinical attributes
        ↓
Silver: standardized imaging features and quality flags
        ↓
Gold: patient-imaging feature table
        ↓
Evaluation: baseline model metrics and governance summary
        ↓
Streamlit Review App
```

## Data Engineering Focus

The project demonstrates lakehouse-style data engineering for clinical AI: reproducible ingestion, standardization, feature-table generation, evaluation artifacts, and governance-ready documentation.
