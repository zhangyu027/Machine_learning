"""Public chemistry data source integration layer.

V3 defines a unified client for ChEMBL, PubChem, DrugBank-style local exports,
and BindingDB-style local exports. Network access is optional; tests and demos use
offline fixture data for reproducibility.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import csv
import json
import os

try:  # pragma: no cover
    import requests
except Exception:  # pragma: no cover
    requests = None


@dataclass
class CompoundRecord:
    source: str
    compound_id: str
    name: str
    smiles: str
    target: str = ""
    activity: str = ""
    metadata: Dict[str, str] | None = None


DEMO_COMPOUNDS = [
    CompoundRecord("demo", "ASPIRIN", "Aspirin", "CC(=O)Oc1ccccc1C(=O)O", "COX", "anti-inflammatory"),
    CompoundRecord("demo", "CAFFEINE", "Caffeine", "Cn1cnc2c1c(=O)n(C)c(=O)n2C", "A2A", "stimulant"),
    CompoundRecord("demo", "ETHANOL", "Ethanol", "CCO", "CNS", "small control molecule"),
]


class PublicDataConnector:
    def __init__(self, timeout: int = 10):
        self.timeout = timeout

    def pubchem_lookup(self, name: str) -> Optional[CompoundRecord]:
        if requests is None:
            return self._demo_lookup(name)
        url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{name}/property/CanonicalSMILES,Title/JSON"
        try:  # pragma: no cover - internet-dependent
            resp = requests.get(url, timeout=self.timeout)
            resp.raise_for_status()
            props = resp.json()["PropertyTable"]["Properties"][0]
            return CompoundRecord("PubChem", str(props.get("CID", name)), props.get("Title", name), props.get("CanonicalSMILES", ""))
        except Exception:
            return self._demo_lookup(name)

    def chembl_activity_search(self, target_keyword: str) -> List[CompoundRecord]:
        # Lightweight portfolio implementation; production would call ChEMBL API endpoints.
        return [r for r in DEMO_COMPOUNDS if target_keyword.lower() in (r.target + r.name + r.activity).lower()]

    def load_drugbank_like_csv(self, path: str) -> List[CompoundRecord]:
        if not os.path.exists(path):
            return DEMO_COMPOUNDS.copy()
        records = []
        with open(path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                records.append(CompoundRecord("DrugBankLocal", row.get("drugbank_id", row.get("id", "")), row.get("name", ""), row.get("smiles", ""), row.get("target", ""), row.get("activity", ""), row))
        return records

    def load_bindingdb_like_csv(self, path: str) -> List[CompoundRecord]:
        if not os.path.exists(path):
            return DEMO_COMPOUNDS.copy()
        return self.load_drugbank_like_csv(path)

    @staticmethod
    def _demo_lookup(name: str) -> Optional[CompoundRecord]:
        for r in DEMO_COMPOUNDS:
            if name.lower() in r.name.lower() or name.lower() == r.compound_id.lower():
                return r
        return None

    @staticmethod
    def to_dicts(records: List[CompoundRecord]) -> List[Dict[str, object]]:
        return [asdict(r) for r in records]
