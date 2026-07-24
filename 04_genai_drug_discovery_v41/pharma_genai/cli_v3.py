"""Backward-compatible CLI wrapper.

The current project is V4. Prefer:
python -m pharma_genai.cli_v4
"""

from pharma_genai.cli_v4 import main

if __name__ == "__main__":
    main()
