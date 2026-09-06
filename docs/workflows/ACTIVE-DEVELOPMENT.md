# Active Workflow Development and Pull Requests

This document records which workflow-related pull requests are currently open, why they exist, what they change, and what must happen before they can be considered complete.

## Snapshot

At catalog generation time, the repository has **two open pull requests** that materially affect workflow infrastructure.

| PR | Branch | Area | Purpose | Current disposition |
|---|---|---|---|---|
| #40 | `feat/workflow-registry-contract` | Registry | Establish canonical registry/discovery/reference integrity | **Changes required** |
| #56 | `feat/aipubs-start-003-explorer` | START-003 | Build evidence-grounded learner repository exploration | **In progress** |

## PR #40 — canonical workflow registry

### Why it exists

Open Flow needs one authoritative machine-readable inventory of workflow identity, path, version, category, and lifecycle. Without that boundary, adding workflows can silently create duplicate IDs, orphaned manifests, stale registry entries, or broken references.

### What it is trying to establish

- filesystem-backed workflow discovery;
- registry/manifest synchronization;
- duplicate detection;
- orphan detection;
- path and metadata integrity;
- workflow-reference integrity;
- lifecycle validation;
- a reusable registry boundary for the resolver/composer and Journey Orchestrator.

### Current review finding

The PR currently has a documented review disposition of **changes required**. The critical requirement is that schema validation must not replace executable semantic validation. `core/registry.py` must retain explicit checks for:

- semantic version validity;
- supported lifecycle states;
- valid required paths;
- workflow ID validity;
- duplicate IDs;
- registry/manifest metadata drift;
- orphan detection;
- workflow-reference integrity.

It also needs regression coverage and green CI on the current PR head.

### Important repository-state concern

PR #40 targets `main` but its recorded base SHA is older than the current `main` used by the newer work. It therefore should not be treated as a clean independent foundation until its changes are reconciled with the current tree and re-reviewed. Its `merge_commit_sha` field is present in the connector snapshot even though GitHub still reports the PR as open and unmerged, so the authoritative state for this catalog is **open/unmerged**.

### Relationship to issues

Primary foundation: **#26**.

Related boundaries:

- **#27** schema-driven discovery/validation;
- **#28** end-to-end resolver/composer tests;
- **#29** control-plane artifact validation;
- **#32** compatibility/versioning;
- **#36** safety monotonicity.

### Required completion sequence

```text
Reconcile with current main
        ↓
Restore semantic validation
        ↓
Add regression fixtures
        ↓
Run full tests + registry validation
        ↓
Review current diff
        ↓
Green CI
        ↓
Merge
```

---

## PR #56 — AIPUBS-START-003 repository explorer

### Why it exists

The beginner journey needs a repository-exploration experience between repository creation and practical Git work. START-003 is intended to translate repository evidence into a learner-friendly mental model while reusing the deterministic OWF-002 collector.

### What it adds

The first implementation slice includes:

- an upgraded START-003 workflow manifest;
- explicit observe-only safety boundaries;
- composition with OWF-002;
- `repository-map` contract;
- `architecture-map` contract;
- `execution-map` contract;
- `learning-summary` contract;
- START-003 result contract;
- an interactive Copilot mentor protocol;
- deterministic contract tests.

### Why it must not duplicate OWF-002

OWF-002 is the reusable evidence engine. START-003 is the learner-facing interpretation/orientation layer.

The intended architecture is:

```text
START-003
    ↓
OWF-002 evidence collection
    ↓
observed / inferred / unknown classification
    ↓
learner maps
    ↓
comprehension checkpoint
    ↓
one next workflow
```

This separation keeps the scanner reusable and the curriculum experience teachable.

### Current remaining gates

- canonical OWF-002 / START-003 identity reconciliation (#49);
- broader sparse/incomplete/evidence-ambiguous fixtures;
- canonical registry reference validation;
- routing and Journey Orchestrator handoff tests;
- documentation/invocation examples;
- green CI evidence.

### Related issues

- **#4:** overall START-003 learner workflow;
- **#41:** learner artifact contracts;
- **#42:** START-003 implementation;
- **#49:** canonical identity/path relationship;
- **#26:** registry integrity;
- **#28:** composition/resolver contract;
- **#30:** deterministic execution/dry-run semantics;
- **#36:** safety monotonicity.

### Completion sequence

```text
Canonical identity
       ↓
Registry references
       ↓
Fixture matrix
       ↓
Routing / orchestrator tests
       ↓
Documentation examples
       ↓
CI
       ↓
Full review
       ↓
Merge
```

---

# Issues currently driving workflow development

The most important open foundation issues form a dependency graph rather than an unordered backlog:

```text
#26 Canonical Registry
      │
      ├───────────────┐
      ↓               ↓
#27 Schema Discovery  #29 Control-Plane Contracts
      │               │
      └───────┬───────┘
              ↓
        #28 Resolver/Composer
              │
        ┌─────┴─────┐
        ↓           ↓
#30 Execution   #36 Safety Monotonicity
              │
              ↓
        Journey Orchestration
              │
              ↓
       Learner Workflows
```

START-003 additionally depends on #41 and the identity reconciliation tracked by #49.

## Duplicate identity issue

Issues **#47** and **#49** describe substantially overlapping OWF-002/START-003 identity reconciliation work. The repository should consolidate these rather than develop two parallel issue tracks. The catalog treats **#49** as the active reference because PR #56 explicitly tracks it.

# What is not an active PR

The following are important but are **not currently open pull requests** in the current repository snapshot:

- OWF-002 hardening from the foundation work has already been merged into `main`.
- The earlier foundation hardening PR #22 has already been merged.
- Many AIPUBS workflow implementation issues remain open, but no corresponding open PR was found for them in the current two-PR snapshot.

This distinction matters: an issue means planned/required work; a PR means a concrete proposed change; a merged PR is historical repository state.

# Recommended order of work

1. Reconcile and finish the canonical registry work in #40.
2. Establish the canonical OWF-002/START-003 relationship through #49.
3. Complete START-003 #56 on top of that canonical relationship.
4. Strengthen resolver/composer tests in #28.
5. Define deterministic execution/dry-run semantics in #30.
6. Implement safety monotonicity in #36.
7. Continue the learner graph with GIT, GITHUB, BUILD, VERIFY, RELEASE, DEPLOY, OPERATE, and MENTOR workflows.

The key architectural principle is to avoid building dozens of disconnected prompts. Each learner workflow should consume validated evidence/artifacts from shared primitives and return structured results that the composer can route forward.
