"""Rate-limit aware GitHub REST API ingestion with schema validation."""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import requests

API_ROOT = "https://api.github.com"
REQUIRED_REPOSITORY_FIELDS = {"id", "name", "full_name", "updated_at", "stargazers_count", "forks_count"}


class GitHubIngestionError(RuntimeError):
    pass


def _headers(token: str | None) -> dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def get_json(url: str, token: str | None = None, attempts: int = 3) -> Any:
    """Fetch JSON with bounded retries and explicit rate-limit behavior."""
    for attempt in range(attempts):
        response = requests.get(url, headers=_headers(token), timeout=30)
        if response.status_code == 200:
            return response.json()
        if response.status_code in {429, 403} and response.headers.get("X-RateLimit-Remaining") == "0":
            reset = int(response.headers.get("X-RateLimit-Reset", "0"))
            wait_seconds = max(1, reset - int(time.time()))
            if attempt == attempts - 1:
                raise GitHubIngestionError(f"GitHub rate limit exhausted; reset in {wait_seconds}s")
            time.sleep(min(wait_seconds, 60))
            continue
        if response.status_code >= 500 and attempt < attempts - 1:
            time.sleep(2 ** attempt)
            continue
        raise GitHubIngestionError(f"GitHub API request failed: {response.status_code} {response.text[:200]}")
    raise GitHubIngestionError("GitHub request exhausted retries")


def validate_repositories(repositories: list[dict[str, Any]]) -> None:
    if not isinstance(repositories, list) or not repositories:
        raise GitHubIngestionError("No repository records returned; refusing to create an empty snapshot")
    for index, repository in enumerate(repositories):
        missing = REQUIRED_REPOSITORY_FIELDS - repository.keys()
        if missing:
            raise GitHubIngestionError(f"Repository record {index} missing required fields: {sorted(missing)}")


def ingest_org_repositories(org: str, token: str | None = None) -> dict[str, Any]:
    repositories = get_json(f"{API_ROOT}/orgs/{org}/repos?per_page=100&sort=updated", token)
    validate_repositories(repositories)
    return {
        "source": "GitHub REST API",
        "entity_type": "organization_repositories",
        "entity": org,
        "retrieved_at": datetime.now(UTC).isoformat(),
        "record_count": len(repositories),
        "repositories": repositories,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--org", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    snapshot = ingest_org_repositories(args.org, os.getenv("GITHUB_TOKEN"))
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2), encoding="utf-8")
    print(f"Wrote {snapshot['record_count']} records to {output}")


if __name__ == "__main__":
    main()
