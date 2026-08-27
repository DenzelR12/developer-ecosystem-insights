"""Metric registry: definitions and caveats travel with every dashboard number."""

from dataclasses import dataclass


@dataclass(frozen=True)
class MetricDefinition:
    name: str
    numerator: str
    denominator: str | None
    unit: str
    source: str
    aggregation_rule: str
    caveat: str


METRICS = {
    "active_repositories": MetricDefinition(
        name="Active repositories",
        numerator="Distinct repositories with at least one qualifying activity event in the reporting window",
        denominator=None,
        unit="repositories",
        source="GitHub REST API",
        aggregation_rule="Count distinct repository IDs within a fixed organization and reporting window.",
        caveat="Repository activity is a platform engagement signal, not a count of unique developers or customers.",
    ),
    "repository_star_delta": MetricDefinition(
        name="Repository star delta",
        numerator="Current stars minus prior comparable snapshot stars for the same repository",
        denominator=None,
        unit="stars",
        source="GitHub REST API snapshots",
        aggregation_rule="Compute per repository, then report distribution or an explicitly labeled total.",
        caveat="Stars are a weak interest signal. Do not treat them as adoption, retention, revenue, or customer satisfaction.",
    ),
    "contributor_activity": MetricDefinition(
        name="Contributor activity",
        numerator="Observed contribution events in a defined repository and reporting window",
        denominator=None,
        unit="events",
        source="GitHub REST API",
        aggregation_rule="Do not sum across repositories unless contributor identities are deduplicated and access coverage is known.",
        caveat="Public telemetry can omit private work, bots, mirrored repositories, and events outside API retention windows.",
    ),
}
