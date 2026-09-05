import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "workflows" / "002-repository-explorer"))
from collector import RepositoryCollector


def test_safety_guarantee_read_only():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        sample = root / "sample.py"
        sample.write_text("print('hello world')", encoding="utf-8")
        before = {p: (p.stat().st_mtime_ns, p.stat().st_size) for p in root.iterdir()}
        RepositoryCollector(root).scan().generate_deliverables()
        after = {p: (p.stat().st_mtime_ns, p.stat().st_size) for p in root.iterdir()}
        assert before == after


def test_contract_outputs_exist_and_are_deterministic():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "package.json").write_text(json.dumps({"name": "test-pkg", "scripts": {"start": "node index.js"}}), encoding="utf-8")
        (root / "index.js").write_text("console.log('started');", encoding="utf-8")
        first = RepositoryCollector(root).scan().generate_deliverables()
        second = RepositoryCollector(root).scan().generate_deliverables()
        assert first == second
        for key in ("repository-map", "architecture-map", "execution-map", "learning-summary", "raw_telemetry"):
            assert key in first
        assert "```mermaid" in first["architecture-map"]
        assert "```mermaid" in first["execution-map"]


def test_empty_repository_handling():
    with tempfile.TemporaryDirectory() as tmp:
        deliverables = RepositoryCollector(Path(tmp)).scan().generate_deliverables()
        assert deliverables["raw_telemetry"]["discovery"]["manifests"] == []
        assert deliverables["raw_telemetry"]["tests"]["test_file_count"] == 0
        assert "Flat / Domain-Centric Package" in deliverables["architecture-map"]


def test_monorepo_and_ci_detection():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "pnpm-workspace.yaml").write_text("packages:\n  - 'apps/*'", encoding="utf-8")
        wf_dir = root / ".github" / "workflows"
        wf_dir.mkdir(parents=True)
        (wf_dir / "ci.yml").write_text("name: CI\non: [push]", encoding="utf-8")
        telemetry = RepositoryCollector(root).scan().generate_deliverables()["raw_telemetry"]
        assert "Monorepo" in telemetry["architecture"]["topology"]
        assert telemetry["ci"]["pipelines"] == [{"provider": "GitHub Actions", "file": ".github/workflows/ci.yml"}]


def test_depth_limit_prunes_deeper_directories():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        nested = root / "a" / "b" / "c"
        nested.mkdir(parents=True)
        (nested / "deep.txt").write_text("x", encoding="utf-8")
        files = RepositoryCollector(root, max_depth=1).scan().all_files
        assert files == []
