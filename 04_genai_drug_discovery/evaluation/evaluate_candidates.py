from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TRAIN_PATH = ROOT / "data" / "demo_smiles.csv"
SCREENED_PATH = ROOT / "molecule_generation" / "screened_candidates.csv"
REPORT_PATH = ROOT / "evaluation" / "evaluation_report.csv"
SUMMARY_PATH = ROOT / "evaluation" / "evaluation_summary.csv"
METRIC_TABLE_PATH = ROOT / "evaluation" / "real_evaluation_table.csv"


def evaluate_candidates(
    train_path=TRAIN_PATH,
    screened_path=SCREENED_PATH,
    report_path=REPORT_PATH,
    summary_path=SUMMARY_PATH,
):
    train_df = pd.read_csv(train_path)
    screened_df = pd.read_csv(screened_path)

    training_set = set(train_df["smiles"].astype(str).tolist())

    screened_df["is_novel"] = screened_df["generated_smiles"].apply(
        lambda x: x not in training_set
    )

    screened_df["diversity_proxy"] = screened_df["generated_smiles"].apply(
        lambda x: len(set(str(x)))
    )

    ranked_df = screened_df.sort_values(
        ["is_valid", "is_novel", "druglikeness_proxy", "diversity_proxy"],
        ascending=[False, False, False, False],
    ).reset_index(drop=True)

    summary = {
        "num_training_molecules": len(train_df),
        "num_generated_unique_molecules": len(ranked_df),
        "validity_rate": ranked_df["is_valid"].mean(),
        "novelty_rate": ranked_df["is_novel"].mean(),
        "average_diversity_proxy": ranked_df["diversity_proxy"].mean(),
        "average_druglikeness_proxy": ranked_df["druglikeness_proxy"].mean(),
    }

    ranked_df.to_csv(report_path, index=False)
    summary_df = pd.DataFrame([summary])
    summary_df.to_csv(summary_path, index=False)

    # Real evaluation table for README / notebook / portfolio reporting
    metric_table = pd.DataFrame({
        "Metric": [
            "Validity rate",
            "Novelty",
            "Diversity",
            "Top candidates",
        ],
        "Meaning": [
            "Percent generated molecules that pass basic checks",
            "Generated molecules that are not copied from the training data",
            "How different generated molecules are, using the diversity proxy",
            "Best generated molecules after scoring and ranking",
        ],
        "Result": [
            f"{summary['validity_rate']:.2%}",
            f"{summary['novelty_rate']:.2%}",
            f"{summary['average_diversity_proxy']:.3f}",
            "Saved in evaluation/top_10_generated_candidates.csv after visualization",
        ],
    })

    metric_table.to_csv(METRIC_TABLE_PATH, index=False)

    print(f"Saved evaluation report to: {report_path}")
    print(f"Saved evaluation summary to: {summary_path}")
    print(f"Saved real evaluation table to: {METRIC_TABLE_PATH}")

    return ranked_df, summary_df, metric_table


if __name__ == "__main__":
    evaluate_candidates()
