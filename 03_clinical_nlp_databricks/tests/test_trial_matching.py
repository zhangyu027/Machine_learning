from pathlib import Path
from trial_matching.matcher import TrialMatcher

ROOT = Path(__file__).resolve().parents[1]


def test_matching_returns_criteria_groups():
    matcher = TrialMatcher()
    trial = matcher.load_trials(ROOT / "data" / "sample" / "trials.json")[0]
    result = matcher.match(
        "Patient age 58 with diabetes. HbA1c 8.2%. On metformin. No recent hospitalization.", trial
    )
    assert result.eligibility == "eligible"
    assert len(result.matched_criteria) == 5
    assert not result.failed_criteria
    assert not result.unknown_criteria


def test_missing_lab_requires_review():
    matcher = TrialMatcher()
    trial = matcher.load_trials(ROOT / "data" / "sample" / "trials.json")[0]
    result = matcher.match("Patient age 58 with diabetes. On metformin. No recent hospitalization.", trial)
    assert result.eligibility == "needs_review"
    assert any(item.criterion_id == "I3" for item in result.unknown_criteria)
