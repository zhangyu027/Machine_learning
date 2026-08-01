# ADR-013: Apply classification-based retention and deletion

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Define retention by data classification and legal need; automate tiering, expiration, and verified deletion.

## Alternatives considered
Indefinite retention was rejected.

## Benefits and rationale
The policy controls cost and legal/privacy exposure.

## Risks and consequences
Deletion across derived products and backups requires lineage and orchestration.

## Revisit triggers
Revisit when regulation or legal hold policy changes.
