from pathlib import Path
from typing import Dict, List

import yaml

from core.registry import validate_registry


def write_manifest(root: Path, workflow_id: str = "OWF-001", version: str = "0.1.0") -> None:
    path = root / "workflows" / workflow_id
    path.mkdir(parents=True)
    (path / "workflow.yaml").write_text(
        yaml.safe_dump({
            "id": workflow_id,
            "name": "Fixture",
            "version": version,
            "category": "fixture",
            "mode": "observe",
            "steps": ["inspect"],
        }),
        encoding="utf-8",
    )


def write_registry(root: Path, entries: List[Dict]) -> Path:
    path = root / "registry.yaml"
    path.write_text(yaml.safe_dump({"workflows": entries}), encoding="utf-8")
    return path


def base_entry(workflow_id="OWF-001"):
    return {
        "id": workflow_id,
        "name": "Fixture",
        "path": f"workflows/{workflow_id}/workflow.yaml",
        "version": "0.1.0",
        "category": "fixture",
        "status": "active",
    }


def test_duplicate_registry_ids(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    registry = write_registry(tmp_path, [base_entry(), base_entry()])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "DUPLICATE_REGISTRY_ID" for error in errors)


def test_missing_reference(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    manifest = tmp_path / "workflows" / "OWF-001" / "workflow.yaml"
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    data["next_workflow"] = "OWF-999"
    manifest.write_text(yaml.safe_dump(data), encoding="utf-8")
    registry = write_registry(tmp_path, [base_entry()])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "UNKNOWN_REFERENCE" for error in errors)


def test_orphaned_registry_entry(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    entry = base_entry()
    entry["id"] = "OWF-002"
    entry["path"] = "workflows/OWF-002/workflow.yaml"
    registry = write_registry(tmp_path, [entry])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "MISSING_MANIFEST" for error in errors)
    assert any(error.code == "MANIFEST_ORPHAN" for error in errors)


def test_invalid_version(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    entry = base_entry()
    entry["version"] = "not-semver"
    registry = write_registry(tmp_path, [entry])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "INVALID_VERSION" for error in errors)
    assert any(error.code == "METADATA_DRIFT" for error in errors)


def test_invalid_status(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    entry = base_entry()
    entry["status"] = "preview"
    registry = write_registry(tmp_path, [entry])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "INVALID_STATUS" for error in errors)


def test_invalid_path(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    entry = base_entry()
    entry["path"] = "/tmp/workflow.yaml"
    registry = write_registry(tmp_path, [entry])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "INVALID_PATH" for error in errors)


def test_retired_reference_requires_explicit_exception(tmp_path):
    write_manifest(tmp_path, "OWF-001")
    data = yaml.safe_load((tmp_path / "workflows/OWF-001/workflow.yaml").read_text())
    data["next_workflow"] = "OWF-002"
    (tmp_path / "workflows/OWF-001/workflow.yaml").write_text(yaml.safe_dump(data))
    retired = base_entry("OWF-002")
    retired["name"] = "Fixture Two"
    retired["path"] = "workflows/OWF-002/workflow.yaml"
    (tmp_path / "workflows/OWF-002").mkdir()
    (tmp_path / "workflows/OWF-002/workflow.yaml").write_text(yaml.safe_dump({
        "id": "OWF-002", "name": "Fixture Two", "version": "0.1.0", "category": "fixture", "mode": "observe", "steps": ["inspect"]
    }))
    retired["status"] = "retired"
    registry = write_registry(tmp_path, [base_entry(), retired])
    errors = validate_registry(registry, tmp_path / "workflows")
    assert any(error.code == "RETIRED_REFERENCE" for error in errors)
