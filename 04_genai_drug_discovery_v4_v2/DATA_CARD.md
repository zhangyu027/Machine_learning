# Data Card — Scientific ML Drug Discovery Platform V4

## Intended use
This repository supports reproducible molecular ML experimentation and portfolio demonstration. It is not a source of validated medicinal-chemistry or regulatory conclusions.

## Required benchmark schema
Each endpoint dataset should contain at minimum:

- `smiles`: standardized molecular structure string
- endpoint label, for example `herg`, `ames`, `bbb`, `solubility`, or `clearance`
- optional compound identifier, assay date, source, units, and assay-quality fields

## Data quality controls

1. Parse and canonicalize SMILES with RDKit when available.
2. Remove invalid structures, salts/mixtures according to a documented rule, duplicates, and contradictory labels.
3. Preserve provenance, assay definition, units, censoring, and missing-label patterns.
4. Fit transformations on training data only.
5. Use Bemis–Murcko scaffold splitting as the primary generalization test.
6. Add temporal and external validation when source data permit.

## Leakage risks
Random molecule splitting can place close structural analogs in both training and test sets. Primary scientific claims must therefore use scaffold-aware evaluation. Random splits may be reported only as secondary comparisons.

## Limitations
The included example and proxy outputs are software demonstrations. Scientific conclusions require endpoint-specific public or proprietary experimental datasets and domain review.
