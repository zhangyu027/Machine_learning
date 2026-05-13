#!/usr/bin/env bash

# End-to-end workflow using real molecule data from ChEMBL.
# Run from project root:
#   bash run_real_data_pipeline.sh

set -e

echo "Step 1: Download real molecule data from ChEMBL"
python data/download_molecule_data.py --source chembl --limit 1000 --output data/real_smiles.csv

echo "Step 2: Build vocabulary from real molecule data"
python molecule_generation/build_vocab.py --data data/real_smiles.csv

echo "Step 3: Train generator model on real molecule data"
python gan_model/train_generator.py --data data/real_smiles.csv --epochs 20 --batch-size 32 --max-len 64

echo "Step 4: Generate candidate molecules"
python molecule_generation/generate_candidates.py

echo "Step 5: Screen generated candidates"
python molecule_generation/screen_candidates.py

echo "Step 6: Evaluate generated candidates using real training data"
python evaluation/evaluate_candidates.py --train data/real_smiles.csv

echo "Step 7: Generate visual outputs"
python evaluation/visualize_results.py

echo "Done."
