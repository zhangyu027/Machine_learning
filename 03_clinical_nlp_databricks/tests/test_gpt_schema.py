from llm.gpt_eligibility_evaluator import EligibilityResult


def test_structured_gpt_schema():
    result = EligibilityResult(
        eligibility="needs_review",
        confidence=0.6,
        matched_evidence=["adult patient"],
        exclusion_evidence=[],
        missing_information=["trial-specific laboratory threshold"],
        rationale="The note lacks required trial criteria.",
        requires_human_review=True,
    )
    assert result.eligibility == "needs_review"
    assert result.requires_human_review is True
