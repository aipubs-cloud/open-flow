import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_workflow_schema_accepts_canonical_example():
    schema = load_json(SCHEMAS / "workflow.schema.json")
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(document), key=lambda e: list(e.path))
    assert not errors, "\n".join(error.message for error in errors)


def test_result_schema_has_stable_status_contract():
    schema = load_json(SCHEMAS / "result.schema.json")
    validator = Draft202012Validator(schema)
    valid = {
        "workflow_id": "OWF-002",
        "workflow_version": "0.1.0",
        "status": "success",
        "mode": "observe",
        "evidence": [{"kind": "FACT", "statement": "README.md exists."}],
        "verification": {"performed": True, "checks": ["filesystem scan completed"]},
    }
    assert validator.is_valid(valid)


def test_result_schema_rejects_unknown_status():
    schema = load_json(SCHEMAS / "result.schema.json")
    validator = Draft202012Validator(schema)
    invalid = {
        "workflow_id": "OWF-002",
        "workflow_version": "0.1.0",
        "status": "complete",
        "mode": "observe",
        "evidence": [],
        "verification": {"performed": False, "checks": []},
    }
    assert not validator.is_valid(invalid)
