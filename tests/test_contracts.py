import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from core.registry import validate_registry

ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(schema_name, instance):
    schema = load_json(SCHEMAS / schema_name)
    return list(Draft202012Validator(schema).iter_errors(instance))


def test_all_public_schemas_are_valid_draft_2020_12_schemas():
    for path in sorted(SCHEMAS.glob("*.schema.json")):
        Draft202012Validator.check_schema(load_json(path))


def test_workflow_schema_accepts_canonical_example():
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    assert not validate("workflow.schema.json", document)


def test_workflow_schema_rejects_conflicting_mode_forms():
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    document["mode"] = "autonomous"
    assert validate("workflow.schema.json", document)


def test_workflow_schema_rejects_malformed_structured_io():
    document = yaml.safe_load((ROOT / "examples" / "workflow.yaml").read_text(encoding="utf-8"))
    document["inputs"] = [{"name": "repository"}]
    assert validate("workflow.schema.json", document)


def test_result_schema_has_stable_status_contract():
    valid = {"workflow_id": "OWF-002", "workflow_version": "0.1.0", "status": "success", "mode": "observe", "evidence": [{"kind": "FACT", "statement": "README.md exists."}], "verification": {"performed": True, "checks": ["filesystem scan completed"]}}
    assert not validate("result.schema.json", valid)


def test_result_schema_rejects_unknown_status():
    invalid = {"workflow_id": "OWF-002", "workflow_version": "0.1.0", "status": "complete", "mode": "observe", "evidence": [], "verification": {"performed": False, "checks": []}}
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


def test_registry_schema_positive_and_negative():
    valid = {"registry": {"name": "AIPubs Open Flow Workflow Registry", "version": "1.0.0", "schema": "schemas/registry.schema.json", "manifest_root": "workflows", "discovery": "filesystem", "lifecycle": {"experimental": "usable_not_stable", "active": "stable_discoverable", "deprecated": "resolvable_prefer_replacement", "retired": "blocked_without_migration_exception"}}, "workflows": [{"id": "AIPUBS-START-001", "name": "What Is GitHub?", "path": "workflows/AIPUBS-START/001-what-is-github/workflow.yaml", "version": "0.1.1", "category": "start", "status": "active"}]}
    assert not validate("registry.schema.json", valid)
    invalid_id = {**valid, "workflows": [{**valid["workflows"][0], "id": "bad-id"}]}
    assert validate("registry.schema.json", invalid_id)
    invalid_extra = {**valid, "workflows": [{**valid["workflows"][0], "unexpected": True}]}
    assert validate("registry.schema.json", invalid_extra)


def test_registry_semantic_validation_is_clean_on_canonical_registry():
    assert not validate_registry()


def test_registry_schema_rejects_unknown_top_level_fields():
    registry = yaml.safe_load((ROOT / "registry" / "workflows.yaml").read_text(encoding="utf-8"))
    registry["unexpected"] = True
    assert validate("registry.schema.json", registry)


def test_registry_semantics_detect_registry_manifest_drift(tmp_path):
    registry = yaml.safe_load((ROOT / "registry" / "workflows.yaml").read_text(encoding="utf-8"))
    registry["workflows"] = [registry["workflows"][0]]
    registry_path = tmp_path / "workflows.yaml"
    registry_path.write_text(yaml.safe_dump(registry), encoding="utf-8")
    errors = validate_registry(registry_path=registry_path, workflow_root=ROOT / "workflows")
    assert any(error.code == "MANIFEST_ORPHAN" for error in errors)


def test_survey_schema_positive_and_negative():
    valid = {"schema_version": "owf-002.survey.v1", "scan_metadata": {"workflow_id": "OWF-002", "collector_version": "0.1.0", "repository_name": "open-flow", "target_path": ".", "total_files": 0, "extension_counts": {}, "top_level": [], "errors": []}, "step_1_discovery": {}, "step_2_architecture": {}, "step_3_execution_path": {}, "step_4_tests": {}, "step_5_ci": {}, "step_6_deployment": {}}
    invalid = {**valid, "schema_version": "wrong"}
    assert not validate("owf-002-survey.schema.json", valid)
    assert validate("owf-002-survey.schema.json", invalid)
