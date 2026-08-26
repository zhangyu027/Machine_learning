# Validation Commands

Run from the repository root with the intended V4 Python interpreter.

```bash
python -m pip install -e .
python -m compileall app pharma_genai molecule_generation evaluation gan_model experiments tests
python -m pytest -q
python -m pip check
```

## Scientific benchmark

The benchmark expects a CSV with a `smiles` column and a binary endpoint column. To acquire hERG without changing the V4 dependency stack:

```bash
conda create -n tdc_data python=3.10 -y
conda run -n tdc_data python -m pip install "setuptools<81" "PyTDC==1.1.15"
conda run -n tdc_data python data/download_herg_tdc.py --output data/processed/herg.csv
```

Then run the benchmark in the main V4 environment:

```bash
python experiments/run_scientific_benchmark.py \
  --input data/processed/herg.csv \
  --target target \
  --output reports/herg_benchmark.csv
```

The benchmark uses scaffold-aware splitting and requires enough complete binary-labeled records for both classes to be represented in the evaluated partitions.

## Application checks

```bash
python -m streamlit run app/streamlit_app.py
python -m uvicorn pharma_genai.api.service:app --reload
```
