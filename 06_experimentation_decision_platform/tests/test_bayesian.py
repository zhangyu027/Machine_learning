from src.experimentation.bayesian_ab_test import beta_binomial_ab_test

def test_bayesian_probability_bounds():
    out=beta_binomial_ab_test(60,100,50,100,draws=5000)
    assert 0 <= out['prob_treatment_better'] <= 1
