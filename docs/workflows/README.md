# Open Flow Workflow Catalog

This directory is the human-readable companion to the machine-readable workflow registry at `registry/workflows.yaml`.

## Purpose

The catalog answers four questions that the registry alone cannot answer well:

1. **What does every workflow do?**
2. **When should a user invoke it?**
3. **What does it consume, produce, and compose with?**
4. **What is actually implemented today versus merely planned or represented by a manifest?**

The catalog is intentionally evidence-based. A workflow being listed in the registry means a manifest exists and is registered. It does **not** automatically mean that a full executable implementation, tests, or an end-to-end user experience exists.

## Source of truth

- Machine identity, path, version, category, and lifecycle: `registry/workflows.yaml`
- Manifest contract: `schemas/workflow.schema.json` and `docs/WORKFLOW_SPEC.md`
- Human-facing category model: `docs/workflow-categories.md`
- Composition/runtime: `core/composer.py`, `core/registry.py`, and the Copilot skills under `.copilot/skills/`
- Safety: `core/safety.py`, `docs/SAFETY_MODEL.md`, `docs/safety-monotonicity.md`, and repository hooks
- Beginner journey: `docs/aipubs-github-beginner-journey.md`

## Current inventory

The repository currently registers **31 workflows**:

| Family | Count | Registered workflows |
|---|---:|---|
| Core OWF | 11 | OWF-001 through OWF-011 |
| START | 4 | AIPUBS-START-001, -002, -003, -010 |
| GIT | 2 | AIPUBS-GIT-001, -002 |
| GITHUB | 5 | AIPUBS-GITHUB-001 through -005 |
| BUILD | 1 | AIPUBS-BUILD-001 |
| VERIFY | 2 | AIPUBS-VERIFY-001, -002 |
| RELEASE | 1 | AIPUBS-RELEASE-001 |
| DEPLOY | 1 | AIPUBS-DEPLOY-001 |
| OPERATE | 1 | AIPUBS-OPERATE-001 |
| SHIELD | 1 | AIPUBS-SHIELD-001 |
| MENTOR | 2 | AIPUBS-MENTOR-001, -002 |
| **Total** | **31** | **All currently marked `active` in the registry** |

## Important distinction: registered vs implemented

Open Flow currently has several layers of maturity:

- **Executable foundation:** OWF-002 has a deterministic repository collector and tests. Core composer, registry, repository creator, safety, hooks, and Copilot skills also exist.
- **Rich learner workflow:** AIPUBS-START-001 has a substantial instructional protocol and observation helper; START-002 has a substantial instructional protocol and repository creation implementation boundary.
- **Manifest-level workflows:** many other workflows currently have a machine-readable manifest but do not yet have dedicated executable code, tests, or complete interactive protocols.
- **Taxonomy/future surface:** `docs/workflow-categories.md` defines a much larger future catalog. Those names are not counted here unless a registered manifest currently exists.

## Beginner journey

The intended learner graph is approximately:

```text
START-001
  ↓
START-002 / START-003
  ↓
GIT-001
  ↓
GIT-002
  ↓
GITHUB-001
  ↓
BUILD-001
  ↓
VERIFY-001
  ↓
GITHUB-002
  ↓
GITHUB-003
  ↓
GITHUB-004
  ↓
GITHUB-005
  ↓
VERIFY-002
  ↓
RELEASE-001
  ↓
DEPLOY-001
  ↓
OPERATE-001
  ↓
START-010
```

This is a learning graph, not a requirement that every user traverse every node. OWF-011 is intended to make such paths composable and adaptive once the resolver/composer contract is complete.

## Active pull requests

At the time this catalog was generated, two pull requests were open and materially affect the workflow system:

### PR #40 — canonical workflow registry contract

Branch: `feat/workflow-registry-contract`

Purpose: harden the registry so workflow discovery, metadata synchronization, orphan detection, and reference integrity become authoritative rather than relying on ad-hoc inventories.

Current state: **open, changes required**. The review requires explicit semantic validation to remain in `core/registry.py` in addition to JSON Schema validation, plus regression tests and green CI. The branch was created from an older `main` base than the current repository head, so it must be reconciled before it can safely become the canonical registry implementation.

### PR #56 — evidence-grounded START-003 repository explorer

Branch: `feat/aipubs-start-003-explorer`

Purpose: turn AIPUBS-START-003 into a learner-facing, evidence-grounded repository orientation workflow that composes the deterministic OWF-002 repository explorer rather than creating a second scanner.

Current state: **open**. The first implementation slice exists, including learner artifact schemas, observe-only protocol, and deterministic contract tests. Remaining gates include registry/identity reconciliation, broader fixtures, Journey Orchestrator handoff tests, documentation examples, and green CI.

## Reading the individual entries

Each entry in `CATALOG.md` records:

- identity and canonical path;
- intended user and problem;
- inputs and outputs where known;
- safety/mode expectations;
- composition relationships;
- implementation evidence currently present in the repository;
- recommended next workflow;
- current engineering maturity.

The catalog should be updated whenever a workflow is added, renamed, versioned, deprecated, implemented, or materially changed.
