import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(schema_name, instance):
    schema = load_json(SCHEMAS / schema_name)
    return list(Draft202012Validator(schema).iter_errors(instance))


def test_all_public_schemas_are_valid_draft_2020_12_schemas():
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)


def test_workflow_schema_accepts_canonical_example():
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    errors = validate("workflow.schema.json", document)
    assert not errors, "\n".join(error.message for error in errors)


def test_workflow_schema_rejects_conflicting_mode_forms():
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    document["mode"] = "autonomous"
    assert validate("workflow.schema.json", document)


def test_workflow_schema_rejects_malformed_structured_io():
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    document["inputs"] = [{"name": "repository"}]
    assert validate("workflow.schema.json", document)


def test_result_schema_has_stable_status_contract():
    valid = {
        "workflow_id": "OWF-002",
        "workflow_version": "0.1.0",
        "status": "success",
        "mode": "observe",
        "evidence": [{"kind": "FACT", "statement": "README.md exists."}],
        "verification": {"performed": True, "checks": ["filesystem scan completed"]},
    }
    assert not validate("result.schema.json", valid)


def test_result_schema_rejects_unknown_status():
    invalid = {
        "workflow_id": "OWF-002",
        "workflow_version": "0.1.0",
        "status": "complete",
        "mode": "observe",
        "evidence": [],
        "verification": {"performed": False, "checks": []},
    }
    assert validate("result.schema.json", invalid)


def test_agent_schema_positive_and_negative():
    valid = {"name": "owf-architect", "description": "Architecture agent.", "role": "architect", "safety": {"read_only_initially": True, "secret_policy": "Never expose secrets."}}
    invalid = {**valid, "safety": {"read_only_initially": "yes", "secret_policy": "Never expose secrets."}}
    assert not validate("agent.schema.json", valid)
    assert validate("agent.schema.json", invalid)


def test_skill_schema_positive_and_negative():
    valid = {"name": "repository-discovery", "description": "Discover repository structure.", "procedure": ["Inspect repository."], "verification": ["Record observed paths."]}
    invalid = {**valid, "procedure": []}
    assert not validate("skill.schema.json", valid)
    assert validate("skill.schema.json", invalid)


def test_hook_schema_positive_and_negative():
    valid = {"name": "pre-tool-gate", "event": "pre-command", "purpose": "Gate consequential commands.", "failure_policy": "fail-closed", "side_effects": False}
    invalid = {**valid, "event": "unknown"}
    assert not validate("hook.schema.json", valid)
    assert validate("hook.schema.json", invalid)


def test_policy_schema_positive_and_negative_cross_field_contract():
    valid = {"version": "1.0.0", "default_mode": "observe", "allowed_modes": ["observe", "plan"], "capabilities": {"filesystem_read": True}, "destructive_operations": False, "secret_policy": "Never expose secrets."}
    invalid = {**valid, "allowed_modes": ["plan"]}
    assert not validate("policy.schema.json", valid)
    assert validate("policy.schema.json", invalid)


def test_registry_schema_positive_and_negative_cross_field_contract():
    valid = {"name": "OWF", "version": "0.1.0", "spec": "1.0", "description": "Workflow registry.", "modes": ["observe", "plan"], "defaults": {"mode": "observe", "require_tests": True, "require_review": True, "destructive_operations": False}, "workflows": [{"id": "OWF-002", "name": "Repository Explorer", "path": "workflows/002-repository-explorer/workflow.yaml"}]}
    invalid_mode = {**valid, "modes": ["plan"]}
    invalid_extra = {**valid, "defaults": {**valid["defaults"], "unexpected": True}}
    assert not validate("registry.schema.json", valid)
    assert validate("registry.schema.json", invalid_mode)
    assert validate("registry.schema.json", invalid_extra)


def test_survey_schema_positive_and_negative():
    valid = {"schema_version": "owf-002.survey.v1", "scan_metadata": {"workflow_id": "OWF-002", "collector_version": "0.1.0", "repository_name": "open-flow", "target_path": ".", "total_files": 0, "extension_counts": {}, "top_level": [], "errors": []}, "step_1_discovery": {}, "step_2_architecture": {}, "step_3_execution_path": {}, "step_4_tests": {}, "step_5_ci": {}, "step_6_deployment": {}}
    invalid = {**valid, "schema_version": "wrong"}
    assert not validate("owf-002-survey.schema.json", valid)
    assert validate("owf-002-survey.schema.json", invalid)
