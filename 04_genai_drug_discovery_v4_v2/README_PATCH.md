# Benchmark module patch

Copy the included `pharma_genai/data` and `pharma_genai/models` folders into the root-level `pharma_genai` package.

Then run:

```bash
pip install -e .
python experiments/run_scientific_benchmark.py \
  --input data/demo_smiles.csv \
  --target target
```

The input CSV must contain both `smiles` and `target`, and `target` must be a binary 0/1 label.
