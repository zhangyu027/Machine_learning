from __future__ import annotations


def decision_recommendation(p_value: float, prob_better: float, relative_lift: float) -> str:
    if p_value < 0.05 and prob_better >= 0.95 and relative_lift > 0:
        return "Launch: evidence is strong and expected impact is positive."
    if prob_better >= 0.80 and relative_lift > 0:
        return "Continue experiment: promising but not yet strong enough for full rollout."
    return "Do not launch yet: evidence is weak or impact is not positive."


def build_executive_report(ab_result: dict, bayes_result: dict, uplift_result: dict) -> str:
    rec = decision_recommendation(ab_result["p_value"], bayes_result["prob_treatment_better"], ab_result["relative_lift"])
    return f"""
# Executive Experiment Decision Report

## Decision
{rec}

## Frequentist result
- Control mean: {ab_result['control_mean']:.3f}
- Treatment mean: {ab_result['treatment_mean']:.3f}
- Relative lift: {ab_result['relative_lift']:.2%}
- p-value: {ab_result['p_value']:.4f}

## Bayesian result
- Probability treatment is better: {bayes_result['prob_treatment_better']:.2%}
- Expected conversion lift: {bayes_result['expected_lift']:.4f}
- 95% credible interval: {bayes_result['credible_interval_95']}

## Uplift insight
Top segments by estimated heterogeneous uplift: {uplift_result['top_uplift_segments']}
""".strip()
