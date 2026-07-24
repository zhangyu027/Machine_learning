from clinical_entities.extractor import ClinicalEntityExtractor


def test_extracts_entities_and_negation():
    note = "58-year-old patient with diabetes. HbA1c 8.2%. On metformin. No recent hospitalization. Denies asthma."
    result = ClinicalEntityExtractor().extract(note)
    assert result.age == 58
    assert "diabetes" in result.conditions
    assert "asthma" in result.negated_conditions
    assert "metformin" in result.medications
    assert result.labs[0].name == "hba1c"
    assert result.recent_hospitalization is False
