<div align="center">

# Open Workflow Framework (OWF)

**A lightweight, Git-native ecosystem of composable workflows for GitHub Copilot CLI and compatible agent environments.**

[![OWF Version](https://img.shields.io/badge/OWF-0.1.0-blue.svg)](workflow.yaml)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Runtime](https://img.shields.io/badge/runtime-Python%203.8%2B-blue.svg)](workflows/002-repository-explorer)

</div>

---

## What is Open Flow?

**Open Workflow Framework (OWF)** turns common AI-assisted engineering activities into explicit, reusable, testable workflows.

Instead of treating an AI coding agent as a blank chat window, OWF provides a structured operating model:

```text
UNDERSTAND → PLAN → EXECUTE → VERIFY → EXPLAIN
```

Workflows can teach users while they work, provide safety gates around consequential actions, preserve evidence, and produce artifacts that can be reviewed through normal Git and GitHub practices.

OWF is deliberately **not a new agent runtime**. It is a Git-native workflow layer that works with the capabilities already provided by environments such as GitHub Copilot CLI.

## v0.1.0 Workflows

| ID | Workflow | Purpose |
|---|---|---|
| OWF-001 | First Contact | Learn an unfamiliar repository |
| OWF-002 | Repository Explorer | Collect deterministic repository evidence |
| OWF-003 | Project Doctor | Diagnose project health |
| OWF-004 | Guided Bug Fix | Reproduce and fix bugs |
| OWF-005 | Test Builder | Build regression protection |
| OWF-006 | Security Auditor | Perform evidence-driven security analysis |
| OWF-007 | Documentation Engineer | Align documentation with implementation |
| OWF-008 | GitHub Maintainer | Turn findings into GitHub work |
| OWF-009 | Research Lab | Conduct reproducible technical research |
| OWF-010 | Autonomous Builder | Execute bounded engineering objectives |

Each workflow has a machine-readable manifest describing its identity, purpose, steps, outputs, mode, and safety expectations.

## Architecture

```text
                         OPEN WORKFLOW FRAMEWORK
                                    |
             +----------------------+----------------------+
             |                      |                      |
         Workflows                Agents                 Skills
             |                      |                      |
             +----------------------+----------------------+
                                    |
                         Safety + Verification
                                    |
                              Copilot CLI
                                    |
                         Git / GitHub / MCP
```

### Core components

- **Workflows** define versioned engineering processes.
- **Agents** provide specialized roles such as mentor, architect, debugger, researcher, tester, security auditor, and release manager.
- **Skills** provide reusable procedures that agents can invoke.
- **Instructions** establish repository-wide operating principles.
- **Schemas** define machine-readable contracts.
- **Tests** verify workflow structure and invariants.
- **Hooks** and **MCP profiles** define extension boundaries without coupling OWF to an unverified provider-specific runtime format.

## Operating Modes

OWF defines five safety-oriented modes:

| Mode | Behavior |
|---|---|
| `observe` | Read and analyze without modifying files |
| `plan` | Produce a proposed plan without making changes |
| `guided` | Explain consequential actions and seek confirmation |
| `assisted` | Perform bounded, authorized work |
| `autonomous` | Execute a bounded objective under explicit policy and verification gates |

Autonomous mode does **not** override repository policy, permissions, safety controls, or verification requirements.

## Evidence First

A central OWF principle is the separation of **observation** from **interpretation**.

```text
Observed evidence
      ↓
Structured facts
      ↓
Inference / analysis
      ↓
Recommendation
      ↓
Verification
```

Agents should not fabricate files, APIs, vulnerabilities, test results, architectural relationships, or completion claims.

When something is unknown, OWF encourages the workflow to say that it is unknown and identify what evidence would resolve the uncertainty.

## OWF-002: Repository Explorer

OWF-002 provides the foundation for repository-aware workflows.

Its runtime collector is intentionally:

- deterministic
- read-only
- Python standard-library only
- suitable for Python 3.8+
- designed to avoid noisy generated and dependency directories
- capable of producing Markdown or machine-readable JSON survey data

The collector performs factual discovery across six areas:

1. **Repository discovery**
2. **Architecture indicators**
3. **Candidate execution paths**
4. **Tests and test configuration**
5. **CI configuration**
6. **Deployment and infrastructure indicators**

A subsequent Step 7 can synthesize that evidence into human-oriented explanations and learning artifacts.

```text
Repository
    |
    v
OWF-002 Collector
    |
    +--> Raw survey / observed facts
    |
    v
Step 7 synthesis
    |
    +--> Repository Map
    +--> Architecture Map
    +--> Execution Map
    +--> Learning Summary
    |
    v
OWF-003+ downstream workflows
```

### What OWF-002 does not claim

The collector does **not** by itself prove:

- the repository's intended architecture
- runtime correctness
- security posture
- code quality
- production topology
- complete execution flow

Those are analytical questions that require additional evidence and, where appropriate, execution or human review.

## Repository Layout

```text
open-flow/
├── .copilot/
│   ├── agents/             reusable role definitions
│   ├── instructions/       repository-wide operating policy
│   └── skills/             reusable procedures
├── workflows/              versioned workflow manifests
├── schemas/                machine-readable contracts
├── hooks/                  extension and safety hook guidance
├── mcp/                    MCP integration boundary guidance
├── tests/                  workflow validation and regression tests
├── workflow.yaml           root OWF manifest
├── README.md               project documentation
└── LICENSE                 project license
```

## Validation

OWF keeps runtime dependencies deliberately small. The current test harness uses `pytest` and `PyYAML` for development-time validation; the OWF-002 collector itself remains standard-library-only at runtime.

```bash
python -m pip install pytest pyyaml
pytest -q
```

The validation suite checks the workflow manifest set, required fields, supported operating modes, and workflow identifier uniqueness.

## Using OWF with Copilot CLI

OWF is designed to complement the native capabilities of GitHub Copilot CLI rather than replace them.

A typical interaction can follow this pattern:

```text
User objective
     ↓
Mentor
     ↓
Repository discovery
     ↓
Specialist workflow
     ↓
Plan
     ↓
Authorized execution
     ↓
Tests / verification
     ↓
Reviewable Git change
     ↓
Pull request
```

The repository's `.copilot/` definitions provide reusable agent, instruction, and skill material that can be incorporated into an appropriate Copilot CLI setup.

## Git-Native Development

OWF is intended to be developed like normal open-source software:

```text
Issue
  ↓
Branch
  ↓
Change
  ↓
Test
  ↓
Review
  ↓
Pull Request
  ↓
Merge
```

Workflow definitions are source code. Changes should therefore be reviewable, reproducible, and traceable through Git history.

## Design Goals

OWF aims to be:

- **Git-native**
- **lightweight**
- **open source**
- **composable**
- **reproducible**
- **testable**
- **auditable**
- **education-oriented**
- **provider-friendly**
- **MCP-compatible**

The framework favors explicit contracts over opaque orchestration and small composable workflows over a single monolithic prompt.

## Roadmap

The v0.1.0 foundation establishes the first workflow set and supporting primitives. Future work can build toward:

- **OWF-011 Workflow Composer** for deterministic workflow composition
- stronger schema validation
- workflow dependency and handoff contracts
- executable learning journeys
- richer provenance and evidence records
- expanded evaluation and regression testing
- validated native hook integrations
- optional MCP-backed project memory and research capabilities

The goal is to make workflow composition inspectable rather than turning the framework into a hidden mega-prompt.

## Status

OWF `0.1.0` is an **experimental open-source starter framework**.

It is not, by itself, a security boundary, sandbox, autonomous-agent runtime, or guarantee of correct AI behavior. Safety and correctness depend on the execution environment, repository policy, permissions, workflow configuration, verification, and human oversight appropriate to the task.

## License

Open Workflow Framework is released under the MIT License. See [LICENSE](LICENSE) for details.
