# GenAI Drug Discovery

A portfolio-ready generative AI project for molecular design and screening. This project demonstrates a practical, interview-friendly scaffold for using generative models in early-stage drug discovery workflows.

## Goals

- represent molecules as token sequences
- train a simple sequence generator baseline
- generate candidate molecules
- score candidates with lightweight heuristics
- document production-style tradeoffs and limitations

## Project Structure

- `gan_model/` training scaffold for a sequence GAN-style baseline
- `molecule_generation/` generation and filtering scripts
- `evaluation/` scoring and novelty/diversity checks
- `data/` small synthetic SMILES-like demo set
- `notebooks/` experiment notes

## Why this project matters

Drug discovery is a strong Health AI portfolio signal because it combines:
- generative modeling
- domain constraints
- ranking / optimization
- scientific evaluation
- production concerns around validity and screening

## Quick Start

```bash
pip install -r requirements.txt
python molecule_generation/build_vocab.py
python gan_model/train_generator.py
python molecule_generation/generate_candidates.py
python evaluation/evaluate_candidates.py
```

## Interview Story

I built a generative AI pipeline for drug discovery that learns token-level molecular patterns from a training corpus, generates new candidate molecules, filters invalid or low-quality outputs, and scores the remaining candidates for novelty and diversity. The project focuses on end-to-end ML system design rather than chemistry perfection, which makes it strong for applied ML and Health AI interviews.