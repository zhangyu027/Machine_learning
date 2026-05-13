import argparse
from pathlib import Path
import pandas as pd
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

from rag.vector_store import search_index


def evaluate_retrieval(eval_file: str, index_dir: str = "vector_store", top_k: int = 5):
    df = pd.read_csv(eval_file)
    rows = []

    for _, row in df.iterrows():
        question = str(row["question"])
        expected = str(row["expected_source_keyword"])

        results = search_index(question, index_dir, top_k=top_k)
        retrieved_sources = [item["filename"] for item in results]
        hit = any(expected in source for source in retrieved_sources)

        rows.append({
            "question": question,
            "expected_source_keyword": expected,
            "hit_in_top_k": hit,
            "top_sources": ", ".join(retrieved_sources)
        })

    out_df = pd.DataFrame(rows)
    hit_rate = out_df["hit_in_top_k"].mean() if len(out_df) else 0

    print(f"Top-{top_k} hit rate: {hit_rate:.2%}")
    print(out_df)

    output_path = ROOT / "evaluation" / "retrieval_evaluation_results.csv"
    out_df.to_csv(output_path, index=False)
    print(f"Saved results to: {output_path}")

    return out_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--eval-file", default="evaluation/sample_eval_questions.csv")
    parser.add_argument("--index-dir", default="vector_store")
    parser.add_argument("--top-k", type=int, default=5)
    args = parser.parse_args()

    evaluate_retrieval(args.eval_file, args.index_dir, args.top_k)
