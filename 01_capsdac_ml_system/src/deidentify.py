"""
CAPSDAC de-identification utilities.

Use only on authorized machines. Do not commit raw CAPSDAC child-level data to GitHub.
"""

from pathlib import Path
import hashlib
import pandas as pd


DIRECT_PII_KEYWORDS = [
    "first_name", "firstname", "last_name", "lastname", "middle_name",
    "child_name", "student_name", "parent_name", "guardian_name",
    "ssn", "social_security", "birthdate", "dob",
    "address", "street", "phone", "email",
]


def hash_value(value, salt="capsdac_demo_salt"):
    if pd.isna(value):
        return None
    raw = f"{salt}_{value}".encode("utf-8")
    return hashlib.sha256(raw).hexdigest()[:12]


def deidentify_dataframe(df, id_columns=None, drop_pii=True):
    out = df.copy()

    if drop_pii:
        pii_cols = [
            c for c in out.columns
            if any(k in c.lower().replace(" ", "_") for k in DIRECT_PII_KEYWORDS)
        ]
        out = out.drop(columns=pii_cols, errors="ignore")

    if id_columns:
        for col in id_columns:
            if col in out.columns:
                out[col + "_Deidentified"] = out[col].apply(hash_value)
                out = out.drop(columns=[col])

    return out


def aggregate_for_public_sample(input_path, output_path, group_cols, count_col_name="EnrollmentCount"):
    df = pd.read_csv(input_path)

    grouped = (
        df.groupby(group_cols, dropna=False)
        .size()
        .reset_index(name=count_col_name)
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    grouped.to_csv(output_path, index=False)

    return grouped
