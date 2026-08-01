# ADR-012: Version data contracts and govern breaking changes

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Permit backward-compatible additive changes in minor versions; require major versions, approvals, and notifications for breaking changes.

## Alternatives considered
Unversioned schemas and unrestricted evolution were rejected.

## Benefits and rationale
Consumers receive predictable compatibility and change windows.

## Risks and consequences
Contract governance adds process overhead.

## Revisit triggers
Revisit when automated compatibility enforcement is mature.
