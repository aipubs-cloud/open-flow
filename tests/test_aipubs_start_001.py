from pathlib import Path
import sys

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "workflows" / "AIPUBS-START" / "001-what-is-github"))

from inspect_primitives import inspect_primitives


def test_empty_directory_is_non_destructive(tmp_path):
    result = inspect_primitives(tmp_path)
    assert result["repository"]["is_git_repository"] is False
    assert result["remote_github"]["status"] == "UNKNOWN"
    assert result["github_actions"]["workflow_files"] == []


def test_fixture_git_repository(tmp_path):
    import subprocess

    subprocess.run(["git", "init"], cwd=tmp_path, check=True, capture_output=True)
    (tmp_path / "README.md").write_text("# fixture\n", encoding="utf-8")
    subprocess.run(["git", "add", "README.md"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "initial"], cwd=tmp_path, check=True, capture_output=True)
    result = inspect_primitives(tmp_path)
    assert result["repository"]["is_git_repository"] is True
    assert result["branch"]["status"] == "OBSERVED FACT"
    assert result["history"]["status"] == "OBSERVED FACT"


def test_actions_and_deployment_are_evidence_based(tmp_path):
    (tmp_path / ".github" / "workflows").mkdir(parents=True)
    (tmp_path / ".github" / "workflows" / "ci.yml").write_text("name: CI\n", encoding="utf-8")
    (tmp_path / "Dockerfile").write_text("FROM scratch\n", encoding="utf-8")
    result = inspect_primitives(tmp_path)
    assert result["github_actions"]["status"] == "OBSERVED FACT"
    assert result["github_actions"]["workflow_files"] == [".github/workflows/ci.yml"]
    assert result["deployment"]["status"] == "OBSERVED FACT"
    assert result["deployment"]["hints"] == ["Dockerfile"]
