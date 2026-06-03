"""End-to-end candidate screening pipeline."""

from __future__ import annotations

from pharma_genai.connectors.public_data import PublicDataConnector
from pharma_genai.services.admet_service import ADMETPredictionService
from pharma_genai.services.uncertainty_service import UncertaintyService
from pharma_genai.validation.smiles_validation import validate_smiles


class CandidateScreeningPipeline:
    def __init__(self) -> None:
        self.connector = PublicDataConnector()
        self.admet = ADMETPredictionService()
        self.uncertainty = UncertaintyService()

    def screen_by_name(self, compound_name: str) -> dict:
        record = self.connector.pubchem_lookup(compound_name)
        if record is None:
            raise ValueError(f"No demo PubChem record found for {compound_name!r}")
        validation = validate_smiles(record.smiles)
        if not validation.is_valid:
            raise ValueError(f"Invalid SMILES for {compound_name!r}: {validation.message}")
        prediction = self.admet.predict(validation.canonical_smiles).to_dict()
        reliability = self.uncertainty.assess(prediction).to_dict()
        return {
            "compound": record.__dict__,
            "smiles_validation": validation.__dict__,
            "admet_prediction": prediction,
            "reliability": reliability,
        }
