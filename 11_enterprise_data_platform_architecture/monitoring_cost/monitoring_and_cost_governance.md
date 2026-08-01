# Monitoring, Observability, and Cost Governance

## Telemetry domains

| Domain | Examples |
|---|---|
| Platform | Service availability, capacity, authentication failures |
| Pipeline | Status, duration, retries, error category, correlation ID |
| Data | Volume, freshness, contract compatibility, quality results |
| Consumption | Query latency, usage, certified-product adoption |
| Security | Privileged access, policy denial, exfiltration indicators |
| Cost | Cost per run, domain spend, idle compute, storage growth |

## Alerting policy

- Critical: page on-call and create incident automatically.
- High: notify owning team and require acknowledgement within the SLO.
- Medium: create backlog item and include in weekly reliability review.
- Low: retain for trend analysis.

Alerts must identify the environment, data product, run ID, owner, failure category, and runbook link.

## Cost controls

- Mandatory owner, environment, domain, and cost-center tags.
- Auto-termination for interactive compute and job-cluster preference for scheduled work.
- Partition and compaction standards driven by measured access patterns.
- Lifecycle policies for archive and deletion.
- Budget alerts with showback by domain/data product.
- Monthly FinOps review using `cost_management/monthly_cost_scorecard.md`.
