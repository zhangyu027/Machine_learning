# ADR-011: Adopt replay-based disaster recovery

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Recover pipelines from version-controlled infrastructure and replay immutable Bronze data to meet defined RTO/RPO targets.

## Alternatives considered
Full hot-hot duplication and backup-only recovery were considered.

## Benefits and rationale
Replay-based recovery balances cost and resilience for analytical workloads.

## Risks and consequences
Recovery speed depends on retained source history and compute availability.

## Revisit triggers
Revisit for tier-0 workloads with stricter continuity requirements.
