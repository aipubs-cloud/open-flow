import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "workflows"
SCHEMA = ROOT / "schemas" / "workflow.schema.json"
REQUIRED = {"id", "name", "version", "purpose", "steps"}
MODES = {"observe", "plan", "guided", "assisted", "autonomous"}


def manifests():
    return sorted(WORKFLOWS.glob("*/workflow.yaml"))


def test_ten_workflows_exist():
    assert len(manifests()) == 10


def test_workflow_manifests_are_valid():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    ids = []
    for path in manifests():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), path
        missing = REQUIRED - data.keys()
        assert not missing, f"{path}: missing {sorted(missing)}"
        assert data["id"].startswith("OWF-")
        declared_modes = data.get("modes")
        declared_mode = data.get("mode")
        assert (declared_mode is not None) ^ (declared_modes is not None), f"{path}: declare exactly one of mode or modes"
        if declared_mode is not None:
            assert declared_mode in MODES
        else:
            assert declared_modes and set(declared_modes) <= MODES
        assert isinstance(data["steps"], list) and data["steps"]
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        assert not errors, f"{path}: " + "; ".join(error.message for error in errors)
        ids.append(data["id"])
    assert len(ids) == len(set(ids))
    assert set(ids) == {f"OWF-{i:03d}" for i in range(1, 11)}


def test_manifest_paths_match_directories():
    for path in manifests():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["id"] in path.read_text(encoding="utf-8")
