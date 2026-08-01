# ADR-006: Select Azure Databricks for primary lakehouse transformation

## Status
Accepted

## Context
The enterprise platform requires a repeatable decision that multiple teams can implement consistently.

## Decision
Use Azure Databricks for Delta Lake transformations and scalable engineering workloads; use Synapse Serverless for governed SQL access.

## Alternatives considered
Synapse Spark, Fabric notebooks, and SQL-only transformation were considered.

## Benefits and rationale
Databricks offers mature Delta capabilities and engineering productivity, while Synapse Serverless reduces operational burden for SQL consumers.

## Risks and consequences
Vendor concentration, skills requirements, and workspace governance must be managed.

## Revisit triggers
Revisit when Fabric capabilities, cost, or enterprise standards materially change.
