# GitHub Push Checklist

Run from the project root.

```bash
conda activate pharma_v4
python -m pip install -e .
python -m pytest -q
python -c "import pharma_genai; print(pharma_genai.__file__)"
python -c "from pharma_genai.data.scaffold_split import scaffold_split_indices; print('scaffold split OK')"
python -c "from pharma_genai.models.classical_baselines import build_baselines; print('baselines OK')"
# If hERG has been acquired with data/download_herg_tdc.py:
python experiments/run_scientific_benchmark.py --input data/processed/herg.csv --target target --output reports/herg_benchmark.csv
```

Check repository status:

```bash
git status
```

Suggested add command:

```bash
git add README.md data/README.md docs reports experiments pharma_genai/data pharma_genai/models requirements*.txt
```

Commit:

```bash
git commit -m "Publish V4.1 scientific benchmark documentation"
git push origin main
```

Avoid committing virtual environments, caches, large model checkpoints, local notebooks with secrets, and downloaded package folders.
