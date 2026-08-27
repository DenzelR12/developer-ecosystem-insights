# Data Contract and Quality Policy

## Purpose
This contract protects downstream customer-success analytics from silently changing APIs, partial responses, incompatible field types, and misleading aggregation.

## Source contract
The GitHub repository snapshot contract is versioned in `src/contracts.py`. Every record must contain a stable repository ID, qualified name, source update timestamp, star count, and fork count. Invalid records are quarantined with the original record and each violated rule rather than coerced into a plausible value.

## Pipeline layers
| Layer | Purpose | Output |
|---|---|---|
| Bronze | Immutable source snapshot with retrieval metadata | Raw API response |
| Silver | Validated, normalized repository records | Accepted records plus quarantine records |
| Gold | Dashboard-ready aggregate with metric grain and caveat | Adoption-health summary |

## Quality policy
Publication is blocked when a snapshot is stale, empty, materially incomplete, or outside expected volume bounds. A quarantine count should be visible to consumers; a successful job is not proof that every source record was valid.

## Metric policy
Repository telemetry is not customer telemetry. Stars, forks, and activity must not be relabeled as retention, revenue, unique developers, or customer satisfaction.