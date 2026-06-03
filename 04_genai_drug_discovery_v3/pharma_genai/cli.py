from __future__ import annotations
import argparse
from .pipeline import analyze_smiles, analyze_file

def main():
    parser=argparse.ArgumentParser(description="Pharma GenAI V2: ADMET, toxicity, and reliability scoring")
    sub=parser.add_subparsers(dest="cmd", required=True)
    one=sub.add_parser("score", help="score one SMILES")
    one.add_argument("smiles")
    batch=sub.add_parser("batch", help="score a CSV/TXT file of SMILES")
    batch.add_argument("input")
    batch.add_argument("--output", default="outputs/admet_v2_predictions.csv")
    batch.add_argument("--column", default="smiles")
    args=parser.parse_args()
    if args.cmd=="score":
        import json
        print(json.dumps(analyze_smiles(args.smiles), indent=2))
    else:
        print(analyze_file(args.input, args.output, args.column))
if __name__ == "__main__": main()
