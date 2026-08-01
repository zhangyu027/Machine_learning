# ADR-009: Isolate development, test, and production

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Use separate identities, storage locations, catalogs, secrets, and deployment permissions for each environment.

## Alternatives considered
Shared environments with naming conventions were considered.

## Benefits and rationale
Isolation reduces accidental access and supports controlled promotion.

## Risks and consequences
Higher infrastructure cost and administration effort.

## Revisit triggers
Revisit only for low-risk sandbox workloads.
