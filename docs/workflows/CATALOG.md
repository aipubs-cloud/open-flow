# Workflow Catalog

**Inventory basis:** `registry/workflows.yaml` on `main`.

**Current registered count:** 31. Every entry below is currently registered with lifecycle status `active`. The maturity field is deliberately conservative and describes repository evidence, not product intent.

## Maturity vocabulary

- **Foundation executable:** dedicated implementation code and/or a meaningful test surface exists.
- **Protocol/learning implementation:** substantial instructional or workflow-specific protocol exists, but the workflow is not yet a complete standalone execution engine.
- **Manifest only:** a registered machine-readable workflow manifest exists; dedicated execution/tests/protocol are not yet evident in the current repository tree.
- **Composition primitive:** primarily orchestrates other workflows and therefore depends on resolver/composer maturity.

---

## Core OWF workflows

### OWF-001 — First Contact

- **Path:** `workflows/001-first-contact/workflow.yaml`
- **Version:** 0.1.0
- **Use:** The general Open Flow entry point. Establishes user intent/context and selects an appropriate workflow rather than assuming a technical task.
- **Best for:** A user who does not yet know which workflow they need.
- **Role:** Front-door routing/orientation primitive.
- **Composes toward:** START, EXPLORER, MENTOR, GIT, BUILD, VERIFY, and other category workflows.
- **Maturity:** Manifest-level core primitive.

### OWF-002 — Repository Explorer

- **Path:** `workflows/002-repository-explorer/workflow.yaml`
- **Version:** 0.1.1
- **Use:** Deterministically inspect a repository's structure, architecture indicators, candidate entry points, tests, CI, deployment hints, and documentation without executing application code.
- **Best for:** Establishing factual repository context before another workflow acts.
- **Implementation:** `collector.py`, `INSTRUCTION.md`, `src/owf002/`, and `tests/test_owf_002.py` provide the strongest dedicated executable workflow implementation currently in the repository.
- **Safety:** Observe/read-only with respect to the inspected repository; no application execution, dependency installation, or network discovery.
- **Feeds:** START-003 and future explorer/mentor/builder workflows.
- **Maturity:** **Foundation executable**.

### OWF-003 — Project Doctor

- **Path:** `workflows/003-project-doctor/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Diagnose project health, structure, configuration, and likely engineering problems before making changes.
- **Best for:** A project that feels broken, confusing, incomplete, or unhealthy.
- **Natural composition:** OWF-002 → OWF-003 → DEBUGGER/VERIFY/SHIELD/DOCS.
- **Maturity:** Manifest only.

### OWF-004 — Guided Bug Fix

- **Path:** `workflows/004-guided-bug-fix/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Guide reproduction, diagnosis, implementation of a bounded fix, and verification.
- **Best for:** A known bug where the learner wants help fixing it rather than autonomous remediation.
- **Natural composition:** EXPLORER → DEBUGGER → VERIFY → GIT/GITHUB.
- **Maturity:** Manifest only.

### OWF-005 — Test Builder

- **Path:** `workflows/005-test-builder/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Create or improve tests around an existing behavior or change.
- **Best for:** Turning an observed behavior or bug into repeatable regression protection.
- **Natural composition:** BUILD/DEBUG → OWF-005 → VERIFY.
- **Maturity:** Manifest only.

### OWF-006 — Security Auditor

- **Path:** `workflows/006-security-auditor/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Inspect a repository for evidence-based security concerns and produce findings without fabricating vulnerabilities.
- **Best for:** Security orientation, pre-release review, or investigation of suspicious configuration.
- **Natural composition:** OWF-002 → OWF-006 → VERIFY/BUILD/DOCS.
- **Maturity:** Manifest only; the repository also contains a related `security-audit` Copilot skill.

### OWF-007 — Documentation Engineer

- **Path:** `workflows/007-documentation-engineer/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Plan, create, improve, or audit project documentation.
- **Best for:** README, guides, API/CLI documentation, architecture explanations, and documentation gaps.
- **Natural composition:** EXPLORER → DOCS → VERIFY/GITHUB.
- **Maturity:** Manifest only; a general documentation Copilot skill exists.

### OWF-008 — GitHub Maintainer

- **Path:** `workflows/008-github-maintainer/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Maintain project-level GitHub work such as Issues, Pull Requests, reviews, and repository hygiene.
- **Best for:** Maintainer operations that require explicit GitHub-side effects and policy checks.
- **Safety:** Must inherit host authority and confirmation rules for writes.
- **Natural composition:** GITHUB workflows → maintenance/release.
- **Maturity:** Manifest only; GitHub operations remain a high-authority boundary.

### OWF-009 — Research Lab

- **Path:** `workflows/009-research-lab/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Structure reproducible technical investigation, experiments, evidence collection, and research outputs.
- **Best for:** Technical research rather than routine application maintenance.
- **Natural composition:** EXPLORER → RESEARCH → VERIFY → DOCS/RELEASE.
- **Maturity:** Manifest only.

### OWF-010 — Autonomous Builder

- **Path:** `workflows/010-autonomous-builder/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Bounded autonomous implementation of a defined task under explicit safety policy.
- **Best for:** Advanced users who have already established requirements, scope, and authorization.
- **Safety:** This is an autonomy boundary, not a blanket permission to modify anything. Composition must preserve child and host restrictions.
- **Natural composition:** PLAN/BUILD → VERIFY → REVIEW → GITHUB/RELEASE.
- **Maturity:** Manifest only.

### OWF-011 — Workflow Composer

- **Path:** `workflows/011-workflow-composer/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Select and compose smaller workflows into a coherent objective-driven pipeline.
- **Best for:** Multi-step journeys where state and artifacts must pass between workflows.
- **Implementation relationship:** `core/composer.py` and `.copilot/skills/workflow-resolver/` are the relevant infrastructure.
- **Critical dependency:** End-to-end resolver/composer contract testing is tracked by Issue #28, while safety monotonicity is tracked by Issue #36.
- **Maturity:** **Composition primitive**.

---

## AIPUBS-START: beginner entry and graduation

### AIPUBS-START-001 — What Is GitHub?

- **Path:** `workflows/AIPUBS-START/001-what-is-github/workflow.yaml`
- **Version:** 0.1.1
- **Use:** Teach the Git/GitHub mental model, repository, commits, branches, Issues, Pull Requests, testing, Actions, deployment, and maintenance.
- **Best for:** Someone who knows little or nothing about GitHub.
- **Implementation:** `INSTRUCTIONS.md` and `inspect_primitives.py` provide a substantial interactive/evidence-grounded protocol.
- **Safety:** Primarily observational; no unsolicited repository/GitHub writes.
- **Next:** Usually START-002, START-003, or GIT-001 depending on learner state.
- **Maturity:** **Protocol/learning implementation**.

### AIPUBS-START-002 — Create Your First Repository

- **Path:** `workflows/AIPUBS-START/002-create-repository/workflow.yaml`
- **Version:** 0.1.1
- **Use:** Guide a beginner through creating their first repository and establishing a safe project starting point.
- **Best for:** A learner who has completed GitHub orientation but does not yet have a repository.
- **Implementation:** `INSTRUCTIONS.md` plus repository-creation infrastructure in `core/repository_creator.py` and tests provide a meaningful implementation boundary.
- **Safety:** Creation is consequential and therefore must remain confirmation/policy gated.
- **Next:** START-003 or GIT-001 after a repository exists.
- **Maturity:** **Protocol/learning implementation**.

### AIPUBS-START-003 — Explore a Repository

- **Path:** `workflows/AIPUBS-START/003-explore-repository/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Turn raw repository evidence into a beginner-readable repository tour and durable learning artifacts.
- **Best for:** A learner who has a repository but does not understand its structure or execution model.
- **Implementation status:** The first rich implementation slice is currently proposed in **PR #56**. It adds repository-map, architecture-map, execution-map, learning-summary, and result contracts plus an interactive mentor protocol.
- **Critical relationship:** It should consume OWF-002 evidence, not create a second repository scanner.
- **Current gate:** Canonical OWF-002/START-003 identity and registry reconciliation is tracked by #49; broader fixtures and Journey Orchestrator tests remain.
- **Maturity:** **Protocol/learning implementation, in active PR development**.

### AIPUBS-START-010 — Complete Your First Open-Source Contribution

- **Path:** `workflows/AIPUBS-START/010-first-open-source-contribution/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Capstone journey from finding a suitable issue through exploration, branch, implementation, testing, Pull Request, review, update, and merge.
- **Best for:** A learner ready to become a first-time open-source contributor.
- **Natural composition:** START-003 → GIT-001/002 → GITHUB-001/002/003/004/005 → VERIFY.
- **Maturity:** Manifest only. The implementation issue is #21.

---

## AIPUBS-GIT

### AIPUBS-GIT-001 — Git Basics

- **Path:** `workflows/AIPUBS-GIT/001-git-basics/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Teach working tree → staging area → commit → history through one controlled change.
- **Best for:** Beginners who understand GitHub conceptually and need practical Git state literacy.
- **Safety:** Controlled write; no push, force push, reset, clean, or unrelated staging. Writes require confirmation.
- **Next:** GIT-002 or BUILD-001.
- **Maturity:** Manifest only in the current tree; the detailed design exists in Issue #5.

### AIPUBS-GIT-002 — Your First Branch

- **Path:** `workflows/AIPUBS-GIT/002-first-branch/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Teach feature branches through a safe, real change and verification of branch state.
- **Best for:** A learner who understands commits and is ready to separate work from the primary branch.
- **Safety:** Guided branch creation; no force push or destructive branch operations.
- **Next:** BUILD-001 or GITHUB-001/002.
- **Maturity:** Manifest only; implementation issue #6 remains open.

---

## AIPUBS-GITHUB: collaboration and repository governance

### AIPUBS-GITHUB-001 — Your First Issue

- **Path:** `workflows/AIPUBS-GITHUB/001-first-issue/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Turn an idea, task, bug, or improvement into a useful tracked GitHub Issue.
- **Best for:** Converting an unstructured goal into actionable project work.
- **Writes:** Creates a real Issue, so GitHub authority and confirmation matter.
- **Next:** BUILD-001 or relevant specialist workflow.
- **Maturity:** Manifest only; implementation issue #7.

### AIPUBS-GITHUB-002 — Your First Pull Request

- **Path:** `workflows/AIPUBS-GITHUB/002-first-pull-request/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Turn a branch and verified changes into a reviewable Pull Request.
- **Best for:** First-time contributors learning how code becomes a proposed integration.
- **Natural composition:** GIT-002 → BUILD-001 → VERIFY-001 → GITHUB-002.
- **Writes:** Opens a real PR and therefore crosses into GitHub-side effects.
- **Maturity:** Manifest only; implementation issue #9.

### AIPUBS-GITHUB-003 — Review Your Own Pull Request

- **Path:** `workflows/AIPUBS-GITHUB/003-self-review/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Inspect requirements, diff, tests, documentation, security, and scope before requesting review.
- **Best for:** Preventing avoidable review failures and teaching readiness assessment.
- **Output:** Explicit readiness result with remaining concerns.
- **Maturity:** Manifest only; implementation issue #11.

### AIPUBS-GITHUB-004 — Respond to Review Feedback

- **Path:** `workflows/AIPUBS-GITHUB/004-review-feedback/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Interpret reviewer feedback, clarify ambiguity, make requested changes, test them, and respond.
- **Best for:** Collaborative iteration after a Pull Request review.
- **Natural composition:** GITHUB-003 → BUILD/VERIFY → GITHUB-004.
- **Maturity:** Manifest only; implementation issue #12.

### AIPUBS-GITHUB-005 — Merge Your First Pull Request

- **Path:** `workflows/AIPUBS-GITHUB/005-first-merge/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Teach the final PR lifecycle: checks, review, approval, merge, and return to the main development line.
- **Best for:** A learner whose PR is already ready for integration.
- **Safety:** Merge is consequential and must respect repository policy and required checks.
- **Maturity:** Manifest only; implementation issue #13.

---

## AIPUBS-BUILD

### AIPUBS-BUILD-001 — Build Your First Change

- **Path:** `workflows/AIPUBS-BUILD/001-first-change/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Take a tracked task through understanding, repository exploration, planning, branch creation, implementation, and testing.
- **Best for:** A learner ready to make a real project change.
- **Natural composition:** GITHUB-001 → START/EXPLORER → GIT-002 → BUILD-001 → VERIFY-001.
- **Safety:** Guided implementation should require explicit write authorization and preserve scope.
- **Maturity:** Manifest only; implementation issue #8.

---

## AIPUBS-VERIFY

### AIPUBS-VERIFY-001 — Does My Code Actually Work?

- **Path:** `workflows/AIPUBS-VERIFY/001-first-test/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Discover the repository's actual testing system, explain it, run appropriate checks, diagnose failures, and verify behavior.
- **Best for:** Learners who need to replace "I think it works" with observed verification.
- **Key rule:** Never assume a testing framework that was not observed.
- **Natural composition:** BUILD/DEBUG → VERIFY-001 → GITHUB-002.
- **Maturity:** Manifest only; implementation issue #10.

### AIPUBS-VERIFY-002 — Meet GitHub Actions

- **Path:** `workflows/AIPUBS-VERIFY/002-github-actions/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Discover actual GitHub Actions workflows, explain triggers/jobs, and teach how repository automation validates changes.
- **Best for:** Understanding CI and automation after learning local testing.
- **Key rule:** If no Actions workflow is observed, say so rather than inventing one.
- **Maturity:** Manifest only; implementation issue #14.

---

## AIPUBS-RELEASE

### AIPUBS-RELEASE-001 — Ship Your First Release

- **Path:** `workflows/AIPUBS-RELEASE/001-first-release/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Move a verified change through version analysis, changelog preparation, tag preparation, release creation, and post-release verification.
- **Best for:** A project that has a verified change ready to ship.
- **Natural composition:** VERIFY → RELEASE → DEPLOY.
- **Key rule:** Do not assume a package ecosystem; inspect actual project conventions.
- **Maturity:** Manifest only; implementation issue #15.

---

## AIPUBS-DEPLOY

### AIPUBS-DEPLOY-001 — Deploy Your First Website

- **Path:** `workflows/AIPUBS-DEPLOY/001-first-deployment/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Discover the project's real build/deployment configuration, validate prerequisites, and guide a safe deployment.
- **Best for:** A verified project ready to become a live application/site.
- **Key rule:** Provider-neutral. Never guess hosting infrastructure.
- **Natural composition:** BUILD/VERIFY → RELEASE → DEPLOY → OPERATE.
- **Maturity:** Manifest only; implementation issue #16.

---

## AIPUBS-OPERATE

### AIPUBS-OPERATE-001 — What Happens After Deployment?

- **Path:** `workflows/AIPUBS-OPERATE/001-software-maintenance/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Teach ongoing maintenance, monitoring, dependency updates, security work, bug fixing, and repeated release cycles.
- **Best for:** Learners who think deployment is the finish line.
- **Key rule:** Use observed repository/operational capabilities and do not invent infrastructure.
- **Natural composition:** DEPLOY → OPERATE → VERIFY/SHIELD/RELEASE.
- **Maturity:** Manifest only; implementation issue #17.

---

## AIPUBS-SHIELD

### AIPUBS-SHIELD-001 — Security 101

- **Path:** `workflows/AIPUBS-SHIELD/001-security-basics/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Teach repository security fundamentals including secrets, `.env` handling, dependency risk, Actions permissions, and insecure configuration.
- **Best for:** Beginners learning what should and should not enter a repository.
- **Key rule:** Findings must be evidence-based and uncertainty must be explicit.
- **Natural composition:** START/EXPLORER → SHIELD → VERIFY → BUILD remediation.
- **Maturity:** Manifest only; implementation issue #18. A related security-audit skill exists.

---

## AIPUBS-MENTOR

### AIPUBS-MENTOR-001 — Ask AI to Explain Your Code

- **Path:** `workflows/AIPUBS-MENTOR/001-explain-my-code/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Explain a file or function, including purpose, inputs, outputs, dependencies, risks, examples, and a small exercise.
- **Best for:** Learning from existing code instead of asking AI to replace understanding with generated code.
- **Natural composition:** START-003/EXPLORER → MENTOR-001.
- **Maturity:** Manifest only; implementation issue #19.

### AIPUBS-MENTOR-002 — Teach Me While I Code

- **Path:** `workflows/AIPUBS-MENTOR/002-teach-me-while-i-code/workflow.yaml`
- **Version:** 0.1.0
- **Use:** Combine planning, explanation, implementation, testing, verification, and teach-back into one adaptive learning loop.
- **Best for:** Users who want AI assistance without losing the learning process.
- **Natural composition:** Any BUILD/DEBUG/VERIFY journey.
- **Maturity:** Manifest only; implementation issue #20.

---

# Cross-workflow use patterns

## New user

```text
OWF-001
  ↓
START-001
  ↓
START-002 (if no repository)
  ↓
START-003 (if repository exists)
  ↓
GIT-001
  ↓
GIT-002
```

## Make and submit a change

```text
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
GITHUB-004 (if feedback)
  ↓
GITHUB-005
```

## Fix a bug safely

```text
OWF-002
  ↓
OWF-003 / OWF-004
  ↓
OWF-005 or VERIFY-001
  ↓
GITHUB-002
```

## Secure a repository

```text
OWF-002
  ↓
OWF-006 / SHIELD-001
  ↓
VERIFY
  ↓
BUILD remediation
  ↓
REVIEW
```

## Ship software

```text
BUILD
  ↓
VERIFY
  ↓
RELEASE
  ↓
DEPLOY
  ↓
OPERATE
```

## Learn while working

```text
OWF-002
  ↓
MENTOR-001 / MENTOR-002
  ↕
BUILD / DEBUG / VERIFY
```

# Current architectural warning

The repository has two identity/layout systems that must be kept deliberately related:

1. Numeric core workflows such as `workflows/002-repository-explorer` representing OWF primitives.
2. AIPUBS learner workflows such as `workflows/AIPUBS-START/003-explore-repository` representing human-facing curriculum experiences.

This is intentional only if the relationship is explicit. **OWF-002 and START-003 must not accidentally become two competing repository scanners.** Issue #49 exists to establish the canonical identity, alias, path, registry, and composition relationship.

# What this catalog does not claim

- A registered manifest is not proof of a complete executable implementation.
- A deployment manifest is not proof of a live deployment.
- A candidate entry point is not proof that the application successfully runs.
- Presence of tests is not proof that tests pass.
- Presence of GitHub Actions files is not proof that a workflow has successfully executed.
- An AI inference is not an observed repository fact.

Those distinctions are central to Open Flow's evidence-first design.
