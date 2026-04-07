# Architecture Graph

```mermaid
flowchart TD
    A[Input Medical Image] --> B[Image Preprocessing]
    M[Clinical Metadata JSON/CSV] --> N[Metadata Preprocessing]

    B --> C[CNN Backbone]
    N --> D[Metadata MLP Encoder]

    C --> E[Image Embedding]
    D --> F[Metadata Embedding]

    E --> G[Fusion Layer]
    F --> G

    G --> H[Base Classifier]
    G --> I[Embedding Store]

    I --> J[kNN / Similar Case Retrieval]
    J --> K[Neighbor Probability Aggregation]

    H --> L[Base Probability]
    K --> O[Graph-Refined Probability]

    L --> P[Final Blending]
    O --> P

    P --> Q[Prediction + Confidence]
    P --> R[FastAPI Output]
```

## Explanation

- **CNN Backbone** extracts image features.
- **Metadata Encoder** converts structured clinical fields into a dense embedding.
- **Fusion Layer** combines image and metadata signals.
- **Base Classifier** produces the primary prediction.
- **kNN / Similar Case Retrieval** approximates graph reasoning using nearest-neighbor evidence.
- **Final Blending** combines the base model and graph-refined evidence.

## Interview one-liner

> "This architecture progresses from image understanding to multimodal fusion and then to graph-inspired case retrieval for more clinically realistic decision support."
