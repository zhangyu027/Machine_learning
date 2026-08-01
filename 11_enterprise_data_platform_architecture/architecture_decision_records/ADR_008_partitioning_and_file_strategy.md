# ADR-008: Standardize partitioning and file-size strategy

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Partition primarily by stable, commonly filtered date attributes and compact small files toward 256 MB–1 GB targets where practical.

## Alternatives considered
High-cardinality business partitions and unpartitioned storage were considered.

## Benefits and rationale
The standard reduces scans and metadata overhead without over-partitioning.

## Risks and consequences
Workloads with unusual access patterns require approved exceptions.

## Revisit triggers
Revisit using observed query and storage metrics.
