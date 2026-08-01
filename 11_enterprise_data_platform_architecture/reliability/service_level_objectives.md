# Reliability Model and Service-Level Objectives

| Capability | SLI | SLO | Error-budget response |
|---|---|---:|---|
| Critical daily data product | Successful on-time publications / expected publications | 99.5% monthly | Freeze nonessential releases when budget is exhausted |
| Freshness | Age of latest accepted Gold partition | Under 24 hours for 99% of observations | Escalate to product owner and incident queue |
| Pipeline acknowledgement | Time from critical alert to human acknowledgement | Under 15 minutes for 95% of incidents | Review on-call coverage and alert routing |
| Recovery time | Time to restore critical publication | Under 4 hours | Invoke recovery runbook and executive notification |
| Recovery point | Maximum accepted data loss | 24 hours | Restore from immutable Bronze/archive data |
| Critical quality pass rate | Critical checks passed / executed | 100% | Quarantine and stop publication |
| Lineage coverage | Governed production assets with current lineage | At least 95% | Block certification of uncovered critical assets |

SLAs are external commitments. SLOs are internal reliability targets. SLIs are measured signals. Error budgets govern how much unreliability is accepted before reliability work takes precedence over feature delivery.
