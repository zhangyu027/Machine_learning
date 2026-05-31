"""
Download real molecular SMILES data for the GenAI Drug Discovery project.

This script supports two public molecule sources:

1. ChEMBL
   - Good for drug-discovery / bioactivity-related molecules.
   - Uses chembl_webresource_client.

2. PubChem
   - Good for named compounds or starter molecule sets.
   - Uses PubChem PUG-REST through requests.

Default output:
    data/real_smiles.csv

The rest of the project can then use:
    data/real_smiles.csv

Example:
    python data/download_molecule_data.py --source chembl --limit 1000

Then run:
    python molecule_generation/build_vocab.py --data data/real_smiles.csv
"""

from pathlib import Path
import argparse
import time
import pandas as pd
import requests


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "real_smiles.csv"


def clean_smiles(smiles_values):
    """
    Clean and deduplicate SMILES strings.
    """
    cleaned = []

    for smiles in smiles_values:
        if smiles is None:
            continue

        smiles = str(smiles).strip()

        if not smiles:
            continue

        # Keep reasonably sized strings for this portfolio model.
        if len(smiles) < 3 or len(smiles) > 120:
            continue

        cleaned.append(smiles)

    return sorted(set(cleaned))


def download_from_chembl(limit=1000):
    """
    Download canonical SMILES from ChEMBL.

    ChEMBL is useful for drug-like compounds and bioactivity-related molecules.
    """
    try:
        from chembl_webresource_client.new_client import new_client
    except ImportError as exc:
        raise ImportError(
            "chembl_webresource_client is not installed. "
            "Run: pip install chembl_webresource_client"
        ) from exc

    molecule = new_client.molecule

    records = molecule.filter(
        molecule_structures__canonical_smiles__isnull=False
    ).only([
        "molecule_chembl_id",
        "molecule_structures",
        "pref_name",
        "max_phase",
    ])[:limit]

    rows = []

    for record in records:
        structures = record.get("molecule_structures") or {}
        smiles = structures.get("canonical_smiles")

        if smiles:
            rows.append({
                "smiles": smiles,
                "source": "ChEMBL",
                "compound_id": record.get("molecule_chembl_id"),
                "name": record.get("pref_name"),
                "max_phase": record.get("max_phase"),
            })

    return pd.DataFrame(rows)


def download_from_pubchem_names(names=None, sleep_seconds=0.2):
    """
    Download SMILES from PubChem using compound names.

    PubChem PUG-REST endpoint example:
    https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/property/CanonicalSMILES/JSON
    """
    if names is None:
        names = [
            "aspirin",
            "acetaminophen",
            "ibuprofen",
            "caffeine",
            "metformin",
            "warfarin",
            "atorvastatin",
            "naproxen",
            "amoxicillin",
            "omeprazole",
            "lisinopril",
            "losartan",
            "simvastatin",
            "gabapentin",
            "sertraline",
            "fluoxetine",
            "diphenhydramine",
            "cetirizine",
            "melatonin",
            "lidocaine",
        ]

    rows = []

    for name in names:
        url = (
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/"
            f"{name}/property/CanonicalSMILES/JSON"
        )

        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()

            properties = data.get("PropertyTable", {}).get("Properties", [])

            for item in properties:
                smiles = item.get("CanonicalSMILES")

                if smiles:
                    rows.append({
                        "smiles": smiles,
                        "source": "PubChem",
                        "compound_id": item.get("CID"),
                        "name": name,
                        "max_phase": None,
                    })

        except Exception as exc:
            print(f"Warning: failed to download {name}: {exc}")

        time.sleep(sleep_seconds)

    return pd.DataFrame(rows)


def save_smiles_dataset(df, output_path=DEFAULT_OUTPUT):
    """
    Save a project-compatible CSV with a required 'smiles' column.
    """
    if df.empty:
        raise ValueError("No molecules were downloaded.")

    smiles = clean_smiles(df["smiles"].tolist())

    clean_df = pd.DataFrame({"smiles": smiles})

    # Keep metadata when possible by merging first matching rows.
    metadata_cols = [col for col in df.columns if col != "smiles"]

    if metadata_cols:
        metadata = df.drop_duplicates("smiles").set_index("smiles")
        clean_df = clean_df.join(metadata[metadata_cols], on="smiles")

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    clean_df.to_csv(output_path, index=False)

    print(f"Saved real molecule dataset: {output_path}")
    print(f"Number of unique molecules: {len(clean_df)}")

    return clean_df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        choices=["chembl", "pubchem"],
        default="chembl",
        help="Data source to use.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=1000,
        help="Number of ChEMBL records to request.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=str(DEFAULT_OUTPUT),
        help="Output CSV path.",
    )

    args = parser.parse_args()

    if args.source == "chembl":
        df = download_from_chembl(limit=args.limit)
    else:
        df = download_from_pubchem_names()

    save_smiles_dataset(df, args.output)


if __name__ == "__main__":
    main()
