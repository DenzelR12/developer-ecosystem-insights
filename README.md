# Developer Ecosystem Insights

A production-style reference implementation for converting public developer-platform telemetry into trustworthy adoption signals.

The project demonstrates the engineering discipline behind customer-success insights: API ingestion, versioned data contracts, quality gates, quarantine handling, metric definitions, baseline thinking, and a documented multi-agent verification workflow.

## Why this exists
Developer ecosystem data changes quickly and can be easy to over-interpret. A dashboard that is technically fresh but semantically wrong is worse than no dashboard. This project makes uncertainty, source lineage, and aggregation limits visible before a metric reaches an executive or customer-facing audience.

## Architecture
```text
GitHub REST API
  -> bounded retries, rate-limit awareness, source metadata
  -> Bronze: immutable source snapshot
  -> Source contract validation
  -> Silver: normalized records + invalid-record quarantine
  -> freshness, completeness, and volume quality gates
  -> Gold: dashboard-ready adoption-health model with metric caveats
  -> publication only after tests and gates pass
```

## Engineering workflow
| Capability | Implementation |
|---|---|
| API ingestion | `src/github_telemetry.py`: timeouts, bounded retries, GitHub rate-limit behavior, environment-based authentication, response validation |
| Data contract | `src/contracts.py`: versioned required fields, types, nullability, and stable identifiers |
| Quarantine | `src/transformations.py`: invalid source records are retained with violated rules rather than silently coerced |
| Quality gates | `src/quality_gates.py`: freshness, completeness, and source-volume checks that block downstream publication |
| Analytics model | `silver_to_gold()`: point-in-time repository health summary carrying metric grain and caveats |
| Metric honesty | `src/metric_definitions.py`: definitions, source, aggregation rules, and limits live alongside the metrics |
| Automated verification | Pytest suite plus GitHub Actions CI on every push and pull request |
| Agentic delivery | `AGENTS.md`: Planner, Builder, Verifier, and Adversarial Reviewer roles with release gates |

## Run locally
```bash
export GITHUB_TOKEN=your_token
python -m src.github_telemetry --org NVIDIA --output data/github_snapshot.json
python -m src.pipeline --input data/github_snapshot.json
pytest -q
```

## What the model measures
This reference model produces repository-level ecosystem signals such as observed repository count, stars, and forks. It does not claim that these signals measure unique developers, customers, retention, revenue, customer satisfaction, or causal impact.

## Scope
This is a portable Python reference implementation intended to demonstrate data-product and analytics-engineering patterns. It is not an NVIDIA internal system and does not claim deployment in Databricks. The validated Silver and Gold interfaces are deliberately suitable for a Spark/Delta Lake implementation in an enterprise environment.