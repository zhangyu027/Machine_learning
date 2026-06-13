# ADR-004: Use Metadata Catalog and Lineage

## Status
Accepted

## Context
Enterprise consumers need to discover datasets, understand definitions, and trace data movement.

## Decision
Use Microsoft Purview or an equivalent metadata platform to manage cataloging, classification, lineage, glossary, and data discovery.

## Capabilities
- Dataset catalog
- Business glossary
- Lineage across pipelines
- PII classification
- Ownership metadata
- Data discovery

## Consequences
- Users can find trusted data.
- Data lineage supports audit and troubleshooting.
- Sensitive data can be classified and governed.
