# ADR-015: Standardize operational, data, and cost telemetry

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Capture pipeline, quality, freshness, lineage, security, and cost signals with shared correlation identifiers.

## Alternatives considered
Tool-specific isolated monitoring was rejected.

## Benefits and rationale
Unified telemetry accelerates diagnosis and enables SLO and FinOps reporting.

## Risks and consequences
Telemetry cost and retention require governance.

## Revisit triggers
Revisit annually based on incident and cost evidence.
