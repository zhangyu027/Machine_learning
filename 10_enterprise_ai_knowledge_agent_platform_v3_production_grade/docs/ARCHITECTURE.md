# Architecture

```text
Documents / image notes / approved SQL data
                ↓
Validated ingestion and chunking
                ↓
Stable embedding + versioned index lifecycle
                ↓
Router ────────────────┬───────────────┐
  ↓                    ↓               ↓
Document retrieval   Image notes   Safe SQL templates
  └────────────────────┴───────────────┘
                ↓
Prompt-injection screening
                ↓
Evidence-first answer + citations
                ↓
Confidence + grounding-risk heuristic
                ↓
FastAPI / metrics / audit-ready response
```
