"""Run entity extraction and patient-to-trial matching on one synthetic note."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trial_matching.matcher import TrialMatcher
NOTE = "Patient age 58 with diabetes. HbA1c 8.2%. Current therapy includes metformin. No recent hospitalization."
matcher = TrialMatcher()
trials = matcher.load_trials(ROOT / "data" / "sample" / "trials.json")
results = matcher.rank(NOTE, trials)
out = ROOT / "outputs" / "trial_match_demo.json"
out.write_text(json.dumps([r.model_dump() for r in results], indent=2))
print(out.read_text())
