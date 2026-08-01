# ADR-014: Centralize certified business metrics

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Publish certified metrics through governed Gold models and semantic layers rather than duplicating logic in reports.

## Alternatives considered
Dashboard-local metric logic was rejected.

## Benefits and rationale
This improves consistency, testing, and reuse.

## Risks and consequences
Semantic model ownership and release management are required.

## Revisit triggers
Revisit when domain-specific metric platforms are adopted.
