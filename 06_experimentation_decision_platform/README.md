# 06 Experimentation Decision Platform V2

A senior-level experimentation and causal decision intelligence project inspired by Amazon-style applied research systems.

## What is included

- A/B testing with frequentist confidence intervals
- CUPED variance reduction
- Bayesian A/B testing using Beta-Binomial posteriors
- Sequential Bayesian experiment monitoring
- Uplift modeling / heterogeneous treatment effects with a T-Learner
- Thompson Sampling multi-armed bandit simulation
- Executive decision report with ship / no-ship framing
- Trained model artifact and user-level uplift scores

## Key outputs

- `data/raw/experiment_events.csv`
- `data/processed/experiment_analysis_dataset.csv`
- `models/uplift_t_learner.joblib`
- `reports/model_outputs/executive_decision_report.json`
- `reports/model_outputs/uplift_scores.csv`
- `reports/model_outputs/sequential_monitoring.csv`
- `reports/model_outputs/thompson_sampling_bandit.csv`
- `reports/figures/*.png`

## Interview story

I built an experimentation decision platform that converts experiment logs into business decisions. It supports standard A/B testing, CUPED, Bayesian decisioning, sequential monitoring, uplift modeling, and bandit-style adaptive optimization.

## Run

```bash
pip install -r requirements.txt
python scripts/run_full_pipeline.py
```
