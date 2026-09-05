import json
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

from core.registry import discover_manifests, validate_registry

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "workflow.schema.json"
REQUIRED = {"id", "name", "version", "steps"}
MODES = {"observe", "plan", "guided", "assisted", "autonomous"}


def manifests():
    return discover_manifests()


def test_workflow_manifests_are_discovered_recursively():
    paths = manifests()
    assert paths
    assert any("AIPUBS-START" in str(path) for path in paths)
    assert any("011-workflow-composer" in str(path) for path in paths)


def test_workflow_manifests_are_valid():
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    ids = []
    for path in manifests():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), path
        missing = REQUIRED - data.keys()
        assert not missing, f"{path}: missing {sorted(missing)}"
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


def test_canonical_registry_is_integrity_clean():
    errors = validate_registry()
    assert not errors, "\n".join(str(error) for error in errors)
