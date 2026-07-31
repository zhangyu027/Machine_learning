# Migration Fix for Existing Archive Copy

The reported failures came from using an older or incompletely replaced directory under
`/Users/yuzhang/projects/Archive/06_experimentation_decision_platform`.

## Recommended replacement

1. Rename the old folder for backup.
2. Extract this package as a new `06_experimentation_decision_platform` directory.
3. Create a clean virtual environment.
4. Install through `requirements-all.txt`.

```bash
cd /Users/yuzhang/projects/Archive
mv 06_experimentation_decision_platform 06_experimentation_decision_platform_old
unzip 06_experimentation_decision_platform_v3.1_fixed.zip
cd 06_experimentation_decision_platform

python3.10 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-all.txt

python -c "import pandas, experimentation; print('environment ready')"
pytest -q
python -m scripts.run_full_pipeline
```

Do not copy only selected files into the old directory; that can leave stale modules and tests.
