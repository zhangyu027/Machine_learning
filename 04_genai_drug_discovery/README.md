# GenAI Drug Discovery

## Project Question

**Can a simple generative model create valid SMILES-like molecules and rank them by drug-likeness?**

This project is a portfolio-ready generative AI workflow for molecular sequence generation and screening. It demonstrates how a simple sequence generator can learn SMILES-like molecular patterns, generate candidate molecules, screen them with lightweight rules, and rank candidates using validity, novelty, diversity, and drug-likeness proxy metrics.

> This is a portfolio and learning project, not a production drug-discovery system.

---

## Why this project matters

Drug discovery is a strong Health AI / Applied ML portfolio project because it combines:

- generative AI
- sequence modeling
- molecule representation
- candidate generation
- rule-based screening
- ranking and evaluation
- honest discussion of scientific limitations

---

## End-to-End Workflow

The project follows this sequence:

1. **Data loading**  
   Load a small demo SMILES-like dataset.

2. **Vocabulary/tokenization**  
   Build a character-level vocabulary with `<PAD>`, `<START>`, and `<END>` tokens.

3. **Generator model**  
   Define a GRU-based sequence generator.

4. **Model training**  
   Train the generator to predict the next SMILES token.

5. **Molecule generation**  
   Generate new candidate molecular strings.

6. **Screening**  
   Filter and score generated candidates using simple validity and drug-likeness proxy rules.

7. **Evaluation**  
   Rank molecules by validity, novelty, diversity, and drug-likeness proxy metrics.

8. **Final interpretation**  
   Explain what worked, what the limitations are, and how the project could be improved.

---

## Project Structure

```text
04_genai_drug_discovery/
├── data/
│   └── demo_smiles.csv
├── gan_model/
│   ├── dataset.py
│   ├── model.py
│   └── train_generator.py
├── molecule_generation/
│   ├── build_vocab.py
│   ├── generate_candidates.py
│   └── screen_candidates.py
├── evaluation/
│   └── evaluate_candidates.py
├── notebooks/
│   └── GenAI_Drug_Discovery_End_to_End_Demo.ipynb
├── README.md
└── requirements.txt
```

---

## Quick Start

```bash
pip install -r requirements.txt
```

Run the scripts sequentially:

```bash
python molecule_generation/build_vocab.py
python gan_model/train_generator.py
python molecule_generation/generate_candidates.py
python molecule_generation/screen_candidates.py
python evaluation/evaluate_candidates.py
```

Or open the notebook:

```text
notebooks/GenAI_Drug_Discovery_End_to_End_Demo.ipynb
```

---

## Main Notebook

The notebook `GenAI_Drug_Discovery_End_to_End_Demo.ipynb` wraps the full workflow into one readable portfolio demo:

- data loading
- vocabulary/tokenization
- model training
- molecule generation
- screening and evaluation
- final interpretation

---

## Evaluation Metrics

| Metric | Meaning |
|---|---|
| Validity rate | Percentage of generated strings passing simple SMILES-like character checks |
| Novelty rate | Percentage of generated strings not present in training data |
| Diversity proxy | Number of unique characters in each generated molecule |
| Drug-likeness proxy | Simple heuristic based on N/O atoms, length, and aromatic-like pattern |

These are lightweight portfolio metrics and should not be interpreted as chemistry-grade validation.

---

## Example Portfolio Summary

Built an end-to-end generative AI drug discovery pipeline using Python and PyTorch to tokenize molecular sequences, train a GRU-based sequence generator, generate candidate SMILES-like molecules, and rank outputs using validity, novelty, diversity, and drug-likeness proxy metrics.

---

## Limitations

This project is intentionally simple and educational. It does **not** include:

- RDKit chemistry validation
- molecular docking
- toxicity prediction
- clinical validation
- wet-lab screening

A production-ready version would require chemistry-aware validation and domain expert review.

---

## Future Improvements

- Add RDKit validation.
- Calculate molecular properties such as molecular weight, LogP, and QED.
- Add molecular fingerprints for similarity and diversity.
- Train on a larger public SMILES dataset.
- Replace the GRU model with a Transformer model.
- Build a Streamlit app for interactive molecule generation.

## Contact Generate Order
1. build_vocab.py ✅
2. train_generator.py ✅
3. generate_candidates.py ← NEXT
4. screen_candidates.py
5. evaluate_candidates.py
6. visualize_results.py
7. GenAI_Drug_Discovery_End_to_End_Demo.ipynb

## Git Push Steps 
- cd /Users/yuzhang/projects/Machine_learning
- git status
- git add .
- git commit -m "Update GenAI drug discovery portfolio project"
- git push origin main
- git push heroku main
:wq
