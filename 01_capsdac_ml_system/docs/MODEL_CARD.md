# CAPSDAC Forecasting Model Card

## Model Purpose

Forecast near-term CSPP enrollment using monthly CAPSDAC child snapshot data.

## Intended Use

- Program planning
- Enrollment monitoring
- Identifying county/site/vendor contribution patterns
- Early awareness of near-term enrollment movement

## Not Intended For

- Final certified enrollment counts
- Individual child-level decision-making
- Eligibility determination
- High-stakes automated administrative action

## Inputs

Potential input fields include:

- report month
- site/preschool identifier
- vendor/LEA
- county
- historical enrollment counts
- derived lag features
- rolling enrollment summaries

## Outputs

- forecasted enrollment by month
- forecasted enrollment by site
- forecasted enrollment by vendor/LEA
- contribution percentages
- growth rankings
- visual maps and charts

## Limitations

- Forecasts depend on quality and consistency of source snapshots.
- Short historical windows can limit model stability.
- Vendor/site changes may affect comparability over time.
- Forecasts should be interpreted with operational knowledge.
- Geospatial output depends on county/site coordinate mapping quality.

## Human Review

Forecasts should be reviewed by CAPSDAC analysts or program staff before use in reporting or planning.
