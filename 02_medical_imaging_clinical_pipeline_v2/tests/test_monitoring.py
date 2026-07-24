from monitoring.drift_monitor import classify_drift, population_stability_index


def test_psi_stable_for_same_distribution():
    values = list(range(1, 101))
    psi = population_stability_index(values, values)
    assert psi < 0.1
    assert classify_drift(psi) == "stable"
