# V4 Installation and Environment Notes

## Do I need an environment named `pharma_v4`?

No. `pharma_v4` is only a convenient local Conda environment name; it is not part of the Python package and the application does not look for that name. The project requires Python 3.10+ and its dependencies.

An isolated environment is recommended because this project contains scientific, chemistry, PyTorch, Hugging Face, Streamlit, and API dependencies that can conflict with Homebrew/global Python packages.

To see where Conda environments live:

```bash
conda env list
```

For an environment named `pharma_v4`, a typical Anaconda path on Apple Silicon is:

```text
/opt/anaconda3/envs/pharma_v4
```

Confirm the interpreter actually in use:

```bash
which python
python -c "import sys; print(sys.executable)"
python -m pip --version
```

Use `python -m pip`, not bare `pip`, so installation is tied to the same interpreter.

## Recommended clean V4 environment

```bash
conda create -n pharma_v4 python=3.11 -y
conda activate pharma_v4
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements.txt
python -m pip install -e .
python -m pip check
python -m pytest -q
```

RDKit can be installed with Conda if needed:

```bash
conda install -c conda-forge rdkit
```

## hERG / PyTDC: keep data acquisition isolated

Do **not** install PyTDC into the main V4 environment just to download one dataset. PyTDC can pull dependency versions that conflict with the project's newer NLP stack.

Create a small data-only environment instead:

```bash
conda create -n tdc_data python=3.10 -y
conda run -n tdc_data python -m pip install "setuptools<81" "PyTDC==1.1.15"
conda run -n tdc_data python data/download_herg_tdc.py \
  --output data/processed/herg.csv
```

The produced CSV belongs to the project; the temporary `tdc_data` environment does not.

Then, from the main V4 environment:

```bash
python experiments/run_scientific_benchmark.py \
  --input data/processed/herg.csv \
  --target target \
  --output reports/herg_benchmark.csv
```

## Streamlit

```bash
python -m streamlit run app/streamlit_app.py
```

## FastAPI

The API implementation in this package is under `pharma_genai/api/service.py`. Run it only if that module exposes an `app` object:

```bash
python -m uvicorn pharma_genai.api.service:app --reload
```
