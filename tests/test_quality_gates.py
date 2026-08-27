from datetime import UTC, datetime, timedelta

import pytest

from src.quality_gates import completeness_gate, freshness_gate, require_quality, volume_gate


def snapshot(retrieved_at=None, records=None):
    records = records if records is not None else [{"id": 1, "name": "repo", "updated_at": "2026-08-27T00:00:00Z"}]
    return {
        "retrieved_at": retrieved_at or datetime.now(UTC).isoformat(),
        "record_count": len(records),
        "repositories": records,
    }


def test_fresh_snapshot_passes():
    assert freshness_gate(snapshot()).passed


def test_stale_snapshot_fails():
    stale = (datetime.now(UTC) - timedelta(hours=25)).isoformat()
    assert not freshness_gate(snapshot(retrieved_at=stale)).passed


def test_missing_required_values_fail_completeness():
    assert not completeness_gate(snapshot(records=[{"id": 1, "name": None, "updated_at": None}])).passed


def test_empty_snapshot_fails_volume():
    assert not volume_gate(snapshot(records=[])).passed


def test_failed_gate_blocks_publication():
    with pytest.raises(ValueError, match="Publication blocked"):
        require_quality(snapshot(retrieved_at="not-a-date"))
