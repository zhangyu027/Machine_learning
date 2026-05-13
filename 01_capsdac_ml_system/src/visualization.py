"""
CAPSDAC visualization utilities.
"""

from pathlib import Path
import matplotlib.pyplot as plt


def save_current_figure(path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(path, bbox_inches="tight", dpi=150)


def rotate_xticks(angle=75):
    plt.xticks(rotation=angle, ha="right")
