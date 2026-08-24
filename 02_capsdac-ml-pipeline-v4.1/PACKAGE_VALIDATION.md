# Package Validation

Validated on 2026-08-23.

- Unit tests: 7 passed.
- Synthetic 12-month demo pipeline: completed successfully.
- Demo coverage: July 2025 through June 2026, 40 synthetic sites, 8 synthetic agencies.
- Forecast horizon: 1 month.
- Expanding-window validation: enabled.
- Real child-level data: not included in this package.
- Real supplied extract was inspected as 12 distinct months (Jul-2025 through Jun-2026), 786,718 source rows, 2,161 preschool site codes, and 324 vendors/agencies. The adapter is designed for that schema.

The raw CAPSDAC child ZIP must remain outside source control under `data/private/` or another approved secure path.
