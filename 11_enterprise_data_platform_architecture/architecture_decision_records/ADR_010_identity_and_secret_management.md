# ADR-010: Use managed identities and Key Vault

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Use managed identities or workload federation for service access; store unavoidable secrets in Key Vault with rotation.

## Alternatives considered
Embedded secrets and long-lived service-principal credentials were rejected.

## Benefits and rationale
This reduces credential exposure and improves auditability.

## Risks and consequences
Some third-party connectors may still require managed secrets.

## Revisit triggers
Revisit as connector authentication capabilities evolve.
