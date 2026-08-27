from datetime import UTC, datetime
from src.contracts import validate_repository_contract
from src.transformations import bronze_to_silver, silver_to_gold

def valid_record():
    return {"id": 1, "name": "demo", "full_name": "org/demo", "updated_at": "2026-08-27T00:00:00Z", "stargazers_count": 12, "forks_count": 3}
def snapshot(records):
    return {"source": "GitHub REST API", "retrieved_at": datetime.now(UTC).isoformat(), "repositories": records, "record_count": len(records)}
def test_contract_accepts_valid_record(): assert validate_repository_contract(valid_record()) == []
def test_contract_reports_missing_and_wrong_type_fields():
    record=valid_record(); record.pop("full_name"); record["forks_count"]="3"
    violations=validate_repository_contract(record)
    assert any("full_name" in v for v in violations); assert any("forks_count" in v for v in violations)
def test_invalid_records_are_quarantined():
    bad=valid_record(); bad["id"]="not-an-int"
    accepted, quarantined=bronze_to_silver(snapshot([valid_record(),bad]))
    assert len(accepted)==1 and len(quarantined)==1
def test_gold_model_retains_metric_caveat():
    accepted,_=bronze_to_silver(snapshot([valid_record()])); model=silver_to_gold(accepted)
    assert model["repository_count"]==1; assert "not unique developers" in model["metric_caveat"]
