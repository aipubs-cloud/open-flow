# OWF Safety Model

## Principle

OWF treats safety as a layered control system, not a single prompt instruction.

```text
Intent
  -> workflow boundary
  -> capability boundary
  -> policy gate
  -> host permission
  -> action
  -> verification
  -> audit trail
```

Each layer reduces risk; none should be assumed to replace the others.

## Risk classes

### Read-only

Examples:

- listing files
- reading configuration
- parsing metadata
- running non-mutating validation

These actions should normally be available in `observe` mode.

### Local mutation

Examples:

- editing files
- generating artifacts
- changing configuration

These require an authorized execution mode and should produce a diff or equivalent audit artifact.

### External side effects

Examples:

- pushing Git commits
- opening or modifying GitHub issues
- deploying services
- sending network requests that change remote state

These require explicit capability and policy boundaries. `autonomous` does not imply permission to perform them.

### High-consequence operations

Examples include credential changes, destructive deletion, privilege changes, production deployment, and irreversible migrations.

Such operations should be disabled by default and require explicit host-level authorization and appropriate human review.

## Confirmation policy

Confirmation should be based on consequence, not merely on command syntax. A harmless read command need not interrupt a workflow repeatedly; an irreversible external action should not be hidden inside a long chain of operations.

## Secret handling

Secrets must not be:

- committed to the repository
- embedded in examples
- printed into workflow results
- included in telemetry
- copied into issue comments
- written into generated survey artifacts

Use environment variables, host secret stores, or equivalent secure mechanisms.

## Fail-safe behavior

When a safety decision cannot be established, the workflow should prefer:

```text
STOP -> REPORT -> REQUEST AUTHORIZATION OR CLARIFICATION
```

It should not silently broaden permissions or invent an interpretation that makes execution possible.

## Autonomous mode

Autonomous mode means the objective is sufficiently bounded to execute without per-step confirmation. It does not mean unrestricted access.

An autonomous workflow should have:

- explicit objective
- allowed capabilities
- denied capabilities
- resource limits
- stop conditions
- verification gates
- failure reporting

## Host enforcement

Repository instructions cannot create operating-system isolation. Real security boundaries must be implemented by the execution host, CI permissions, sandbox, container, cloud IAM, GitHub permissions, or equivalent enforcement mechanism.
