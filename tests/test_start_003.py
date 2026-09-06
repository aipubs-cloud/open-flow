import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
MANIFEST = ROOT / "workflows/AIPUBS-START/003-explore-repository/workflow.yaml"


def load_schema(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def validate(name, instance):
    return list(Draft202012Validator(load_schema(name)).iter_errors(instance))


def test_start_003_manifest_matches_current_workflow_contract():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    assert not validate("workflow.schema.json", manifest)
    assert manifest["id"] == "AIPUBS-START-003"
    assert manifest["mode"] == "observe"
    assert manifest["type"] == "atomic"


def test_start_003_artifact_schemas_are_valid():
    for name in (
        "repository-map.schema.json",
        "architecture-map.schema.json",
        "execution-map.schema.json",
        "learning-summary.schema.json",
        "start-003-result.schema.json",
    ):
        Draft202012Validator.check_schema(load_schema(name))


def test_execution_artifact_preserves_candidate_status():
    valid = {
        "schema_version": "owf.execution-map.v1",
        "candidate_entry_points": [{"path": "src/main.py", "basis": "entrypoint naming pattern"}],
        "observed_run_scripts": [],
        "runtime_unknowns": ["Production runtime path not established."],
    }
    assert not validate("execution-map.schema.json", valid)


def test_learning_summary_requires_a_single_next_workflow():
    valid = {
        "schema_version": "owf.learning-summary.v1",
        "learner_understands": ["repository structure"],
        "learner_needs_review": [],
        "important_locations": ["src/"],
        "recommended_next_workflow": {
            "id": "AIPUBS-GIT-001",
            "reason": "Learner wants Git fundamentals.",
        },
    }
    assert not validate("learning-summary.schema.json", valid)
    invalid = {**valid, "recommended_next_workflow": []}
    assert validate("learning-summary.schema.json", invalid)


def test_result_requires_explicit_unknowns_and_one_next_workflow():
    valid = {
        "workflow_id": "AIPUBS-START-003",
        "version": "0.1.0",
        "status": "completed",
        "evidence": {"observed": [], "inferred": [], "unknown": ["deployment"]},
        "artifacts": ["repository-map", "architecture-map", "execution-map", "learning-summary"],
        "graduation": {"status": "passed", "criteria": ["evidence states preserved"]},
        "next_workflow": {"id": "AIPUBS-GIT-001", "reason": "Git fundamentals requested."},
    }
    assert not validate("start-003-result.schema.json", valid)
