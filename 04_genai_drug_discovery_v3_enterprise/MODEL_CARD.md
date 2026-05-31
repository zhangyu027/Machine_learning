# Model Card: Pharma GenAI V2 ADMET Reliability Scorer

## Intended Use
Portfolio demonstration of small-molecule ADMET/toxicity screening and candidate ranking.

## Inputs
SMILES strings representing small molecules.

## Outputs
Molecular descriptors, ADMET risk probabilities, toxicity risk probabilities, development priority, reliability label, confidence score, uncertainty score, and applicability-domain notes.

## Reliability Layer
The reliability module follows the idea of pharmaceutical ML prediction reliability analysis: predictions are not treated as equally trustworthy. Confidence is estimated from descriptor-domain coverage, decision-boundary uncertainty, and proxy ensemble disagreement. A beta-binomial style alpha/beta summary is included for uncertainty communication.

## Limitations
Current V2 scoring uses transparent heuristic/rule-based models unless retrained by the user. Use this for portfolio demonstration, education, and architecture review, not clinical or regulatory decisions.

## Recommended Validation
External validation on ADMET benchmark datasets, scaffold split evaluation, calibration curves, applicability-domain analysis, and prospective experimental feedback.
