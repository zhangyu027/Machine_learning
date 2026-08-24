-- Executive forecast checks for CAPSDAC planning.
SELECT
  ForecastMonth,
  SUM(PredictedEnrollment) AS statewide_predicted_enrollment
FROM `capsdac2-ml.capsdac_analytics.vendor_forecast`
GROUP BY ForecastMonth
ORDER BY ForecastMonth;

-- Vendor concentration risk: top vendors as share of total forecasted enrollment.
WITH vendor_month AS (
  SELECT ForecastMonth, VendorNumber, VendorName, SUM(PredictedEnrollment) AS vendor_pred
  FROM `capsdac2-ml.capsdac_analytics.vendor_forecast`
  GROUP BY ForecastMonth, VendorNumber, VendorName
), ranked AS (
  SELECT *, RANK() OVER(PARTITION BY ForecastMonth ORDER BY vendor_pred DESC) AS rnk,
         SUM(vendor_pred) OVER(PARTITION BY ForecastMonth) AS month_total
  FROM vendor_month
)
SELECT ForecastMonth, VendorNumber, VendorName, vendor_pred, vendor_pred / month_total AS share_of_month
FROM ranked
WHERE rnk <= 10
ORDER BY ForecastMonth, vendor_pred DESC;
