from pathlib import Path
import pandas as pd

def load_sample_sources(base_path="data/sample"):
    base = Path(base_path)
    return {
        "patients": pd.read_csv(base / "fhir/patient.csv"),
        "encounters": pd.read_csv(base / "fhir/encounter.csv"),
        "labs": pd.read_csv(base / "fhir/labs.csv"),
        "vitals": pd.read_csv(base / "vitals/vitals.csv"),
        "notes": pd.read_csv(base / "notes/clinical_notes.csv"),
        "images": pd.read_csv(base / "imaging_metadata/imaging_manifest.csv"),
    }
