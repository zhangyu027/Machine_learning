"""Public chemistry data connectors for the V3.1 enterprise drug discovery demo."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class CompoundRecord:
    source: str
    compound_id: str
    name: str
    smiles: str
    target: str = ""
    activity: str = ""
    metadata: dict | None = None


DEMO_PUBCHEM_RECORDS: dict[str, CompoundRecord] = {
    "aspirin": CompoundRecord(
        source="PubChem",
        compound_id="2244",
        name="Aspirin",
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        target="PTGS1/PTGS2 (COX)",
        activity="anti-inflammatory / analgesic",
        metadata={"canonical_name": "acetylsalicylic acid", "molecular_formula": "C9H8O4"},
    ),
    "acetylsalicylic acid": CompoundRecord(
        source="PubChem",
        compound_id="2244",
        name="Aspirin",
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        target="PTGS1/PTGS2 (COX)",
        activity="anti-inflammatory / analgesic",
        metadata={"canonical_name": "acetylsalicylic acid"},
    ),
    "caffeine": CompoundRecord(
        source="PubChem",
        compound_id="2519",
        name="Caffeine",
        smiles="Cn1cnc2c1c(=O)n(C)c(=O)n2C",
        target="adenosine receptor",
        activity="stimulant",
        metadata={"canonical_name": "caffeine", "molecular_formula": "C8H10N4O2"},
    ),
    "ibuprofen": CompoundRecord(
        source="PubChem",
        compound_id="3672",
        name="Ibuprofen",
        smiles="CC(C)CC1=CC=C(C=C1)C(C)C(=O)O",
        target="PTGS1/PTGS2 (COX)",
        activity="nonsteroidal anti-inflammatory",
        metadata={"canonical_name": "ibuprofen", "molecular_formula": "C13H18O2"},
    ),
    "warfarin": CompoundRecord(
        source="PubChem",
        compound_id="54678486",
        name="Warfarin",
        smiles="CC(=O)CC(C1=CC=CC=C1)C2=C(C3=CC=CC=C3OC2=O)O",
        target="VKORC1",
        activity="anticoagulant",
        metadata={"canonical_name": "warfarin"},
    ),
}


DEMO_CHEMBL_RECORDS: dict[str, CompoundRecord] = {
    "aspirin": CompoundRecord(
        source="ChEMBL",
        compound_id="CHEMBL25",
        name="Aspirin",
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        target="cyclooxygenase",
        activity="reference compound",
        metadata={"assay_type": "curated demo record"},
    ),
    "caffeine": CompoundRecord(
        source="ChEMBL",
        compound_id="CHEMBL113",
        name="Caffeine",
        smiles="Cn1cnc2c1c(=O)n(C)c(=O)n2C",
        target="adenosine receptor",
        activity="reference compound",
        metadata={"assay_type": "curated demo record"},
    ),
}


DEMO_DRUGBANK_RECORDS: dict[str, CompoundRecord] = {
    "aspirin": CompoundRecord(
        source="DrugBank",
        compound_id="DB00945",
        name="Aspirin",
        smiles="CC(=O)OC1=CC=CC=C1C(=O)O",
        target="cyclooxygenase",
        activity="approved drug",
        metadata={"approval_status": "approved"},
    ),
    "caffeine": CompoundRecord(
        source="DrugBank",
        compound_id="DB00201",
        name="Caffeine",
        smiles="Cn1cnc2c1c(=O)n(C)c(=O)n2C",
        target="adenosine receptor",
        activity="approved / common stimulant",
        metadata={"approval_status": "approved"},
    ),
}


class PublicDataConnector:
    """Offline-safe public-data lookup layer.

    Production code can replace these dictionaries with PubChem PUG-REST,
    ChEMBL API, or local DrugBank exports without changing downstream code.
    """

    def _lookup(self, table: dict[str, CompoundRecord], query: str) -> Optional[CompoundRecord]:
        key = query.strip().lower()
        record = table.get(key)
        if record is None:
            return None
        if not record.smiles:
            return None
        return record

    def pubchem_lookup(self, query: str) -> Optional[CompoundRecord]:
        return self._lookup(DEMO_PUBCHEM_RECORDS, query)

    def chembl_lookup(self, query: str) -> Optional[CompoundRecord]:
        return self._lookup(DEMO_CHEMBL_RECORDS, query)

    def drugbank_lookup(self, query: str) -> Optional[CompoundRecord]:
        return self._lookup(DEMO_DRUGBANK_RECORDS, query)

    def lookup_all_sources(self, query: str) -> list[CompoundRecord]:
        records = [
            self.pubchem_lookup(query),
            self.chembl_lookup(query),
            self.drugbank_lookup(query),
        ]
        return [r for r in records if r is not None]
