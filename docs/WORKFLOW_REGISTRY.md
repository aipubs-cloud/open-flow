# Workflow Registry

`registry/workflows.yaml` is the authoritative catalog for shipped OWF and AIPUBS workflow manifests.

## Why the registry exists

Workflow manifests describe execution behavior. The registry describes catalog identity and lifecycle. Keeping these concerns separate lets the runtime discover manifests from the filesystem while CI verifies that every discoverable workflow has an intentional catalog entry.

## Registry entry

Each entry contains:

| Field | Meaning |
|---|---|
| `id` | Stable workflow identity. Do not silently reuse an ID. |
| `name` | Human-facing name and manifest consistency check. |
| `path` | Canonical repository path to `workflow.yaml`. |
| `version` | Semantic version mirrored from the manifest. |
| `category` | Catalog grouping. |
| `status` | `experimental`, `active`, `deprecated`, or `retired`. |
| `replacement` | Optional successor for deprecated/retired workflows. |

## Adding a workflow

1. Add the manifest under `workflows/`.
2. Give it a unique OWF or AIPUBS ID.
3. Add exactly one registry entry.
4. Keep the registry `name`, `version`, and `path` identical to the manifest.
5. Run `python tests/validate_workflows.py`.
6. Run `python -m core.registry`.

The validator discovers manifests recursively. Contributors must not edit a hard-coded inventory to make a new workflow visible.

## Renaming a workflow

Treat the workflow ID as a stable identity. If the display name changes, update the registry and manifest together. If the identity itself must change, update every reference and document the migration. Never silently move an old ID to a different workflow.

## Deprecating

Set `status: deprecated` and provide `replacement` when a supported successor exists. Existing references remain resolvable so users can migrate deliberately.

## Retiring

Set `status: retired`. New compositions and references are rejected by registry validation unless the referencing manifest explicitly declares an approved migration exception. Remove the exception when migration is complete.

## Reference integrity

The validator checks workflow IDs found in `prerequisites`, `next_workflow`, `composition`, `pipeline`, `bindings`, `missions`, and nested workflow-bearing structures. Unknown IDs and unauthorized retired references fail CI.

## CI contract

Registry validation is part of the repository CI gate. A green test suite with a broken registry is not considered a valid Open Flow foundation.
