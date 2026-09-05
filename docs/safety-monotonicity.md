# Open Flow Safety Monotonicity

## Status

Normative foundation for composed workflows. This document defines the safety invariant implemented by `core/safety.py` and tested by `tests/test_safety.py`.

## Principle

Composition is **restriction-preserving**. A parent workflow, resolver, agent, host capability boundary, or execution context may add restrictions, but it may not remove or weaken restrictions inherited from a child workflow.

The effective policy is therefore the safe intersection of applicable authority, with restrictive requirements retained:

```text
child policy ─┐
parent policy ├─> safety resolver ─> effective policy
host boundary ┤
user gate ────┘
```

The resolver must fail closed whenever an authority or capability is missing or ambiguous.

## Policy dimensions

The canonical policy covers:

- execution mode: `observe < plan < guided < assisted < autonomous`
- write authority
- destructive operations
- confirmation requirements
- force push
- delete operations
- secret exposure
- credential requests
- network authority
- dry-run
- filesystem scope
- repository scope
- capabilities
- evidence requirements

The mode ordering is a privilege ordering. When workflows are composed, the least-privileged mode wins.

Boolean authority is combined conservatively. A capability is retained only when every applicable policy explicitly retains it. Explicit resource scopes are intersected.

## Required invariants

1. An `observe` child remains observe-only when composed into `assisted` or `autonomous` execution.
2. `destructive_operations: false` can never become `true` through composition.
3. A required write confirmation can never be removed by a parent.
4. A requested capability absent from the effective policy produces `capability_unavailable` rather than an implicit escalation.
5. A parent cannot broaden filesystem or repository scope.
6. A dry-run restriction remains side-effect-free through nested composition.
7. Evidence requirements remain enabled when any applicable policy requires them.
8. Cancellation, blocked, and capability-unavailable states must be terminal for that attempted action unless a new explicit authorization boundary is established.
9. Nested composition must be equivalent to resolving all applicable policies together. Grouping must not create a privilege escalation.
10. A safety decision must be serializable into the workflow execution plan/result so it can be audited.

## Authorization boundary

Changing a workflow from read-only to write-capable is not an ordinary composition detail. It is a new authorization boundary. The workflow must stop, declare the new authority, show the consequences, and obtain whatever confirmation the applicable policy requires.

A composition such as:

```text
OWF-002 (observe)
    ↓
assisted parent
    ↓
autonomous parent
```

must still resolve to an observe-only effective policy unless a separately authorized workflow explicitly establishes a new boundary. A parent cannot smuggle write authority through the child.

## Machine-readable result

Implementations should expose at least:

```yaml
safety:
  requested_mode: autonomous
  effective_mode: observe
  write: false
  destructive_operations: false
  require_confirmation_for_write: true
  dry_run: true
  decision: restricted
  status: capability_unavailable
```

The exact result envelope is owned by the workflow execution/result specification. The important invariant is that the recorded effective policy is the policy actually enforced, not merely the policy requested by a caller.

## Relationship to Open Flow

This foundation applies to workflow registry validation, manifest composition, dry-run execution, and future workflow composition. It is especially important for beginner workflows such as `AIPUBS-START-002`, repository exploration such as `AIPUBS-START-003`, and controlled Git operations such as `AIPUBS-GIT-001`.

The implementation intentionally has no provider-specific dependency. GitHub, Copilot CLI, MCP servers, or other execution hosts may provide capabilities, but none may use those capabilities to weaken the effective Open Flow policy.
