# Operating Model: From Question to Defensible Metric

## 1. Define before collecting
Every request begins with a written measurement contract: decision owner, question, population, event, time window, source, baseline date, success threshold, and known coverage limits.

## 2. Capture a baseline
Before an intervention launches, capture the prior comparable period and document expected data delays.

## 3. Ingest and validate
Collect source data through versioned API clients. Validate schema, freshness, completeness, and volume. Quarantine invalid records. Fail closed if quality gates fail.

## 4. Publish with caveats
Expose data lineage, retrieval time, metric grain, and aggregation caveats beside dashboard outputs.

## 5. Investigate anomalies
Test source availability, definition changes, duplicates, API changes, and lag before claiming customer behavior changed.

## 6. Review with agents and humans
Require independent verification and adversarial review for double counting, broken assumptions, unsupported attribution, privacy, and security issues.