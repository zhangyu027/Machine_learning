# Final Validation Check

## Local validation

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pytest ruff
python -m pip install -e reference_implementation

ruff check reference_implementation/src reference_implementation/tests tests
python -m compileall reference_implementation/src
pytest -q tests reference_implementation/tests
enterprise-platform-demo --config reference_implementation/config/sample_pipeline.json
terraform fmt -check -recursive infra/terraform
```

## Required evidence before merge

- All architecture and reference-implementation tests pass.
- The sample pipeline produces Bronze, Silver, Gold, quality, lineage, and run artifacts.
- Terraform formatting passes.
- GitHub Actions passes.
- No `.DS_Store`, `__MACOSX`, secrets, state files, virtual environments, or generated outputs are tracked.
- Documentation distinguishes executable patterns from the target Azure architecture.
