import hashlib

def hash_identifier(value, salt="portfolio-demo"):
    return hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()[:16]

def deidentify_columns(df, columns):
    out = df.copy()
    for col in columns:
        if col in out.columns:
            out[col] = out[col].astype(str).map(hash_identifier)
    return out
