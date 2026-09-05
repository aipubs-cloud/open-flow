"""Canonical workflow registry validation and filesystem discovery."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any, Iterable

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "registry" / "workflows.yaml"
REGISTRY_SCHEMA_PATH = ROOT / "schemas" / "registry.schema.json"
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
    """Discover workflow manifests recursively from the configured filesystem root."""
    if not root.is_dir():
        return []
    return sorted(path for path in root.rglob("workflow.yaml") if path.is_file())


def _load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def load_registry(registry_path: Path = REGISTRY_PATH) -> dict[str, Any]:
    """Load the canonical registry document without applying semantic checks."""
    return _load_yaml(registry_path)


def _schema_errors(registry: dict[str, Any]) -> list[RegistryError]:
    schema = json.loads(REGISTRY_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return [
        RegistryError("REGISTRY_SCHEMA", error.message)
        for error in sorted(validator.iter_errors(registry), key=lambda item: list(item.path))
    ]


def _references(value: Any) -> Iterable[str]:
    if isinstance(value, str):
        if WORKFLOW_ID.fullmatch(value):
            yield value
    elif isinstance(value, list):
        for item in value:
            yield from _references(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {"workflow", "workflow_id", "next_workflow", "replacement", "composition", "pipeline", "bindings", "missions", "prerequisites"}:
                yield from _references(item)
            elif isinstance(item, (dict, list)):
                yield from _references(item)


def validate_registry(
    registry_path: Path = REGISTRY_PATH,
    workflow_root: Path = WORKFLOW_ROOT,
) -> list[RegistryError]:
    """Validate schema, inventory integrity, filesystem discovery, and references."""
    errors: list[RegistryError] = []
    repo_root = workflow_root.parent
    registry = load_registry(registry_path)
    errors.extend(_schema_errors(registry))
    entries = registry.get("workflows", [])
    if not isinstance(entries, list):
        return errors + [RegistryError("REGISTRY_FORMAT", "workflows must be a list")]

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

    manifests = discover_manifests(workflow_root)
    manifest_by_id: dict[str, tuple[Path, dict[str, Any]]] = {}
    for path in manifests:
        data = _load_yaml(path)
        workflow_id = data.get("id")
        if not isinstance(workflow_id, str):
            errors.append(RegistryError("MANIFEST_ID_MISSING", path.as_posix()))
            continue
        if workflow_id in manifest_by_id:
            errors.append(RegistryError("DUPLICATE_MANIFEST_ID", workflow_id))
        manifest_by_id[workflow_id] = (path, data)
        if not WORKFLOW_ID.fullmatch(workflow_id):
            errors.append(RegistryError("INVALID_MANIFEST_ID", f"{path}: {workflow_id}"))

    for workflow_id, entry in registry_by_id.items():
        relative_path = entry.get("path")
        path = repo_root / str(relative_path or "")
        if not path.is_file():
            errors.append(RegistryError("MISSING_MANIFEST", f"{workflow_id}: {relative_path}"))
            continue
        if workflow_id not in manifest_by_id:
            errors.append(RegistryError("REGISTRY_ORPHAN", workflow_id))
            continue
        manifest_path, manifest = manifest_by_id[workflow_id]
        canonical_path = manifest_path.relative_to(repo_root).as_posix()
        if relative_path != canonical_path:
            errors.append(RegistryError("PATH_DRIFT", f"{workflow_id}: registry={relative_path} manifest={canonical_path}"))
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
    retired = {workflow_id for workflow_id, entry in registry_by_id.items() if entry.get("status") == "retired"}
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
    print(f"registry validation passed: {len(discover_manifests())} manifests discovered and registered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
