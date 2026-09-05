import json
from pathlib import Path

from owf002.repo_explorer import collect, format_markdown


def make_repo(tmp_path: Path) -> Path:
    (tmp_path / "src").mkdir()
    (tmp_path / "tests").mkdir()
    (tmp_path / ".git").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('ok')\n", encoding="utf-8")
    (tmp_path / "tests" / "test_main.py").write_text("def test_ok(): assert True\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]\nname='demo'\n", encoding="utf-8")
    (tmp_path / ".github").mkdir()
    (tmp_path / ".github" / "workflows").mkdir()
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
    return tmp_path


def test_collect_is_deterministic_and_ignores_noise(tmp_path):
    root = make_repo(tmp_path)
    first = collect(root)
    second = collect(root)
    assert first == second
    assert all(".git/" not in p for p in [x["path"] for x in []])
    assert ".git" not in [x["name"] for x in first["scan_metadata"]["top_level"]]
    assert first["scan_metadata"]["total_files"] == 5


def test_expected_steps_are_populated(tmp_path):
    data = collect(make_repo(tmp_path))
    assert data["schema_version"] == "owf-002.survey.v1"
    assert data["step_1_discovery"]["manifests"][0]["file"] == "pyproject.toml"
    assert "src/main.py" in data["step_3_execution_path"]["detected_entry_points"]
    assert data["step_4_tests"]["test_files_detected"] == 1
    assert data["step_5_ci"]["ci_pipelines"][0]["provider"] == "GitHub Actions"


def test_markdown_and_json_contracts(tmp_path):
    data = collect(make_repo(tmp_path))
    markdown = format_markdown(data)
    encoded = json.dumps(data, sort_keys=True)
    assert "# Raw Repository Survey:" in markdown
    assert "Step 6: Deployment & Infrastructure" in markdown
    assert '"schema_version": "owf-002.survey.v1"' in encoded
