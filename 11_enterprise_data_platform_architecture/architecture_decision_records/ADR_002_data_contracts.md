# ADR-002: Adopt Data Contracts for Critical Data Products

## Status
Accepted

## Context
Downstream reports, ML models, and APIs can break when schemas or business definitions change unexpectedly.

## Decision
Use data contracts for critical datasets.

## Contract Elements
- Dataset owner
- Consumer group
- Schema
- Required fields
- Grain
- Primary keys
- Allowed values
- Freshness expectation
- Quality rules
- Change notification process

## Consequences
- Producers and consumers share expectations.
- Breaking changes are easier to identify.
- Quality rules can be automated.
