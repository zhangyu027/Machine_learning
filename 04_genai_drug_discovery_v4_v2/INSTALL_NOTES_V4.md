# V4 Installation and Run Notes

This package has been cleaned and renamed consistently as V4.

## Install

```bash
cd 04_genai_drug_discovery_v4_principal_enterprise
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
pytest -q
```

## Streamlit

```bash
PYTHONPATH=. streamlit run app/streamlit_app.py
```

## FastAPI

```bash
PYTHONPATH=. uvicorn pharma_genai.api:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Note

`pipeline_v4.py` is the current interface. `pipeline_v3.py` may remain only as a backward-compatible wrapper for older notebooks/tests.
