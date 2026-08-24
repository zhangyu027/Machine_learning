# Validation Commands

```bash
python -m pip install -r requirements-dev.txt
python -m compileall app pharma_genai molecule_generation evaluation gan_model experiments tests
python -m pytest -q
python experiments/run_scientific_benchmark.py --input data/processed/herg.csv --target target
streamlit run app/streamlit_app.py
uvicorn pharma_genai.api:app --reload
jupyter notebook GenAI_Drug_Discovery_End_to_End_Demo.ipynb
```

The benchmark requires at least 20 complete binary-labeled records and both classes in train/test scaffold partitions.
The API command assumes the existing repository contains `pharma_genai/api.py` with an `app` object.
# Validation Commands

```bash
python -m pip install -r requirements-dev.txt
python -m compileall app pharma_genai molecule_generation evaluation gan_model experiments tests
python -m pytest -q
python experiments/run_scientific_benchmark.py --input data/processed/herg.csv --target target
streamlit run app/streamlit_app.py
uvicorn pharma_genai.api:app --reload
jupyter notebook GenAI_Drug_Discovery_End_to_End_Demo.ipynb
```

The benchmark requires at least 20 complete binary-labeled records and both classes in train/test scaffold partitions.
The API command assumes the existing repository contains `pharma_genai/api.py` with an `app` object.
# Validation Commands

```bash
python -m pip install -r requirements-dev.txt
python -m compileall app pharma_genai molecule_generation evaluation gan_model experiments tests
python -m pytest -q
python experiments/run_scientific_benchmark.py --input data/processed/herg.csv --target target
streamlit run app/streamlit_app.py
uvicorn pharma_genai.api:app --reload
jupyter notebook GenAI_Drug_Discovery_End_to_End_Demo.ipynb
```

The benchmark requires at least 20 complete binary-labeled records and both classes in train/test scaffold partitions.
The API command assumes the existing repository contains `pharma_genai/api.py` with an `app` object.
