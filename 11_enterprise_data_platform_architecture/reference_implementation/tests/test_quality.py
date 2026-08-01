import pytest

from enterprise_data_platform.quality import DataQualityError, required_fields_rule, run_quality_checks, unique_grain_rule


def test_warning_results_are_persisted_without_failure():
    result = run_quality_checks([{"id": "1"}], [required_fields_rule(["id"], severity="medium")])
    assert result[0]["passed"] is True


def test_critical_duplicate_grain_stops_pipeline():
    with pytest.raises(DataQualityError):
        run_quality_checks([{"id": "1"}, {"id": "1"}], [unique_grain_rule(["id"])])
