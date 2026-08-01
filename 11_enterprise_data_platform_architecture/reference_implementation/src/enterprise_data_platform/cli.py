"""Command-line entry point."""
from __future__ import annotations

import argparse
import json

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the enterprise data-platform reference pipeline")
    parser.add_argument("--config", required=True, help="Path to pipeline configuration JSON")
    args = parser.parse_args()
    print(json.dumps(run_pipeline(args.config), indent=2))


if __name__ == "__main__":
    main()
