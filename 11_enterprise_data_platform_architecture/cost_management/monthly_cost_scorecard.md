# Monthly Cost Governance Scorecard

| Metric | Target | Escalation threshold | Owner |
|---|---:|---:|---|
| Cost per successful pipeline run | Baseline ±10% | Above baseline by 20% | Platform engineering |
| Compute utilization | 50–80% during scheduled windows | Under 25% for three periods | Workload owner |
| Idle interactive-cluster hours | Under 10 hours/month | Over 25 hours/month | Workspace administrator |
| Storage growth | Forecast ±10% | Unexplained growth above 20% | Domain owner |
| Untagged spend | 0% | Any untagged production resource | FinOps/platform owner |
| Premium storage older than policy | 0 TB | Any eligible data not tiered | Data-product owner |

## Required dimensions

- Environment
- Domain and data product
- Service and workspace
- Cost center
- Workload type
- Owner

Use showback by default. Introduce chargeback only when ownership and allocation quality are sufficiently reliable.
