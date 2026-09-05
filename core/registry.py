"""Canonical workflow registry validation and discovery."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Iterable

import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "workflows.yaml"
WORKFLOW_ROOT = ROOT / "workflows"
SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
WORKFLOW_ID = re.compile(r"^(?:OWF-[0-9]{3}|AIPUBS-[A-Z0-9]+-[0-9]{3})$")
STATUSES = {"experimental", "active", "deprecated", "retired"}


@dataclass(frozen=True)
class RegistryError:
    code: str
    message: str

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"


def discover_manifests(root: Path = WORKFLOW_ROOT) -> list[Path]:
    """Discover manifests from the filesystem, never from an inventory list."""
    return sorted(root.rglob("workflow.yaml"))


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def _references(value: Any) -> Iterable[str]:
    """Extract workflow IDs from common reference-bearing manifest structures."""
    if isinstance(value, str):
        if WORKFLOW_ID.fullmatch(value):
            yield value
        return
    if isinstance(value, list):
        for item in value:
            yield from _references(item)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"workflow", "workflow_id", "next_workflow", "replacement"}:
                yield from _references(item)
            elif key in {"composition", "pipeline", "bindings", "missions", "prerequisites"}:
                yield from _references(item)
            elif isinstance(item, (dict, list)):
                yield from _references(item)


def validate_registry(registry_path: Path = REGISTRY_PATH, workflow_root: Path = WORKFLOW_ROOT) -> list[RegistryError]:
    errors: list[RegistryError] = []
    registry = _load_yaml(registry_path)
    entries = registry.get("workflows", [])
    if not isinstance(entries, list):
        return [RegistryError("REGISTRY_FORMAT", "workflows must be a list")]

    registry_by_id: dict[str, dict[str, Any]] = {}
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(RegistryError("REGISTRY_ENTRY", f"entry {index} is not an object"))
            continue
        workflow_id = entry.get("id")
        if not isinstance(workflow_id, str) or not WORKFLOW_ID.fullmatch(workflow_id):
            errors.append(RegistryError("INVALID_ID", f"entry {index} has invalid id {workflow_id!r}"))
            continue
        if workflow_id in registry_by_id:
            errors.append(RegistryError("DUPLICATE_REGISTRY_ID", workflow_id))
        registry_by_id[workflow_id] = entry
        if not SEMVER.fullmatch(str(entry.get("version", ""))):
            errors.append(RegistryError("INVALID_VERSION", f"{workflow_id}: {entry.get('version')!r}"))
        if entry.get("status") not in STATUSES:
            errors.append(RegistryError("INVALID_STATUS", f"{workflow_id}: {entry.get('status')!r}"))
        if not isinstance(entry.get("path"), str):
            errors.append(RegistryError("INVALID_PATH", f"{workflow_id}: missing path"))

    manifests = discover_manifests(workflow_root)
    manifest_by_id: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in manifests:
        data = _load_yaml(path)
        workflow_id = data.get("id")
        if not isinstance(workflow_id, str):
            errors.append(RegistryError("MANIFEST_ID_MISSING", str(path.relative_to(ROOT))))
            continue
        if workflow_id in manifest_by_id:
            errors.append(RegistryError("DUPLICATE_MANIFEST_ID", workflow_id))
        manifest_by_id[workflow_id] = (path, data)
        if not WORKFLOW_ID.fullmatch(workflow_id):
            errors.append(RegistryError("INVALID_MANIFEST_ID", f"{path}: {workflow_id}"))

    for workflow_id, entry in registry_by_id.items():
        path = ROOT / str(entry.get("path", ""))
        if not path.is_file():
            errors.append(RegistryError("MISSING_MANIFEST", f"{workflow_id}: {entry.get('path')}"))
            continue
        if workflow_id not in manifest_by_id:
            errors.append(RegistryError("REGISTRY_ORPHAN", workflow_id))
            continue
        manifest_path, manifest = manifest_by_id[workflow_id]
        canonical_path = manifest_path.relative_to(ROOT).as_posix()
        if entry.get("path") != canonical_path:
            errors.append(RegistryError("PATH_DRIFT", f"{workflow_id}: registry={entry.get('path')} manifest={canonical_path}"))
        for field in ("name", "version"):
            if entry.get(field) != manifest.get(field):
                errors.append(RegistryError("METADATA_DRIFT", f"{workflow_id}: {field} registry={entry.get(field)!r} manifest={manifest.get(field)!r}"))
        manifest_category = manifest.get("category")
        if manifest_category is not None and entry.get("category") != manifest_category:
            errors.append(RegistryError("CATEGORY_DRIFT", f"{workflow_id}: registry={entry.get('category')!r} manifest={manifest_category!r}"))

    for workflow_id in manifest_by_id:
        if workflow_id not in registry_by_id:
            errors.append(RegistryError("MANIFEST_ORPHAN", workflow_id))

    known = set(registry_by_id)
    retired = {k for k, v in registry_by_id.items() if v.get("status") == "retired"}
    for workflow_id, (_, manifest) in manifest_by_id.items():
        for reference in sorted(set(_references(manifest))):
            if reference not in known:
                errors.append(RegistryError("UNKNOWN_REFERENCE", f"{workflow_id} -> {reference}"))
            elif reference in retired and not manifest.get("allow_retired_references", False):
                errors.append(RegistryError("RETIRED_REFERENCE", f"{workflow_id} -> {reference}"))

    return errors


def main() -> int:
    errors = validate_registry()
    if errors:
        for error in errors:
            print(error)
        print(f"registry validation failed: {len(errors)} error(s)")
        return 1
    print(f"registry validation passed: {len(discover_manifests())} manifests registered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
