from pathlib import Path
import json
import pandas as pd
import matplotlib.pyplot as plt


def generate_figures(
    gold_csv="outputs/tables/gold_monthly_program_demand.csv",
    predictions_csv="outputs/tables/forecast_predictions.csv",
    metrics_json="outputs/tables/forecast_model_metrics.json",
    quality_csv="outputs/tables/data_quality_report.csv",
    output_dir="outputs/figures",
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    gold = pd.read_csv(gold_csv)
    pred = pd.read_csv(predictions_csv)
    metrics = json.loads(Path(metrics_json).read_text())

    gold["event_month"] = pd.to_datetime(gold["event_month"])

    monthly = gold.groupby("event_month", as_index=False)["target_next_month_demand"].sum()

    plt.figure(figsize=(9, 5))
    plt.plot(monthly["event_month"], monthly["target_next_month_demand"], marker="o")
    plt.title("Gold Layer: Monthly Program Demand")
    plt.xlabel("Month")
    plt.ylabel("Demand")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.savefig(output_dir / "monthly_program_demand_trend.png", bbox_inches="tight")
    plt.close()

    plt.figure(figsize=(8, 5))
    plt.scatter(pred["actual_demand"], pred["predicted_demand"], alpha=0.6)
    plt.title("Forecast Model: Actual vs Predicted Demand")
    plt.xlabel("Actual Demand")
    plt.ylabel("Predicted Demand")
    plt.grid(True)
    plt.savefig(output_dir / "actual_vs_predicted_demand.png", bbox_inches="tight")
    plt.close()

    metric_df = pd.DataFrame({
        "metric": ["mae", "rmse", "r2"],
        "value": [metrics["mae"], metrics["rmse"], metrics["r2"]],
    })
    plt.figure(figsize=(7, 5))
    plt.bar(metric_df["metric"], metric_df["value"])
    plt.title("Forecast Model Metrics")
    plt.grid(axis="y")
    plt.savefig(output_dir / "forecast_model_metrics.png", bbox_inches="tight")
    plt.close()

    if Path(quality_csv).exists():
        q = pd.read_csv(quality_csv)
        pass_rate = q["passed"].mean()
        plt.figure(figsize=(5, 5))
        plt.bar(["quality_pass_rate"], [pass_rate])
        plt.ylim(0, 1)
        plt.title("Data Quality Pass Rate")
        plt.grid(axis="y")
        plt.savefig(output_dir / "data_quality_pass_rate.png", bbox_inches="tight")
        plt.close()

    return list(output_dir.glob("*.png"))


if __name__ == "__main__":
    print(generate_figures())
