# Executable Reference Implementation

This small, dependency-light implementation demonstrates the architecture patterns described by the repository:

- JSON data contracts
- Bronze/Silver/Gold processing
- severity-aware data quality
- lineage manifests and source hashes
- pipeline-run metadata
- deterministic test coverage

Run from the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e reference_implementation
enterprise-platform-demo --config reference_implementation/config/sample_pipeline.json
pytest -q reference_implementation/tests
```

The example is intentionally local and synthetic. Azure services remain the target production architecture, not a claim of live deployment.
