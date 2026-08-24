# V4 12-Month Design Decision

## Source data observed

The supplied CAPSDAC child extract spans July 2025 through June 2026 and contains 12 distinct reporting months. The implementation therefore treats one year as the current historical boundary rather than pretending annual lags are statistically mature.

## Forecast design

The production-facing default is H+1 next-month enrollment at the preschool-site level. Three prior lags and a shifted rolling mean preserve short-term dynamics while leaving multiple feature months for expanding-window validation.

## Privacy boundary

The child adapter uses `ChildUniqueID` only transiently for within-site/month de-duplication. Child identifiers and direct PII never appear in the aggregate feature table. Real child data is excluded from Git and from the release ZIP.

## Decision-science extension

The same site-month layer can support anomaly detection, certification reconciliation, program-risk scoring, and hypothesis-driven analysis when certification and agency-level reporting tables are joined. Those extensions should remain analytically separate from the enrollment forecast target.
