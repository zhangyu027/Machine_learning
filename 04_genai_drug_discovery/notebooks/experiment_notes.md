# Experiment Notes

## Baseline
- token-level sequence generator with GRU
- training on small synthetic SMILES-like corpus
- objective: next-token prediction

## Future improvements
- replace baseline with VAE or diffusion model
- use RDKit for true chemical validity
- add property predictor for binding affinity or toxicity
- add Bayesian optimization or reinforcement learning loop