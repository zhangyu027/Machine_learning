# Critical Daily Publication Runbook

## Service

`public_health.gold_daily_program_metrics`

## Detection

- Pipeline failure alert
- Critical quality rule failure
- Freshness SLO breach
- Consumer reconciliation failure

## Immediate triage

1. Acknowledge within 15 minutes.
2. Confirm latest successful partition and affected consumers.
3. Classify the incident as source, infrastructure, transformation, quality, or publication failure.
4. Quarantine suspect output and prevent certification/publication.

## Recovery

- Source issue: preserve evidence and coordinate retransmission.
- Infrastructure issue: retry only after dependency health is confirmed.
- Transformation defect: deploy approved rollback or hotfix through emergency change control.
- Data defect: replay from immutable Bronze after corrected input or rule approval.
- Publication defect: republish the verified Gold partition and invalidate downstream caches.

## Closure evidence

- Reconciliation and critical quality checks passed.
- Lineage and run metadata persisted.
- Product owner and consumers notified.
- Incident record includes root cause, duration, impact, and corrective actions.
