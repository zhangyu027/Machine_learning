import pandas as pd


def vendor_contribution(site_forecast: pd.DataFrame) -> pd.DataFrame:
    return (
        site_forecast.groupby(["ForecastMonth", "VendorNumber", "LEAName"], as_index=False)["PredictedEnrollment"]
        .sum()
        .sort_values(["ForecastMonth", "PredictedEnrollment"], ascending=[True, False])
    )


def statewide_forecast(site_forecast: pd.DataFrame) -> pd.DataFrame:
    return site_forecast.groupby("ForecastMonth", as_index=False)["PredictedEnrollment"].sum()
