"""
Conceptual graph-enhanced clinical reasoning module.

This lightweight module creates a similar-case graph using metadata features.
It is intended as a portfolio extension, not a full GNN implementation.
"""

import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def build_case_similarity_edges(metadata_df, feature_columns=None, top_k=5):
    """
    Build top-k similar-case edges from structured metadata.

    Returns an edge list:
        source_case, target_case, similarity
    """
    if feature_columns is None:
        feature_columns = ["age", "sex", "prior_condition", "scanner_site"]

    features = metadata_df[feature_columns].copy()
    features["age"] = (features["age"] - features["age"].mean()) / (features["age"].std() + 1e-8)
    features["scanner_site"] = features["scanner_site"] / max(features["scanner_site"].max(), 1)

    matrix = features.values.astype("float32")
    sim = cosine_similarity(matrix)

    rows = []

    for i in range(sim.shape[0]):
        # Sort most similar cases, skipping itself.
        neighbors = np.argsort(sim[i])[::-1]
        neighbors = [j for j in neighbors if j != i][:top_k]

        for j in neighbors:
            rows.append({
                "source_case": metadata_df.iloc[i].get("patient_id", i),
                "target_case": metadata_df.iloc[j].get("patient_id", j),
                "similarity": float(sim[i, j]),
            })

    return pd.DataFrame(rows)


def save_case_similarity_graph(metadata_path, output_path, top_k=5):
    metadata_df = pd.read_csv(metadata_path)
    edge_df = build_case_similarity_edges(metadata_df, top_k=top_k)
    edge_df.to_csv(output_path, index=False)
    return edge_df
