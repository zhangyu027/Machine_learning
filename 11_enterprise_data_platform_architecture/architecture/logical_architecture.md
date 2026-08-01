# Logical Architecture

```mermaid
flowchart LR
    subgraph Sources
      B[Batch files]
      S[Streams]
      A[APIs]
      D[Operational databases]
    end
    subgraph Control[Metadata and Control Plane]
      C[Data contracts]
      M[Pipeline metadata]
      Q[Quality rules]
      O[Orchestration]
    end
    subgraph Lakehouse
      R[Landing / quarantine / archive]
      Z1[Bronze]
      Z2[Silver]
      Z3[Gold data products]
    end
    subgraph Governance
      G[Catalog, glossary, lineage]
      I[Identity, secrets, policies]
      OBS[Logs, metrics, costs, SLOs]
    end
    subgraph Consumption
      BI[Semantic models / BI]
      AI[AI and feature consumers]
      SHARE[Governed sharing / APIs]
    end

    Sources --> R --> Z1 --> Z2 --> Z3 --> Consumption
    Control --> R
    Control --> Z1
    Control --> Z2
    Control --> Z3
    Governance -. governs .-> Lakehouse
    Governance -. observes .-> Consumption
```

## Design intent

The control plane drives ingestion, contracts, quality, and promotion. The data plane separates source-aligned, conformed, and consumption-ready assets. Governance and observability apply across every layer rather than being downstream add-ons.
