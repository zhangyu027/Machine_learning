# Merge Instructions

This archive is an overlay patch for `08_healthcare_multimodal_foundation`.

## Apply

From the repository root:

```bash
cd 08_healthcare_multimodal_foundation
cp -R /path/to/healthcare_multimodal_patch/. .
```

Review the copied files with `git diff`. If your existing evaluation module uses a different location, move `src/healthcare_mm/evaluation/multimodal_eval.py` to that existing location and update the test import.

Do not blindly overwrite `api/main.py`. Follow `API_PATCH_GUIDE.md`, because the API source was not part of the supplied review package and its current imports and response fields could not be verified.

## Validate

```bash
python -m pip install -r requirements-dev.txt
python -m scripts.run_pipeline
pytest -q
uvicorn api.main:app --reload
```

Then inspect `/docs`, `/health`, and `/metrics` after completing the API guide.

## Suggested commit

```bash
git checkout -b fix/healthcare-mm-review
git add 08_healthcare_multimodal_foundation
git commit -m "Harden healthcare multimodal evaluation and documentation"
```
