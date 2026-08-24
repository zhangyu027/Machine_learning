PYTHONPATH := $(PWD)/forecasting

.PHONY: install test run report dashboard api clean validate

install:
	pip install -r requirements.txt

test:
	PYTHONPATH=$(PYTHONPATH) pytest

run:
	PYTHONPATH=$(PYTHONPATH) python forecasting/scripts/run_capsdac_pipeline.py

report:
	PYTHONPATH=$(PYTHONPATH) python forecasting/scripts/generate_visualization_report.py

validate: test run report

dashboard:
	streamlit run dashboards/streamlit_app.py

api:
	uvicorn serving.api.main:app --reload

clean:
	rm -f data/processed/*.csv outputs/metrics/*.json outputs/metrics/*.csv outputs/reports/*.json outputs/reports/*.md outputs/forecasts/*.csv outputs/experiments/*.csv outputs/retraining/*.json
	rm -rf outputs/experiments/capsdac-v3-* models/registry/*.joblib models/registry/*.json
