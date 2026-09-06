import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
MANIFEST = ROOT / "workflows/AIPUBS-START/003-explore-repository/workflow.yaml"
REGISTRY = ROOT / "registry/workflows.yaml"


def load_schema(name):
    return json.loads((SCHEMAS / name).read_text(encoding="utf-8"))


def validate(name, instance):
    return list(Draft202012Validator(load_schema(name)).iter_errors(instance))


def test_start_003_manifest_matches_current_workflow_contract_and_registry():
    manifest = yaml.safe_load(MANIFEST.read_text(encoding="utf-8"))
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert not validate("workflow.schema.json", manifest)
    assert manifest["id"] == "AIPUBS-START-003"
    assert manifest["name"] == "Explore a Repository"
    assert manifest["category"] == "start"
    assert manifest["mode"] == "observe"
    assert manifest["type"] == "atomic"

    entry = next(item for item in registry["workflows"] if item["id"] == manifest["id"])
    assert entry["path"] == "workflows/AIPUBS-START/003-explore-repository/workflow.yaml"
    assert entry["version"] == manifest["version"]
    assert entry["name"] == manifest["name"]
    assert entry["category"] == manifest["category"]
    assert entry["status"] == "active"


def test_start_003_artifact_schemas_are_valid():
    for name in (
        "repository-map.schema.json",
        "architecture-map.schema.json",
        "execution-map.schema.json",
        "learning-summary.schema.json",
        "start-003-result.schema.json",
    ):
        Draft202012Validator.check_schema(load_schema(name))


def test_sparse_execution_evidence_preserves_candidate_and_unknown_status():
    valid = {
        "schema_version": "owf.execution-map.v1",
        "candidate_entry_points": [{"path": "src/main.py", "basis": "entrypoint naming pattern"}],
        "observed_run_scripts": [],
        "runtime_unknowns": ["Production runtime path not established."],
    }
    assert not validate("execution-map.schema.json", valid)

    invalid = {k: v for k, v in valid.items() if k != "runtime_unknowns"}
    assert validate("execution-map.schema.json", invalid)


def test_incomplete_learning_summary_requires_a_route():
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
    missing_route = {k: v for k, v in valid.items() if k != "recommended_next_workflow"}
    assert validate("learning-summary.schema.json", missing_route)
    invalid_route = {**valid, "recommended_next_workflow": []}
    assert validate("learning-summary.schema.json", invalid_route)


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

    missing_unknowns = {
        **valid,
        "evidence": {"observed": [], "inferred": []},
    }
    assert validate("start-003-result.schema.json", missing_unknowns)

    multiple_routes = {
        **valid,
        "next_workflow": [
            {"id": "AIPUBS-GIT-001", "reason": "Git fundamentals requested."},
            {"id": "AIPUBS-VERIFY-001", "reason": "Testing requested."},
        ],
    }
    assert validate("start-003-result.schema.json", multiple_routes)

    syntactically_valid_but_unknown_route = {
        **valid,
        "next_workflow": {"id": "AIPUBS-DOES-NOT-EXIST", "reason": "Unknown route."},
    }
    assert not validate("start-003-result.schema.json", syntactically_valid_but_unknown_route)


def test_selected_next_workflow_is_registered():
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    registered_ids = {item["id"] for item in registry["workflows"]}
    selected = "AIPUBS-GIT-001"
    assert selected in registered_ids
