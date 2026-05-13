# Data Privacy and De-identification

## Important

CAPSDAC data may include personally identifiable information (PII) or sensitive child-level information.  
Raw CAPSDAC data should **not** be committed to GitHub.

## CDE Data Warehouse Access

The CDE data warehouse is accessible only through the issued laptop / approved secure environment.  
This public portfolio package does not include CDE warehouse credentials, access instructions, or raw child-level data.

## What Is Included in This Public Package

This package includes only:

```text
data/raw/Child_April_deidentified_sample.csv
```

This file is a de-identified sample designed for demonstrating the pipeline structure.

## What Was Removed

The original raw file was removed from the shareable package:

```text
data/raw/Child_April_deidentified_sample.csv
```

Any table that may have been derived from raw row-level records was removed or replaced with safe de-identified sample tables.

## De-identification Approach

The package uses these principles:

1. Do not share child-level records.
2. Do not share direct identifiers.
3. Replace real site/vendor identifiers with de-identified labels.
4. Use aggregate enrollment counts.
5. Use approximate locations only for visualization.
6. Keep only fields needed to demonstrate forecasting and reporting logic.

## Local Secure Workflow

Use this workflow on the issued laptop only:

```text
CDE warehouse / secure source
        ↓
Local authorized export
        ↓
Local de-identification
        ↓
Aggregate tables
        ↓
Portfolio-safe sample outputs
        ↓
GitHub package
```

## De-identification Utility

A helper module is included:

```text
src/deidentify.py
```

## Recommended GitHub Rule

Only commit:

```text
de-identified sample data
aggregate outputs
figures
documentation
code
```

Never commit:

```text
raw child-level data
names
birth dates
addresses
phone numbers
emails
IDs that can identify a child or family
warehouse credentials
secure connection details
```
