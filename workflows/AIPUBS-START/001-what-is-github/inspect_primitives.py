"""Safe, deterministic repository observation for AIPUBS-START-001."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def git(root: Path, *args: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", *args], cwd=root, text=True, capture_output=True, check=False
        )
    except OSError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def inspect_primitives(root: Path) -> dict:
    root = root.resolve()
    is_git = (root / ".git").exists() or git(root, "rev-parse", "--show-toplevel") is not None
    evidence = {
        "repository": {"status": "OBSERVED FACT", "is_git_repository": is_git},
        "remote_github": {"status": "UNKNOWN"},
        "branch": {"status": "UNKNOWN"},
        "history": {"status": "UNKNOWN"},
        "github_actions": {"status": "UNKNOWN", "workflow_files": []},
        "tests": {"status": "UNKNOWN", "hints": []},
        "deployment": {"status": "UNKNOWN", "hints": []},
    }
    if not is_git:
        return evidence

    remote = git(root, "config", "--get", "remote.origin.url")
    if remote:
        evidence["remote_github"] = {
            "status": "OBSERVED FACT",
            "url": remote,
            "is_github": "github.com" in remote.lower(),
        }
    branch = git(root, "branch", "--show-current")
    if branch:
        evidence["branch"] = {"status": "OBSERVED FACT", "current_branch": branch}
    latest = git(root, "log", "-1", "--format=%h - %s")
    if latest:
        evidence["history"] = {"status": "OBSERVED FACT", "latest_commit": latest}

    actions = sorted(str(p.relative_to(root)) for p in (root / ".github" / "workflows").glob("*.y*ml")) if (root / ".github" / "workflows").exists() else []
    if actions:
        evidence["github_actions"] = {"status": "OBSERVED FACT", "workflow_files": actions}
    else:
        evidence["github_actions"] = {"status": "UNKNOWN", "workflow_files": []}

    test_names = {"tests", "test", "spec", "__tests__"}
    test_hints = sorted(p.name for p in root.iterdir() if p.is_dir() and p.name.lower() in test_names)
    if test_hints:
        evidence["tests"] = {"status": "OBSERVED FACT", "hints": test_hints}

    deploy_names = {"Dockerfile", "docker-compose.yml", "Procfile", "fly.toml", "vercel.json", "wrangler.toml"}
    deploy_hints = sorted(p.name for p in root.iterdir() if p.name in deploy_names)
    if deploy_hints:
        evidence["deployment"] = {"status": "OBSERVED FACT", "hints": deploy_hints}
    return evidence


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    print(json.dumps(inspect_primitives(target), indent=2))
