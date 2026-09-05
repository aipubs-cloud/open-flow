# AIPubs Open Flow Workflow Categories

AIPubs Open Flow is a free, open-source workflow ecosystem designed to help new GitHub users learn by doing while progressively introducing software development, collaboration, security, testing, research, and automation.

## Category model

| Category | Brand | Scope |
|---|---|---|
| START | AIPubs / Start | GitHub fundamentals and first contribution |
| EXPLORER | AIPubs / Explorer | Repository discovery and orientation |
| MENTOR | AIPubs / Mentor | Learn concepts while working |
| BUILDER | AIPubs / Builder | Software creation and feature development |
| DEBUGGER | AIPubs / Debugger | Reproduction, diagnosis, and bug fixing |
| VERIFY | AIPubs / Verify | Tests, regression protection, and quality |
| SHIELD | AIPubs / Shield | Security and supply-chain fundamentals |
| DOCS | AIPubs / Docs | Documentation and project communication |
| GIT | AIPubs / Git | Version control fundamentals |
| GITHUB | AIPubs / GitHub | Issues, pull requests, reviews, Actions, and governance |
| RELEASE | AIPubs / Release | Versioning, releases, deployment, and verification |
| RESEARCH | AIPubs / Research | Reproducible technical research |
| AUTONOMY | AIPubs / Autonomy | Bounded advanced agent automation |

## Suggested workflow families

### START

- START-001 GitHub Orientation
- START-002 Repository Orientation
- START-003 First Clone
- START-004 First Branch
- START-005 First Commit
- START-006 First Pull Request
- START-007 First Issue
- START-008 First Contribution

### EXPLORER

- EXPLORER-001 Repository Explorer
- EXPLORER-002 Architecture Explorer
- EXPLORER-003 Dependency Explorer
- EXPLORER-004 Entry-Point Explorer
- EXPLORER-005 Test Explorer
- EXPLORER-006 CI Explorer
- EXPLORER-007 Deployment Explorer
- EXPLORER-008 Documentation Explorer
- EXPLORER-009 Repository Map
- EXPLORER-010 Project Orientation

### MENTOR

- MENTOR-001 Explain This Repository
- MENTOR-002 Explain This File
- MENTOR-003 Explain This Function
- MENTOR-004 Explain This Error
- MENTOR-005 Explain This Commit
- MENTOR-006 Explain This Pull Request
- MENTOR-007 Teach Me Git
- MENTOR-008 Teach Me Testing
- MENTOR-009 Teach Me Security
- MENTOR-010 Teach Me Architecture

### BUILDER

- BUILD-001 Create a Project
- BUILD-002 Add a Feature
- BUILD-003 Create a Module
- BUILD-004 Add an API
- BUILD-005 Add Configuration
- BUILD-006 Add a CLI Command
- BUILD-007 Integrate a Dependency
- BUILD-008 Refactor a Component
- BUILD-009 Create a Service
- BUILD-010 Build an MVP

### DEBUGGER

- DEBUG-001 Understand the Error
- DEBUG-002 Reproduce the Bug
- DEBUG-003 Isolate the Failure
- DEBUG-004 Inspect Logs
- DEBUG-005 Trace Execution
- DEBUG-006 Form a Hypothesis
- DEBUG-007 Create a Regression Test
- DEBUG-008 Fix the Bug
- DEBUG-009 Verify the Fix
- DEBUG-010 Postmortem

### VERIFY

- VERIFY-001 Discover Existing Tests
- VERIFY-002 Test a Function
- VERIFY-003 Test a Feature
- VERIFY-004 Write a Regression Test
- VERIFY-005 Test an API
- VERIFY-006 Test CLI Behavior
- VERIFY-007 Test Failure Conditions
- VERIFY-008 Coverage Gap Analysis
- VERIFY-009 CI Verification
- VERIFY-010 Release Verification

### SHIELD

- SHIELD-001 Security Orientation
- SHIELD-002 Secret Detection
- SHIELD-003 Dependency Audit
- SHIELD-004 Permission Audit
- SHIELD-005 GitHub Actions Audit
- SHIELD-006 Configuration Audit
- SHIELD-007 API Security Review
- SHIELD-008 Supply Chain Review
- SHIELD-009 Repository Security Report
- SHIELD-010 Remediation Workflow

### DOCS

- DOCS-001 Repository README
- DOCS-002 Installation Guide
- DOCS-003 Quickstart
- DOCS-004 API Documentation
- DOCS-005 CLI Documentation
- DOCS-006 Architecture Documentation
- DOCS-007 Contributor Guide
- DOCS-008 Security Policy
- DOCS-009 Changelog
- DOCS-010 Documentation Audit

### GIT

- GIT-001 Repository
- GIT-002 Clone
- GIT-003 Branch
- GIT-004 Commit
- GIT-005 Diff
- GIT-006 Merge
- GIT-007 Rebase
- GIT-008 Pull Request
- GIT-009 Conflict Resolution
- GIT-010 Recovery

### GITHUB

- GITHUB-001 Issues
- GITHUB-002 Projects
- GITHUB-003 Pull Requests
- GITHUB-004 Reviews
- GITHUB-005 Labels
- GITHUB-006 Milestones
- GITHUB-007 Releases
- GITHUB-008 Actions
- GITHUB-009 Discussions
- GITHUB-010 Repository Governance

### RELEASE

- RELEASE-001 Release Readiness
- RELEASE-002 Version Analysis
- RELEASE-003 Changelog Generation
- RELEASE-004 Release Notes
- RELEASE-005 Tag Preparation
- RELEASE-006 GitHub Release
- RELEASE-007 Package Build
- RELEASE-008 Deployment Check
- RELEASE-009 Rollback Plan
- RELEASE-010 Post-Release Verification

### RESEARCH

- RESEARCH-001 Research Question
- RESEARCH-002 Literature Discovery
- RESEARCH-003 Hypothesis
- RESEARCH-004 Experiment Design
- RESEARCH-005 Dataset Analysis
- RESEARCH-006 Reproducibility
- RESEARCH-007 Evidence Review
- RESEARCH-008 Technical Report
- RESEARCH-009 Research Publication
- RESEARCH-010 Peer Review

### AUTONOMY

- AUTO-001 Bounded Task
- AUTO-002 Autonomous Issue Resolution
- AUTO-003 Autonomous Testing
- AUTO-004 Autonomous Documentation
- AUTO-005 Autonomous Refactoring
- AUTO-006 Autonomous Security Remediation
- AUTO-007 Autonomous PR Preparation
- AUTO-008 Scheduled Maintenance
- AUTO-009 Repository Health Loop
- AUTO-010 Autonomous Builder

## Learning progression

Open Flow should move users through increasing levels of capability rather than defaulting to unrestricted automation:

```text
OBSERVE
   ↓
PLAN
   ↓
GUIDED
   ↓
ASSISTED
   ↓
AUTONOMOUS
```

A practical learner progression is:

```text
BEGINNER
   ↓
EXPLORER
   ↓
BUILDER
   ↓
VERIFIER
   ↓
REVIEWER
   ↓
MAINTAINER
   ↓
RESEARCHER
   ↓
AUTONOMOUS OPERATOR
```

## Cross-category composition

The categories are intentionally composable. Future workflow composition can combine small, inspectable workflows into objective-driven pipelines.

### Fix a bug

```text
EXPLORER → DEBUGGER → VERIFY → DOCS → GIT
```

### Secure a repository

```text
EXPLORER → SHIELD → VERIFY → BUILDER → GIT → RELEASE
```

### New-user onboarding

```text
START → EXPLORER → MENTOR → GIT → BUILDER → VERIFY
```

### Production readiness

```text
EXPLORER → PROJECT HEALTH → SHIELD → VERIFY → DOCS → RELEASE
```

## Design principles

1. **Free and open source.** Workflows are intended to be broadly reusable and inspectable.
2. **Learn by doing.** Workflows should teach users through real repository tasks.
3. **Evidence first.** Observations, inferences, hypotheses, and unknowns must remain distinguishable.
4. **Progressive autonomy.** Users should gain automation gradually through verified workflows.
5. **Small composable units.** Prefer reusable workflows over monolithic prompts.
6. **Git-native.** Workflow definitions, changes, tests, and history belong in the repository.
7. **Provider-friendly.** Avoid unnecessary dependence on a single AI vendor or runtime.
8. **Safety by contract.** Destructive actions, credentials, permissions, and network access must be explicitly bounded.
9. **Verification is mandatory.** Workflows should report what was actually tested or verified.
10. **AIPubs branded, community extensible.** AIPubs provides the open framework and taxonomy while contributors can add compatible workflows.

## Relationship to OWF

These categories are the human-facing AIPubs taxonomy. The Open Workflow Framework (OWF) remains the machine-facing specification and execution model.

```text
AIPubs Open Flow
      │
      ├── START
      ├── EXPLORER
      ├── MENTOR
      ├── BUILDER
      ├── DEBUGGER
      ├── VERIFY
      ├── SHIELD
      ├── DOCS
      ├── GIT
      ├── GITHUB
      ├── RELEASE
      ├── RESEARCH
      └── AUTONOMY
             │
             ▼
        OWF manifests
             │
             ▼
       Copilot CLI / agents
```

## Status

This catalog defines the initial AIPubs Open Flow taxonomy. The individual workflows will be implemented incrementally, tested, versioned, and documented as part of the OWF project.
