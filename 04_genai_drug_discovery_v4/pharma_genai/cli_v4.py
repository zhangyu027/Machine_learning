from __future__ import annotations
import argparse
import json
from .pipeline_v3 import analyze_many_v3


def main() -> None:
    parser = argparse.ArgumentParser(description="Pharma GenAI Drug Discovery V4 CLI")
    parser.add_argument("--smiles", nargs="+", default=["CCO", "CC(=O)Oc1ccccc1C(=O)O", "Cn1cnc2c1c(=O)n(C)c(=O)n2C"])
    parser.add_argument("--literature", action="store_true")
    args = parser.parse_args()
    print(json.dumps(analyze_many_v3(args.smiles, include_literature=args.literature), indent=2))


if __name__ == "__main__":
    main()
