#!/usr/bin/env python3
"""OWF-002 Repository Explorer.

Deterministic, read-only repository survey collector using only the Python
standard library. The collector deliberately reports evidence rather than
pretending to understand intent or implementation quality.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

WORKFLOW_ID = "OWF-002"
SCHEMA_VERSION = "owf-002.survey.v1"
COLLECTOR_VERSION = "0.1.0"

IGNORED_DIRS: Set[str] = {
    ".git", "node_modules", "vendor", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".turbo", ".cache", "target", ".idea",
    ".vscode", ".tox", "coverage", ".pytest_cache", "bin", "obj",
}

MANIFEST_FILES = {
    "package.json": "Node.js / JavaScript / TypeScript",
    "pyproject.toml": "Python (PEP 517 / Poetry / Flit / PDM)",
    "setup.py": "Python (setuptools)",
    "requirements.txt": "Python (pip)",
    "Pipfile": "Python (Pipenv)",
    "Cargo.toml": "Rust (Cargo)",
    "go.mod": "Go",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java / Kotlin (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "Gemfile": "Ruby (Bundler)",
    "composer.json": "PHP (Composer)",
    "mix.exs": "Elixir (Mix)",
    "Package.swift": "Swift (SPM)",
    "flake.nix": "Nix",
}

ENTRYPOINT_PATTERNS = [
    re.compile(r"^(main|index|app|server|cli)\.(py|js|ts|jsx|tsx|go|rs|rb|php|java|kt|c|cpp)$", re.I),
    re.compile(r"^(src|cmd|app|bin)/(main|index|app|server)\.(py|js|ts|jsx|tsx|go|rs|rb)$", re.I),
]

TEST_CONFIG_FILES = {
    "jest.config.js", "jest.config.ts", "jest.config.json", "vitest.config.ts",
    "vitest.config.js", "pytest.ini", "tox.ini", ".coveragerc", ".rspec",
    "phpunit.xml", "karma.conf.js",
}


def safe_rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def scan_file_tree(root: Path, max_depth: int = 5) -> Dict[str, Any]:
    """Collect a deterministic filesystem inventory without modifying files."""
    extensions: Dict[str, int] = {}
    files: List[Dict[str, Any]] = []
    errors: List[Dict[str, str]] = []

    try:
        top_level = [
            {"name": item.name, "type": "directory" if item.is_dir() else "file"}
            for item in sorted(root.iterdir(), key=lambda p: p.name.lower())
            if item.name not in IGNORED_DIRS
        ]
    except OSError as exc:
        top_level = []
        errors.append({"path": ".", "operation": "list", "error": str(exc)})

    for dirpath, dirnames, filenames in os.walk(root, topdown=True, onerror=lambda e: errors.append({
        "path": str(getattr(e, "filename", "unknown")), "operation": "walk", "error": str(e)
    })):
        dirnames[:] = sorted(d for d in dirnames if d not in IGNORED_DIRS)
        curr = Path(dirpath)
        try:
            depth = len(curr.relative_to(root).parts)
        except ValueError:
            continue
        if depth >= max_depth:
            dirnames[:] = []

        for name in sorted(filenames, key=str.lower):
            path = curr / name
            rel = safe_rel(path, root)
            suffix = path.suffix.lower() or "(no_extension)"
            try:
                size = path.stat().st_size
            except OSError as exc:
                size = None
                errors.append({"path": rel, "operation": "stat", "error": str(exc)})
            extensions[suffix] = extensions.get(suffix, 0) + 1
            files.append({"path": rel, "extension": suffix, "size_bytes": size})

    return {
        "total_files_scanned": len(files),
        "extension_counts": dict(sorted(extensions.items(), key=lambda x: (-x[1], x[0]))[:15]),
        "top_level": top_level,
        "all_files": [item["path"] for item in files],
        "files": files,
        "errors": errors,
    }


def step_1_discover(all_files: List[str]) -> Dict[str, Any]:
    manifests, docs, licenses = [], [], []
    for rel in all_files:
        name = Path(rel).name
        if name in MANIFEST_FILES:
            manifests.append({"file": rel, "ecosystem": MANIFEST_FILES[name]})
        if re.match(r"^(README|CONTRIBUTING|ARCHITECTURE|CHANGELOG|CODE_OF_CONDUCT)(\..+)?$", name, re.I) or rel.lower().startswith("docs/"):
            docs.append(rel)
        if re.match(r"^LICENSE(\..+)?$", name, re.I):
            licenses.append(rel)
    return {"manifests": manifests, "documentation": docs[:50], "licenses": licenses}


def step_2_architecture(root: Path, all_files: List[str]) -> Dict[str, Any]:
    indicators = {
        "pnpm-workspace.yaml": "pnpm Monorepo", "lerna.json": "Lerna Monorepo",
        "nx.json": "Nx Monorepo", "turbo.json": "Turborepo", "go.work": "Go Multi-Module Workspace",
    }
    workspaces = [{"file": rel, "type": indicators[Path(rel).name]} for rel in all_files if Path(rel).name in indicators]
    cargo = root / "Cargo.toml"
    if cargo.exists():
        try:
            if "[workspace]" in cargo.read_text(encoding="utf-8", errors="ignore"):
                workspaces.append({"file": "Cargo.toml", "type": "Cargo Workspace"})
        except OSError:
            pass
    has_packages = any(f.startswith(("packages/", "apps/", "modules/")) for f in all_files)
    has_src = any(f.startswith("src/") for f in all_files)
    pattern = "Monorepo / Multi-Package" if workspaces or has_packages else (
        "Standard Layered / src-centric Monolith or Library" if has_src else "Flat or Domain-Centric Structure"
    )
    return {"structural_pattern_hint": pattern, "workspace_configs": workspaces}


def step_3_execution_path(root: Path, all_files: List[str]) -> Dict[str, Any]:
    entry_points = []
    for rel in all_files:
        if any(p.search(rel) for p in ENTRYPOINT_PATTERNS):
            entry_points.append(rel)
    scripts: Dict[str, Any] = {}
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(encoding="utf-8", errors="ignore"))
            raw = data.get("scripts", {})
            if isinstance(raw, dict):
                scripts["package.json (scripts)"] = {
                    k: v for k, v in raw.items()
                    if k in {"start", "dev", "build", "serve", "run"} or "start" in k or "dev" in k
                }
        except (OSError, json.JSONDecodeError):
            pass
    return {"detected_entry_points": sorted(set(entry_points))[:25], "run_scripts": scripts}


def step_4_tests(all_files: List[str]) -> Dict[str, Any]:
    configs, samples = [], []
    count = 0
    pattern = re.compile(r"(_test|\.test|\.spec|test_)\.[a-zA-Z0-9]+$", re.I)
    for rel in all_files:
        name = Path(rel).name
        if name in TEST_CONFIG_FILES:
            configs.append(rel)
        if pattern.search(name) or "/tests/" in f"/{rel}/" or "/test/" in f"/{rel}/":
            count += 1
            if len(samples) < 10 and not rel.endswith((".pyc", ".json", ".md")):
                samples.append(rel)
    return {"test_configs": configs, "test_files_detected": count, "sample_test_files": samples}


def step_5_ci(all_files: List[str]) -> Dict[str, Any]:
    result = []
    for rel in all_files:
        norm = rel.replace("\\", "/")
        if norm.startswith(".github/workflows/") and norm.endswith((".yml", ".yaml")):
            result.append({"provider": "GitHub Actions", "file": rel})
        elif norm == ".gitlab-ci.yml":
            result.append({"provider": "GitLab CI", "file": rel})
        elif norm.startswith(".circleci/"):
            result.append({"provider": "CircleCI", "file": rel})
        elif norm in {"Jenkinsfile", "azure-pipelines.yml", "bitbucket-pipelines.yml"}:
            result.append({"provider": norm.split(".")[0], "file": rel})
    return {"ci_pipelines": result}


def step_6_deployment(all_files: List[str]) -> Dict[str, Any]:
    infra, envs = [], []
    for rel in all_files:
        name, norm = Path(rel).name, rel.replace("\\", "/")
        if name.startswith("Dockerfile"):
            infra.append({"type": "Docker", "file": rel})
        elif name.startswith("docker-compose") and name.endswith((".yml", ".yaml")):
            infra.append({"type": "Docker Compose", "file": rel})
        elif norm.startswith("helm/") or name == "Chart.yaml":
            infra.append({"type": "Helm / K8s", "file": rel})
        elif norm.startswith(("k8s/", "kubernetes/")):
            infra.append({"type": "Kubernetes Manifest", "file": rel})
        elif name.endswith(".tf") or norm.startswith("terraform/"):
            infra.append({"type": "Terraform", "file": rel})
        elif name in {"fly.toml", "Procfile", "serverless.yml", "render.yaml", "vercel.json", "netlify.toml"}:
            infra.append({"type": "Cloud / PaaS Manifest", "file": rel})
        if name.startswith(".env") and any(x in name for x in ("example", "sample", "template", "dist")):
            envs.append(rel)
    return {"infrastructure_files": infra[:50], "env_templates": envs}


def collect(root: Path, max_depth: int = 5) -> Dict[str, Any]:
    scan = scan_file_tree(root, max_depth=max_depth)
    files = scan["all_files"]
    return {
        "schema_version": SCHEMA_VERSION,
        "scan_metadata": {
            "workflow_id": WORKFLOW_ID,
            "collector_version": COLLECTOR_VERSION,
            "repository_name": root.name,
            "target_path": str(root),
            "total_files": scan["total_files_scanned"],
            "extension_counts": scan["extension_counts"],
            "top_level": scan["top_level"],
            "errors": scan["errors"],
        },
        "step_1_discovery": step_1_discover(files),
        "step_2_architecture": step_2_architecture(root, files),
        "step_3_execution_path": step_3_execution_path(root, files),
        "step_4_tests": step_4_tests(files),
        "step_5_ci": step_5_ci(files),
        "step_6_deployment": step_6_deployment(files),
    }


def format_markdown(data: Dict[str, Any]) -> str:
    meta = data["scan_metadata"]
    lines = [f"# Raw Repository Survey: `{meta['repository_name']}`", f"> Scanned `{meta['total_files']}` files across `{meta['target_path']}`.\n"]
    s1, s2, s3 = data["step_1_discovery"], data["step_2_architecture"], data["step_3_execution_path"]
    s4, s5, s6 = data["step_4_tests"], data["step_5_ci"], data["step_6_deployment"]
    lines += ["## Step 1: Repository Discovery", "### Manifests & Ecosystems"]
    lines += [f"- **{m['file']}** ({m['ecosystem']})" for m in s1["manifests"]] or ["- *No standard package manifests detected.*"]
    lines += ["\n### File Extensions (Top 15)"] + [f"- `{e}`: {n} files" for e, n in meta["extension_counts"].items()]
    lines += ["\n### Documentation & Licenses"] + [f"- Docs: `{x}`" for x in s1["documentation"]] + [f"- License: `{x}`" for x in s1["licenses"]]
    lines += ["\n## Step 2: Architecture & Topology", f"- **Inferred Pattern:** {s2['structural_pattern_hint']}"]
    lines += [f"- Workspace Config: `{x['file']}` ({x['type']})" for x in s2["workspace_configs"]]
    lines += ["\n### Top-Level Layout"] + [f"- `{x['name']}` ({x['type']})" for x in meta["top_level"]]
    lines += ["\n## Step 3: Execution Paths & Entry Points"]
    lines += [f"- Candidate Entry: `{x}`" for x in s3["detected_entry_points"]] or ["- *No explicit standard entry points found.*"]
    for source, cmds in s3["run_scripts"].items():
        lines += [f"\n### {source}"] + [f"- `{k}`: `{v}`" for k, v in cmds.items()]
    lines += ["\n## Step 4: Test Infrastructure", f"- **Detected Test Files:** {s4['test_files_detected']}"]
    lines += [f"- Test Config: `{x}`" for x in s4["test_configs"]] + [f"- Sample Test: `{x}`" for x in s4["sample_test_files"]]
    lines += ["\n## Step 5: Continuous Integration (CI)"] + ([f"- **{x['provider']}**: `{x['file']}`" for x in s5["ci_pipelines"]] or ["- *No standard CI configuration files located.*"])
    lines += ["\n## Step 6: Deployment & Infrastructure"] + ([f"- `{x['file']}` ({x['type']})" for x in s6["infrastructure_files"]] or ["- *No standard deployment manifests detected.*"])
    lines += ["\n### Environment Configuration Templates"] + [f"- `{x}`" for x in s6["env_templates"]] if s6["env_templates"] else lines
    if meta["errors"]:
        lines += ["\n## Collection Warnings", f"- {len(meta['errors'])} filesystem operations produced errors. See JSON for details."]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="OWF-002: deterministic read-only repository survey")
    parser.add_argument("target", nargs="?", default=".")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    parser.add_argument("--output", "-o")
    parser.add_argument("--max-depth", type=int, default=5)
    args = parser.parse_args()
    root = Path(args.target).resolve()
    if not root.exists() or not root.is_dir():
        print(f"Error: Target '{root}' is not a valid directory.", file=sys.stderr)
        return 1
    payload = collect(root, max_depth=max(0, args.max_depth))
    output = json.dumps(payload, indent=2, sort_keys=True) if args.format == "json" else format_markdown(payload)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
        print(f"Data collected successfully and written to {args.output}")
    else:
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
