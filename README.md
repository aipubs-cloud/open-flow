# Open Workflow Framework

Open Workflow Framework (OWF) is a lightweight, Git-native ecosystem of composable workflows for GitHub Copilot CLI and compatible agent environments.

OWF organizes instructions, agents, skills, workflow manifests, safety policies, and verification into reusable engineering workflows. It is deliberately not a new agent runtime.

## v0.1.0 workflows

| ID | Workflow | Purpose |
|---|---|---|
| OWF-001 | First Contact | Learn an unfamiliar repository |
| OWF-002 | Repository Explorer | Collect repository evidence |
| OWF-003 | Project Doctor | Diagnose project health |
| OWF-004 | Guided Bug Fix | Reproduce and fix bugs |
| OWF-005 | Test Builder | Build regression protection |
| OWF-006 | Security Auditor | Perform evidence-driven security analysis |
| OWF-007 | Documentation Engineer | Align docs with implementation |
| OWF-008 | GitHub Maintainer | Turn findings into GitHub work |
| OWF-009 | Research Lab | Conduct reproducible technical research |
| OWF-010 | Autonomous Builder | Execute bounded engineering objectives |

## Architecture

```text
                 OPEN WORKFLOW FRAMEWORK
                            |
          +-----------------+-----------------+
          |                 |                 |
       Workflows          Agents           Skills
          |                 |                 |
          +-----------------+-----------------+
                            |
                    Safety + Verification
                            |
                         Copilot CLI
                            |
                   Git / GitHub / MCP
```

A workflow is a versioned composition of reusable actions. Agents provide role-specific reasoning. Skills provide reusable procedures. Copilot CLI supplies the execution environment and native capabilities.

## Operating modes

- `observe` - read/analyze only
- `plan` - produce a plan without changes
- `guided` - explain consequential actions and seek confirmation
- `assisted` - perform bounded authorized work
- `autonomous` - execute a bounded objective under explicit policy

Autonomous mode does not override repository policy, permissions, or safety gates.

## Core loop

```text
UNDERSTAND -> PLAN -> EXECUTE -> VERIFY -> EXPLAIN
```

The framework treats evidence and verification as first-class outputs. An agent must not claim a test passed, a vulnerability exists, or an objective is complete without supporting evidence.

## Repository layout

```text
.copilot/
  agents/          reusable role definitions
  instructions/    repository-wide operating policy
  skills/          reusable procedures
workflows/         versioned workflow manifests
schemas/           machine-readable contracts
tests/             workflow validation
```

## OWF-002 foundation

OWF-002 is the first evidence-collection workflow. Its Python collector is deterministic, read-only, dependency-free at runtime, and emits versioned survey data for downstream workflows.

```text
Repository
   |
   v
OWF-002 Explorer
   |
   +--> survey.json
   +--> survey.md
   |
   v
OWF-003+ analysis
```

OWF-002 reports what was observed. It does not claim to understand repository intent, correctness, security posture, or code quality.

## Validation

The test harness validates that all ten workflow manifests exist, contain required fields, use supported modes, and have unique OWF identifiers.

```bash
python -m pip install pytest pyyaml
pytest -q
```

## Design goals

- Git-native
- lightweight
- open source
- composable
- reproducible
- testable
- auditable
- provider-friendly
- MCP-compatible
- education-oriented

## Status

OWF `0.1.0` is an experimental starter specification and workflow set. It is not, by itself, a security boundary or autonomous-agent runtime.
