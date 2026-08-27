"""Fail-closed data quality gates for telemetry snapshots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class GateResult:
    name: str
    passed: bool
    detail: str


def freshness_gate(snapshot: dict[str, Any], max_age_hours: int = 24) -> GateResult:
    value = snapshot.get("retrieved_at")
    if not value:
        return GateResult("freshness", False, "retrieved_at is missing")
    try:
        retrieved_at = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return GateResult("freshness", False, "retrieved_at is not ISO-8601")
    age_hours = (datetime.now(UTC) - retrieved_at).total_seconds() / 3600
    return GateResult("freshness", age_hours <= max_age_hours, f"age_hours={age_hours:.2f}; max={max_age_hours}")


def completeness_gate(snapshot: dict[str, Any], max_null_rate: float = 0.02) -> GateResult:
    records = snapshot.get("repositories", [])
    required = ("id", "name", "updated_at")
    if not records:
        return GateResult("completeness", False, "no records")
    nulls = sum(1 for row in records for field in required if row.get(field) in (None, ""))
    rate = nulls / (len(records) * len(required))
    return GateResult("completeness", rate <= max_null_rate, f"null_rate={rate:.4f}; max={max_null_rate:.4f}")


def volume_gate(snapshot: dict[str, Any], expected_min_records: int = 1, expected_max_records: int = 1000) -> GateResult:
    count = snapshot.get("record_count", 0)
    passed = expected_min_records <= count <= expected_max_records
    return GateResult("volume", passed, f"record_count={count}; expected=[{expected_min_records}, {expected_max_records}]")


def run_quality_gates(snapshot: dict[str, Any]) -> list[GateResult]:
    return [freshness_gate(snapshot), completeness_gate(snapshot), volume_gate(snapshot)]


def require_quality(snapshot: dict[str, Any]) -> None:
    failed = [gate for gate in run_quality_gates(snapshot) if not gate.passed]
    if failed:
        details = "; ".join(f"{gate.name}: {gate.detail}" for gate in failed)
        raise ValueError(f"Publication blocked by data quality gates: {details}")
