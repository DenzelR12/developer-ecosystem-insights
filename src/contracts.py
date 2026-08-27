"""Versioned source and analytics contracts for developer-ecosystem telemetry."""

from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True)
class FieldContract:
    name: str
    expected_type: type | tuple[type, ...]
    nullable: bool
    description: str

REPOSITORY_SOURCE_CONTRACT_V1 = (
    FieldContract("id", int, False, "Stable GitHub repository identifier"),
    FieldContract("name", str, False, "Repository name"),
    FieldContract("full_name", str, False, "Owner-qualified repository name"),
    FieldContract("updated_at", str, False, "GitHub ISO-8601 update timestamp"),
    FieldContract("stargazers_count", int, False, "Point-in-time interest signal, not adoption"),
    FieldContract("forks_count", int, False, "Point-in-time reuse signal, not unique developers"),
)

def validate_repository_contract(record: dict[str, Any]) -> list[str]:
    violations: list[str] = []
    for field in REPOSITORY_SOURCE_CONTRACT_V1:
        value = record.get(field.name)
        if value is None:
            if not field.nullable:
                violations.append(f"missing required field: {field.name}")
            continue
        if not isinstance(value, field.expected_type):
            violations.append(f"invalid type for {field.name}: expected {field.expected_type}, got {type(value)}")
    return violations
