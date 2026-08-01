# ADR-007: Use batch by default and streaming only for justified latency requirements

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Default to scheduled micro-batch or batch pipelines. Adopt streaming when a documented business SLO cannot be met by batch.

## Alternatives considered
Universal streaming and universal batch were considered.

## Benefits and rationale
This controls operational complexity while preserving a path for low-latency products.

## Risks and consequences
Two operating patterns require separate observability and support skills.

## Revisit triggers
Revisit for products with measured sub-hour latency demand.
