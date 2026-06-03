# Installation Notes

This V3.1 package no longer requires `rdkit-pypi`.

Why:
- `rdkit-pypi` is not available for every Python version/platform.
- The package already includes a lightweight SMILES validation fallback, so tests and demos can run without RDKit.

Recommended install:

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pytest -q
```

Optional RDKit install:

```bash
conda install -c conda-forge rdkit
```

or, only if supported on your environment:

```bash
pip install rdkit
```

The code will automatically use RDKit when available and fall back safely when it is not installed.
