from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]

EVAL_DIR = ROOT / "evaluation"
FIGURE_DIR = ROOT / "outputs" / "figures"
FIGURE_DIR.mkdir(parents=True, exist_ok=True)

TRAINING_LOSS_PATH = EVAL_DIR / "training_loss.csv"
EVALUATION_REPORT_PATH = EVAL_DIR / "evaluation_report.csv"
EVALUATION_SUMMARY_PATH = EVAL_DIR / "evaluation_summary.csv"
TOP_10_PATH = EVAL_DIR / "top_10_generated_candidates.csv"


def plot_training_loss():
    """
    Generate training loss curve from evaluation/training_loss.csv.
    """
    loss_df = pd.read_csv(TRAINING_LOSS_PATH)

    plt.figure(figsize=(8, 5))
    plt.plot(loss_df["epoch"], loss_df["loss"], marker="o")
    plt.title("Training Loss Curve")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.grid(True)

    output_path = FIGURE_DIR / "training_loss_curve.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def plot_druglikeness_histogram():
    """
    Generate histogram of molecule drug-likeness proxy scores.
    """
    ranked_df = pd.read_csv(EVALUATION_REPORT_PATH)

    plt.figure(figsize=(8, 5))
    ranked_df["druglikeness_proxy"].hist()
    plt.title("Histogram of Molecule Drug-likeness Proxy Scores")
    plt.xlabel("Drug-likeness Proxy Score")
    plt.ylabel("Number of Generated Molecules")
    plt.grid(True)

    output_path = FIGURE_DIR / "druglikeness_score_histogram.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def save_top_10_candidates():
    """
    Save top 10 generated candidates table as CSV.
    """
    ranked_df = pd.read_csv(EVALUATION_REPORT_PATH)
    top_10 = ranked_df.head(10)
    top_10.to_csv(TOP_10_PATH, index=False)

    print(f"Saved: {TOP_10_PATH}")


def plot_summary_chart():
    """
    Generate validity / novelty / diversity / drug-likeness summary chart.
    """
    summary_df = pd.read_csv(EVALUATION_SUMMARY_PATH)

    chart_df = pd.DataFrame({
        "metric": [
            "Validity Rate",
            "Novelty Rate",
            "Average Diversity Proxy",
            "Average Drug-likeness Proxy",
        ],
        "value": [
            float(summary_df.loc[0, "validity_rate"]),
            float(summary_df.loc[0, "novelty_rate"]),
            float(summary_df.loc[0, "average_diversity_proxy"]),
            float(summary_df.loc[0, "average_druglikeness_proxy"]),
        ],
    })

    plt.figure(figsize=(9, 5))
    plt.bar(chart_df["metric"], chart_df["value"])
    plt.title("Validity / Novelty / Diversity Summary")
    plt.ylabel("Metric Value")
    plt.xticks(rotation=25, ha="right")
    plt.grid(axis="y")

    output_path = FIGURE_DIR / "validity_novelty_diversity_summary.png"
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()

    print(f"Saved: {output_path}")


def generate_all_visual_outputs():
    """
    Run all visual output steps.
    """
    plot_training_loss()
    plot_druglikeness_histogram()
    save_top_10_candidates()
    plot_summary_chart()


if __name__ == "__main__":
    generate_all_visual_outputs()
