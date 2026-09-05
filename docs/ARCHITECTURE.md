# OWF Architecture

## Purpose

Open Workflow Framework (OWF) is a Git-native composition layer for reusable engineering workflows. It provides conventions and machine-readable contracts around host capabilities such as Git, GitHub, Copilot CLI, test runners, and MCP services.

OWF is intentionally not an agent runtime. The host remains responsible for execution, permissions, authentication, process isolation, and tool availability.

## Architectural layers

```text
User objective
      |
      v
Workflow manifest
      |
      +---- Policy / safety mode
      |
      +---- Agents
      |
      +---- Skills
      |
      +---- Hooks
      |
      +---- External capabilities / MCP
      |
      v
Host execution environment
      |
      v
Evidence + verification + result
```

### Workflows

A workflow is the primary unit of composition. It defines an objective, boundaries, inputs, outputs, capabilities, operating modes, and verification requirements.

Workflows should be declarative where possible. A manifest describes what the workflow means; host-specific instructions explain how the host can realize it.

### Agents

Agents provide role-specific reasoning responsibilities. Examples include architecture, debugging, security auditing, testing, research, mentoring, and release management.

Agents should not duplicate global policy. Repository-wide safety and operating rules belong in instructions or policy contracts.

### Skills

Skills are reusable procedures. A skill should describe inputs, method, expected artifacts, verification, and limitations. Skills should be composable and independently testable where practical.

### Hooks

Hooks are lifecycle extension points. OWF defines conceptual categories only until a host's native hook contract has been validated. No invented runtime protocol should be presented as native support.

### MCP profiles

MCP is an external capability boundary. Profiles should state the service purpose, capabilities, trust assumptions, data boundaries, and safety mode. An MCP server is not implicitly trusted because a workflow requests it.

### Schemas

Schemas define machine-readable contracts for workflow manifests, policies, agents, skills, hooks, and results. Schema changes are public contract changes and should be versioned deliberately.

## Data flow

A normal workflow should produce a traceable sequence:

```text
objective
  -> context discovery
  -> plan
  -> authorized actions
  -> observations
  -> verification
  -> result
```

Each transition should preserve enough information to explain what happened and what remains uncertain.

## Determinism

Where a workflow claims deterministic behavior, it must identify:

- inputs
- ordering rules
- ignored paths or sources
- environment assumptions
- random seeds, if applicable
- serialization rules
- versioned schema
- expected invariants

A deterministic claim does not mean the external world is deterministic. It means the workflow's defined computation is reproducible under stated conditions.

## Security boundary

OWF policy is advisory unless enforced by the host. The repository must never imply that a Markdown instruction can prevent a capable host from performing an operation it is permitted to perform.

Security-sensitive workflows therefore document both policy intent and host enforcement requirements.

## Compatibility

Host-specific behavior belongs at the integration boundary. When Copilot CLI, GitHub Actions, MCP, or another host changes its native schema, OWF integrations should be validated before updating claims.
