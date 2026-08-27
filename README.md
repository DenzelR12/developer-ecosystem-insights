# Developer Ecosystem Insights

A reference implementation for converting public developer-platform telemetry into trustworthy adoption metrics.

Built to demonstrate the engineering patterns behind a Customer Success Insights function: API ingestion, schema contracts, freshness and quality gates, defensible metric definitions, and a documented agent-assisted development workflow.

## What this repository does

1. Pulls repository and contributor telemetry from the GitHub REST API.
2. Validates the incoming records against an explicit schema.
3. Stops downstream publication when freshness, completeness, or volume-anomaly gates fail.
4. Produces a metric-ready normalized snapshot with source metadata.
5. Registers each metric with a definition, owner, aggregation rule, and caveat so dashboards do not overclaim what the data can say.

## Architecture

```text
GitHub REST API
  -> retry and rate limit aware ingestion
  -> schema validation and normalization
  -> quality gates: freshness, null rate, row count, volume anomaly
  -> approved snapshot or fail closed result
  -> metric registry and dashboard layer
```

The pipeline intentionally fails closed. A stale or malformed source should not silently become an executive metric.

## Run locally

```bash
export GITHUB_TOKEN=your_token
python -m src.github_telemetry --org NVIDIA --output data/github_snapshot.json
python -m src.pipeline --input data/github_snapshot.json
pytest -q
```

The GitHub token is optional for public endpoints but recommended to avoid restrictive rate limits. Do not commit tokens or generated data containing sensitive information.

## Metric honesty

A contribution count is not a customer count. A GitHub star is not retention. Repo-level activity cannot be summed across overlapping organizations without a deduplication key. The `src/metric_definitions.py` registry captures these limits beside the metric definitions rather than burying them in dashboard footnotes.

## Agentic workflow

This repository was structured for agent-assisted delivery. `AGENTS.md` defines separate planner, builder, verifier, and adversarial-review responsibilities. No output is considered publishable until schema checks, quality gates, and tests pass.

## Scope

This is a portable Python reference implementation, not a claim that it runs on NVIDIA internal systems or is deployed in Databricks. The interfaces are intentionally designed so the normalized output can be written to a Spark or Delta Lake table in an enterprise environment.