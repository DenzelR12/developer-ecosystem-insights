"""Raw, normalized, and analytics-ready transformations with record quarantine."""
from __future__ import annotations
from datetime import datetime
from typing import Any
from src.contracts import validate_repository_contract

def bronze_to_silver(snapshot: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    accepted, quarantined = [], []
    for raw in snapshot.get("repositories", []):
        violations = validate_repository_contract(raw)
        if violations:
            quarantined.append({"raw_record": raw, "violations": violations})
            continue
        accepted.append({"repository_id": raw["id"], "repository_name": raw["full_name"], "source_updated_at": raw["updated_at"], "stars": raw["stargazers_count"], "forks": raw["forks_count"], "source": snapshot.get("source", "GitHub REST API"), "snapshot_at": snapshot["retrieved_at"]})
    return accepted, quarantined

def silver_to_gold(repositories: list[dict[str, Any]]) -> dict[str, Any]:
    return {"metric_grain": "one source snapshot across distinct repositories", "repository_count": len(repositories), "total_stars": sum(row["stars"] for row in repositories), "total_forks": sum(row["forks"] for row in repositories), "metric_caveat": "Stars and forks are ecosystem-interest signals. They are not unique developers, customers, retention, or revenue.", "generated_at": datetime.utcnow().isoformat() + "Z"}
