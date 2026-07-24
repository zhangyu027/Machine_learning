# Error Analysis Plan

Review false negatives first because missed abnormalities may carry higher clinical risk. Review false positives for unnecessary escalation risk. For each error, record image quality, acquisition site, modality, label confidence, model confidence, and whether artifacts or preprocessing failures are present.

## Required analyses

1. Rank false negatives and false positives by confidence.
2. Compare metrics by scanner site, modality, sex, age band, and image-quality band when these fields are available.
3. Inspect calibration and choose thresholds based on the intended operating point rather than accuracy alone.
4. Separate data-quality failures from model failures.
5. Document corrective actions: relabeling, augmentation, sampling, threshold adjustment, or architecture changes.
