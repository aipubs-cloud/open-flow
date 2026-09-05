from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / "workflows"
REQUIRED = {"id", "name", "version", "purpose", "steps"}
MODES = {"observe", "plan", "guided", "assisted", "autonomous"}


def manifests():
    return sorted(WORKFLOWS.glob("*/workflow.yaml"))


def test_ten_workflows_exist():
    assert len(manifests()) == 10


def test_workflow_manifests_are_valid():
    ids = []
    for path in manifests():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), path
        missing = REQUIRED - data.keys()
        assert not missing, f"{path}: missing {sorted(missing)}"
        assert data["id"].startswith("OWF-")
        assert data["mode"] in MODES if "mode" in data else True
        assert isinstance(data["steps"], list) and data["steps"]
        ids.append(data["id"])
    assert len(ids) == len(set(ids))
    assert set(ids) == {f"OWF-{i:03d}" for i in range(1, 11)}


def test_manifest_paths_match_directories():
    for path in manifests():
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        assert data["id"] in path.read_text(encoding="utf-8")
