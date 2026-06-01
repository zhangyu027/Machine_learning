# Experimentation Decision Platform

## Project question
Can we build a production-style experimentation and causal decision platform that helps executives determine whether a product, policy, or operational change truly caused measurable improvement?

## Why this project matters
This project is designed to strengthen a senior data scientist / senior research scientist profile. It focuses on the skills often emphasized in Amazon-style applied research roles: experimentation, causal inference, statistical rigor, scalable decision systems, and clear business communication.

## What it includes
- A/B test analysis
- CUPED variance reduction
- Bayesian A/B testing
- Uplift modeling
- Difference-in-differences
- Synthetic-control style baseline comparison
- Executive decision report generation
- Streamlit-ready dashboard layer
- Unit tests and sample experiment data

## Architecture
```text
Raw experiment events
        ↓
Data validation
        ↓
Metric construction
        ↓
A/B testing + CUPED + Bayesian testing
        ↓
Causal/uplift modeling
        ↓
Decision recommendation
        ↓
Executive report
```

## Quick start
```bash
cd 06_experimentation_decision_platform
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
python scripts/run_demo.py
pytest
```

## Interview positioning
> I built an experimentation decision platform that evaluates whether an intervention caused measurable improvement using A/B testing, CUPED variance reduction, Bayesian posterior probability, and uplift modeling. The system converts raw event data into executive-ready decisions with confidence, risk, and recommended action.
