import pandas as pd


def population_stability_index(expected: pd.Series, actual: pd.Series, buckets: int = 10) -> float:
    """Simple PSI utility for feature drift monitoring."""
    expected_bins = pd.qcut(expected.rank(method="first"), buckets, duplicates="drop")
    expected_dist = expected_bins.value_counts(normalize=True).sort_index()
    actual_bins = pd.cut(actual, bins=buckets)
    actual_dist = actual_bins.value_counts(normalize=True).sort_index()
    actual_dist = actual_dist.reindex(expected_dist.index, fill_value=1e-6)
    expected_dist = expected_dist.replace(0, 1e-6)
    return float(((actual_dist - expected_dist) * (actual_dist / expected_dist).apply(lambda x: __import__('math').log(max(x, 1e-6)))).sum())
