# Disaster Recovery Strategy

## Objectives

- Critical-data RTO: 4 hours.
- Critical-data RPO: 24 hours.
- Metadata and configuration recovery: 2 hours.
- Recovery exercises: at least twice per year.

## Design

- Geo-redundant or cross-region replicated storage for critical Bronze and configuration assets.
- Infrastructure and policies reconstructed from version-controlled Terraform.
- Pipeline definitions and contract versions stored in Git and promoted through CI/CD.
- Catalog exports and critical glossary/ownership metadata backed up on a defined schedule.
- Idempotent pipelines capable of replay from immutable Bronze/archive data.
- Secondary-region capacity plan with documented dependencies and service limitations.

## Recovery sequence

1. Declare incident and identify affected region and dependencies.
2. Freeze writes where split-brain risk exists.
3. Deploy or activate secondary-region infrastructure.
4. Restore configuration, identities, metadata, and orchestration.
5. Replay data from the last verified recovery point.
6. Run contract, quality, reconciliation, and lineage validation.
7. Obtain product-owner approval before reopening consumption.
8. Complete post-incident review and update recovery evidence.
