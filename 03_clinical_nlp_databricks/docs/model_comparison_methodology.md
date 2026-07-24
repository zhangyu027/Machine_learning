# Model Comparison Methodology

## Primary metrics

- **Macro-F1:** gives equal weight to eligible, not eligible, and needs review.
- **Eligible recall:** measures how often truly eligible cases are retained by the screening system.
- **Latency:** average wall-clock milliseconds per note in the measured environment.
- **Cost:** qualitative deployment tier, not a fixed dollar amount.
- **Explainability:** qualitative ability to inspect features, evidence, or rationale.

## Integrity rule

The comparison table reads only generated metric JSON files. If a model has not been executed, its metrics are shown as `Not run`. This prevents portfolio claims from exceeding the evidence.

## Clinical limitations

Synthetic notes are useful for validating software flow but cannot establish clinical validity. Real deployment would require representative data, privacy review, subgroup evaluation, calibration, prospective validation, and qualified human oversight.
