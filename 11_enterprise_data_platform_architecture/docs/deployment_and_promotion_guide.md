# Deployment and Promotion Guide

## Reference workflow

1. Create a feature branch and update code, contract, ADR, or infrastructure.
2. Open a pull request with validation evidence and impact assessment.
3. Run documentation tests, reference tests, linting, Terraform formatting, policy checks, and secret scanning.
4. Build immutable artifacts and apply to development.
5. Validate contracts, quality, lineage, access, observability, cost tags, and rollback.
6. Promote the same artifact to test and production through approvals.
7. Monitor release health and record deployment evidence.

## Environment rules

- No direct production changes.
- Separate identities, storage, catalogs, workspaces, secrets, and state.
- Production secrets come from Key Vault; no repository or CI plaintext secrets.
- Breaking contract changes require major versions and consumer approval.
- Emergency changes require an incident/change record and retrospective.
