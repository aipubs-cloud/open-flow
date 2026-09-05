#!/usr/bin/env python3
"""OWF-002 deterministic, read-only repository evidence collector.

Uses only the Python standard library. Repository scanning and synthesis do not
execute application code, invoke network services, or modify the scanned tree.
Artifact emission is an explicit output operation and should target a dedicated
artifact directory rather than the repository under inspection.
"""

import argparse
import json
import os
from pathlib import Path
import re
from typing import Any, Dict, List, Set

IGNORED_DIRS: Set[str] = {
    ".git", "node_modules", "vendor", "__pycache__", ".venv", "venv",
    "dist", "build", ".next", ".turbo", ".cache", "target", ".idea",
    ".vscode", ".tox", "coverage", ".pytest_cache", "bin", "obj"
}

MANIFEST_SPECS = {
    "package.json": "JavaScript / TypeScript (npm/yarn/pnpm)",
    "pyproject.toml": "Python (PEP 517 / Poetry / Flit / PDM)",
    "setup.py": "Python (setuptools)",
    "requirements.txt": "Python (pip)",
    "Cargo.toml": "Rust (Cargo)",
    "go.mod": "Go Modules",
    "pom.xml": "Java (Maven)",
    "build.gradle": "Java / Kotlin (Gradle)",
    "build.gradle.kts": "Kotlin (Gradle)",
    "Gemfile": "Ruby (Bundler)",
    "composer.json": "PHP (Composer)",
    "mix.exs": "Elixir (Mix)",
}

ENTRYPOINT_REGEX = re.compile(
    r"^(main|index|app|server|cli|mod)\.(py|js|ts|jsx|tsx|go|rs|rb|php|java|kt|c|cpp)$|"
    r"^(src|cmd|app|bin)/(main|index|app|server)\.(py|js|ts|jsx|tsx|go|rs|rb)$",
    re.IGNORECASE,
)


class RepositoryCollector:
    def __init__(self, root: Path, max_depth: int = 5):
        self.root = root.resolve()
        if max_depth < 0:
            raise ValueError("max_depth must be >= 0")
        self.max_depth = max_depth
        self.all_files: List[str] = []
        self.top_level: List[Dict[str, str]] = []
        self.ext_counts: Dict[str, int] = {}
        self.total_size_bytes = 0

    def scan(self) -> "RepositoryCollector":
        """Walk deterministically without following symlinks or entering ignored directories."""
        if not self.root.is_dir():
            raise NotADirectoryError(str(self.root))

        for item in sorted(self.root.iterdir(), key=lambda p: p.name.casefold()):
            if item.name not in IGNORED_DIRS:
                self.top_level.append({
                    "name": item.name,
                    "type": "directory" if item.is_dir() else "file",
                })

        for dirpath, dirnames, filenames in os.walk(self.root, followlinks=False):
            curr = Path(dirpath)
            depth = len(curr.relative_to(self.root).parts)
            dirnames[:] = sorted(
                (d for d in dirnames if d not in IGNORED_DIRS),
                key=str.casefold,
            )
            if depth >= self.max_depth:
                dirnames[:] = []

            for f in sorted(filenames, key=str.casefold):
                fpath = curr / f
                rel = fpath.relative_to(self.root).as_posix()
                self.all_files.append(rel)
                try:
                    self.total_size_bytes += fpath.stat().st_size
                except OSError:
                    pass
                ext = fpath.suffix.lower() or "(no_ext)"
                self.ext_counts[ext] = self.ext_counts.get(ext, 0) + 1

        return self

    def step_1_discovery(self) -> Dict[str, Any]:
        manifests, docs, licenses = [], [], []
        for f in self.all_files:
            base = os.path.basename(f)
            if base in MANIFEST_SPECS:
                manifests.append({"file": f, "ecosystem": MANIFEST_SPECS[base]})
            if re.match(r"^(README|CONTRIBUTING|ARCHITECTURE|CHANGELOG)(\..+)?$", base, re.I) or f.startswith("docs/"):
                docs.append(f)
            if re.match(r"^LICENSE(\..+)?$", base, re.I):
                licenses.append(f)
        return {
            "manifests": manifests,
            "documentation": sorted(docs)[:15],
            "licenses": sorted(licenses),
            "languages": sorted(self.ext_counts.items(), key=lambda x: (-x[1], x[0]))[:10],
        }

    def step_2_architecture(self) -> Dict[str, Any]:
        workspaces = []
        ws_indicators = {
            "pnpm-workspace.yaml": "pnpm Workspace",
            "lerna.json": "Lerna Monorepo",
            "nx.json": "Nx Monorepo",
            "turbo.json": "Turborepo",
            "go.work": "Go Multi-Module",
        }
        for f in self.all_files:
            b = os.path.basename(f)
            if b in ws_indicators:
                workspaces.append({"file": f, "type": ws_indicators[b]})

        cargo_path = self.root / "Cargo.toml"
        if cargo_path.exists() and cargo_path.is_file():
            try:
                if "[workspace]" in cargo_path.read_text(encoding="utf-8", errors="ignore"):
                    workspaces.append({"file": "Cargo.toml", "type": "Cargo Workspace"})
            except OSError:
                pass

        has_packages = any(f.startswith(("packages/", "apps/", "services/", "modules/")) for f in self.all_files)
        has_src = any(f.startswith("src/") for f in self.all_files)
        if workspaces or has_packages:
            pattern = "Monorepo / Multi-Package Structure"
        elif has_src:
            pattern = "Layered Monolith / Standard Library (src/ layout)"
        else:
            pattern = "Flat / Domain-Centric Package"
        return {
            "topology": pattern,
            "workspaces": workspaces,
            "top_level_directories": [i["name"] for i in self.top_level if i["type"] == "directory"],
        }

    def step_3_execution_paths(self) -> Dict[str, Any]:
        entrypoints = [f for f in self.all_files if ENTRYPOINT_REGEX.match(f)]
        scripts: Dict[str, Dict[str, str]] = {}
        pkg_json = self.root / "package.json"
        if pkg_json.exists() and pkg_json.is_file():
            try:
                data = json.loads(pkg_json.read_text(encoding="utf-8", errors="ignore"))
                if isinstance(data.get("scripts"), dict):
                    scripts["npm_scripts"] = {
                        k: str(v) for k, v in data["scripts"].items()
                        if k in {"start", "dev", "build", "serve", "run"} or "start" in k or "dev" in k
                    }
            except (OSError, ValueError, TypeError):
                pass
        return {"entrypoint_candidates": sorted(entrypoints)[:15], "manifest_scripts": scripts}

    def step_4_tests(self) -> Dict[str, Any]:
        configs, test_files = [], []
        known_test_configs = {
            "jest.config.js", "jest.config.ts", "vitest.config.ts", "pytest.ini",
            "tox.ini", ".rspec", "phpunit.xml",
        }
        test_file_pattern = re.compile(r"(_test|\.test|\.spec|test_)\.[a-zA-Z0-9]+$", re.I)
        for f in self.all_files:
            b = os.path.basename(f)
            if b in known_test_configs:
                configs.append(f)
            if (test_file_pattern.search(b) or "/test/" in f"/{f}/" or "/tests/" in f"/{f}/") and not f.endswith((".md", ".json", ".pyc")):
                test_files.append(f)
        return {"test_configs": sorted(configs), "test_file_count": len(test_files), "sample_test_files": sorted(test_files)[:8]}

    def step_5_ci(self) -> Dict[str, Any]:
        ci_pipes = []
        for f in self.all_files:
            if f.startswith(".github/workflows/") and f.endswith((".yml", ".yaml")):
                ci_pipes.append({"provider": "GitHub Actions", "file": f})
            elif f == ".gitlab-ci.yml":
                ci_pipes.append({"provider": "GitLab CI", "file": f})
            elif f.startswith(".circleci/"):
                ci_pipes.append({"provider": "CircleCI", "file": f})
            elif f == "Jenkinsfile":
                ci_pipes.append({"provider": "Jenkins", "file": f})
            elif f == "azure-pipelines.yml":
                ci_pipes.append({"provider": "Azure Pipelines", "file": f})
        return {"pipelines": ci_pipes}

    def step_6_deployment(self) -> Dict[str, Any]:
        infra, envs = [], []
        for f in self.all_files:
            b = os.path.basename(f)
            if b.startswith("Dockerfile"):
                infra.append({"type": "Docker", "file": f})
            elif b.startswith("docker-compose") and b.endswith((".yml", ".yaml")):
                infra.append({"type": "Docker Compose", "file": f})
            elif f.startswith(("k8s/", "helm/", "terraform/")) or f.endswith(".tf"):
                infra.append({"type": "IaC / Orchestration", "file": f})
            elif b in {"fly.toml", "Procfile", "serverless.yml", "vercel.json"}:
                infra.append({"type": "PaaS Spec", "file": f})
            if b.startswith(".env") and any(k in b.lower() for k in ("example", "sample", "template", "dist")):
                envs.append(f)
        return {"infrastructure": infra, "environment_templates": sorted(envs)}

    def generate_deliverables(self) -> Dict[str, Any]:
        s1, s2 = self.step_1_discovery(), self.step_2_architecture()
        s3, s4 = self.step_3_execution_paths(), self.step_4_tests()
        s5, s6 = self.step_5_ci(), self.step_6_deployment()

        repo_map = [f"# Repository Map: {self.root.name}", "", f"- **Root Path:** `{self.root}`", f"- **Files Scanned:** {len(self.all_files)}", f"- **Total File Size:** {self.total_size_bytes / 1024:.1f} KB", "", "### Directory Layout"]
        repo_map.extend(f"- `{item['name']}` ({item['type']})" for item in self.top_level)

        arch_map = ["```mermaid", "graph TD", f'    Root["{self.root.name} ({s2["topology"]})"]']
        for d in s2["top_level_directories"][:6]:
            node_id = re.sub(r"[^a-zA-Z0-9]", "_", d) or "Directory"
            arch_map.append(f'    Root --> {node_id}["{d}"]')
        if s6["infrastructure"]:
            arch_map.append('    Root --> Infra["Infrastructure / Deploy"]')
        if s4["test_file_count"] > 0:
            arch_map.append('    Root --> Tests["Test Suites"]')
        arch_map.append("```")

        exec_map = ["```mermaid", "flowchart TD", "    Dev[Developer / User]"]
        if s3["entrypoint_candidates"]:
            ep = s3["entrypoint_candidates"][0].replace('"', "'")
            exec_map.extend([f'    Entry["Entrypoint candidate: {ep}"]', "    Dev --> Entry"])
        else:
            exec_map.extend(["    App[Application / Library entrypoint not deterministically identified]", "    Dev --> App"])
        exec_map.append("```")

        summary = [f"# Learning Summary: {self.root.name}", "", f"**Structural Architecture:** {s2['topology']}", "", "### Observed Facts"]
        if s1["manifests"]:
            summary.append(f"- **Primary Ecosystem Evidence:** {s1['manifests'][0]['ecosystem']} (`{s1['manifests'][0]['file']}`)")
        summary.extend([
            f"- **Test Suite:** {s4['test_file_count']} test files detected across {len(s4['test_configs'])} config files.",
            f"- **CI/CD:** {len(s5['pipelines'])} pipeline definitions found.",
            f"- **Deployment:** {len(s6['infrastructure'])} infrastructure manifest(s) present.",
            "", "### Quickstart Commands (Observed)",
        ])
        if s3["manifest_scripts"]:
            for name, val in s3["manifest_scripts"].get("npm_scripts", {}).items():
                summary.append(f"- `npm run {name}`: `{val}`")
        else:
            summary.append("- No supported package-manager run scripts were deterministically observed.")

        return {
            "repository-map": "\n".join(repo_map),
            "architecture-map": "\n".join(arch_map),
            "execution-map": "\n".join(exec_map),
            "learning-summary": "\n".join(summary),
            "raw_telemetry": {"discovery": s1, "architecture": s2, "execution": s3, "tests": s4, "ci": s5, "deployment": s6},
        }


def main() -> None:
    parser = argparse.ArgumentParser(description="OWF-002 deterministic repository collector")
    parser.add_argument("path", nargs="?", default=".", help="Repository root path")
    parser.add_argument("--max-depth", type=int, default=5, help="Scan depth limit")
    parser.add_argument("--format", choices=["markdown", "json"], default="markdown")
    parser.add_argument("--output-dir", type=str, default=None, help="Explicit artifact output directory")
    args = parser.parse_args()

    collector = RepositoryCollector(Path(args.path), max_depth=args.max_depth)
    deliverables = collector.scan().generate_deliverables()
    if args.output_dir:
        out = Path(args.output_dir).resolve()
        out.mkdir(parents=True, exist_ok=True)
        for name in ("repository-map", "architecture-map", "execution-map", "learning-summary"):
            (out / f"{name}.md").write_text(deliverables[name], encoding="utf-8")
        print(f"Artifacts successfully written to {out}")
        return
    if args.format == "json":
        print(json.dumps(deliverables, indent=2))
    else:
        print(deliverables["learning-summary"])
        print("\n" + deliverables["architecture-map"])
        print("\n" + deliverables["execution-map"])


if __name__ == "__main__":
    main()
