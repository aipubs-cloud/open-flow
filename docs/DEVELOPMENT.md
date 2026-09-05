# Development Guide

## Prerequisites

- Git
- Python 3.8 or newer for OWF-002
- `pytest`
- `PyYAML`

Create an isolated environment:

```bash
python -m venv .venv
python -m pip install --upgrade pip
python -m pip install pytest pyyaml
```

## Validate the repository

```bash
python -m pytest -q
```

Validate workflow manifests directly:

```bash
python tests/validate_workflows.py
```

Run the repository explorer:

```bash
python -m owf002.repo_explorer . --format markdown
python -m owf002.repo_explorer . --format json
```

## Development loop

```text
DISCOVER
  -> DEFINE CONTRACT
  -> IMPLEMENT
  -> TEST
  -> INSPECT DIFF
  -> DOCUMENT
  -> REVIEW
```

## Test expectations

Tests should cover:

- normal behavior
- deterministic behavior where claimed
- invalid inputs
- empty/minimal repositories
- permission or filesystem errors where practical
- serialization and schema contracts
- regressions introduced by fixes

Avoid tests that merely exercise implementation lines without checking behavior.

## Determinism checklist

Before claiming deterministic output, verify:

- directory ordering is stable
- file ordering is stable
- serialization ordering is stable where required
- timestamps are excluded or controlled
- environment-dependent paths are normalized where appropriate
- random sources are seeded or absent
- external network state is not part of the claimed deterministic computation

## Adding a schema

1. Define the contract.
2. Give it a stable identifier.
3. Add required fields and constraints.
4. Add valid and invalid fixtures.
5. Validate examples against the schema.
6. Document compatibility expectations.

## Review discipline

Review the final diff, not only the intended design. Look specifically for:

- accidental secrets
- permission expansion
- destructive behavior
- undocumented dependencies
- dead configuration
- misleading claims
- tests that do not actually exercise the changed behavior
