"""Build a GitHub-safe synthetic clinical NLP dataset.

This script creates synthetic trial-screening notes with labels:
eligible, not_eligible, and needs_review. It contains no real patient data.
"""
from pathlib import Path
import random
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "sample" / "clinical_notes_raw.csv"
OUT.parent.mkdir(parents=True, exist_ok=True)

random.seed(42)
conditions = ["diabetes", "heart failure", "asthma", "hypertension", "kidney disease", "COPD"]
meds = ["metformin", "insulin", "beta blocker", "steroid", "ACE inhibitor", "diuretic"]

rows = []
for i in range(240):
    condition = random.choice(conditions)
    med = random.choice(meds)
    age = random.randint(18, 88)
    if i % 3 == 0:
        label = "eligible"
        note = f"Patient age {age} with stable {condition}. Meets inclusion criteria and no exclusion medication conflict. Current therapy includes {med}."
    elif i % 3 == 1:
        label = "not_eligible"
        note = f"Patient age {age} with {condition}. Exclusion criteria present due to recent hospitalization or incompatible medication history including {med}."
    else:
        label = "needs_review"
        note = f"Patient age {age} with possible {condition}. Eligibility unclear. Missing lab confirmation and coordinator review required. Medication history includes {med}."
    rows.append({
        "note_id": f"N{i:04d}",
        "trial_id": f"T{1000 + (i % 8)}",
        "patient_ref": f"SYN-{i:04d}",
        "note_text": note,
        "label": label,
    })

pd.DataFrame(rows).to_csv(OUT, index=False)
print(f"Created synthetic dataset: {OUT}")
