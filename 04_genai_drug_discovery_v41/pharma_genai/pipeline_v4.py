"""V4 pipeline API.

V4 is the current public interface. This wrapper keeps older working
pipeline functions available while exposing V4 names.
"""

from __future__ import annotations


try:
    from .pipeline_v3 import analyze_many_v3 as _analyze_many_impl
    from .pipeline_v3 import dataframe_from_results
    from .pipeline_v3 import lookup_and_analyze
except Exception:
    _analyze_many_impl = None

    def dataframe_from_results(results):
        import pandas as pd
        return pd.DataFrame(results)

    def lookup_and_analyze(compound_name: str, include_literature: bool = False):
        from pharma_genai.services.candidate_screening import CandidateScreeningPipeline
        return CandidateScreeningPipeline().screen_by_name(compound_name)


def analyze_many_v4(*args, **kwargs):
    if _analyze_many_impl is not None:
        return _analyze_many_impl(*args, **kwargs)

    from pharma_genai.services.admet_service import ADMETPredictionService
    from pharma_genai.services.uncertainty_service import UncertaintyService

    service = ADMETPredictionService()
    uncertainty = UncertaintyService()
    smiles = args[0] if args else kwargs.get("smiles", [])
    outputs = []
    for s in smiles:
        pred = service.predict(s).to_dict()
        rel = uncertainty.assess(pred).to_dict()
        outputs.append({**pred, **rel})
    return outputs


analyze_many_v3 = analyze_many_v4
