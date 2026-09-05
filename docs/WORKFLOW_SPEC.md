# OWF Workflow Specification

## 1. Workflow identity

Every workflow MUST have:

- `id`: stable identifier such as `OWF-002`
- `name`: machine-friendly name
- `version`: semantic version of the workflow contract
- `description`: concise purpose

`purpose` may be retained as descriptive metadata for compatibility, but `description` is the normative identity field. IDs are never silently reused for a different purpose.

## 2. Modes

OWF defines five conceptual operating modes:

| Mode | Intent | Default mutation authority |
|---|---|---|
| `observe` | inspect and report | none |
| `plan` | design a change | none |
| `guided` | execute with consequential confirmation | bounded |
| `assisted` | perform authorized development | bounded |
| `autonomous` | execute a predefined objective | explicitly bounded |

A workflow MUST declare its supported operating mode(s). The canonical representation is:

- `mode` for a single-mode workflow.
- `modes` for a multi-mode workflow.

`mode` and `modes` MUST NOT appear together. This prevents contradictory manifests while preserving a compact representation for single-mode workflows.

## 3. Inputs

Structured inputs MUST declare:

- `name`
- `type`
- `required`
- `description`
- optional validation constraints
- optional sensitivity classification when relevant

Simple string inputs remain supported as a compact compatibility form. Never place secrets directly in manifests or fixtures.

## 4. Outputs

Structured outputs MUST declare:

- `name`
- `type` or media format
- optional schema reference when structured
- optional deterministic flag
- optional verification status

Simple string outputs remain supported as a compact compatibility form. A workflow result should distinguish `observed`, `derived`, `verified`, and `unknown` information.

## 5. Capabilities

A workflow may declare required capabilities such as:

- filesystem read
- filesystem write
- process execution
- Git
- GitHub
- network
- MCP

Capabilities should be minimal. A workflow should fail clearly when a required capability is unavailable rather than silently substituting a less-safe behavior.

## 6. Safety

Every workflow should define, directly or through its governing policy:

- default mode
- destructive-operation policy
- permission assumptions
- secret handling rules
- external-side-effect rules
- confirmation requirements
- failure behavior

## 7. Verification

A workflow must state how success is established. Examples:

- unit tests
- schema validation
- static analysis
- reproducible command output
- diff inspection
- independent artifact comparison

Statements such as `tests_passed: true` are only valid when the tests were actually executed and recorded.

## 8. Composition

Workflows may compose agents and skills by stable names. Composition must not weaken the parent workflow's safety policy.

A child component may have stricter restrictions than its parent, but should not silently grant broader authority.

## 9. Failure semantics

Failures should be explicit. Recommended result states:

- `success`
- `partial`
- `blocked`
- `failed`
- `unverified`

A blocked action is not a successful action.

## 10. Versioning

Changing a workflow's objective, required inputs, output meaning, capability requirements, or safety semantics is a contract change.

Use:

- PATCH for clarifications and backward-compatible corrections
- MINOR for backward-compatible additions
- MAJOR for incompatible contract changes

## 11. Evidence discipline

OWF components should use the following vocabulary:

- **FACT**: directly observed or independently verified
- **INFERENCE**: conclusion derived from observed facts
- **HYPOTHESIS**: proposed explanation requiring validation
- **UNKNOWN**: insufficient evidence

A workflow must not promote a hypothesis to a fact merely because it is plausible.
