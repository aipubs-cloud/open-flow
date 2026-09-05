# Contributing to Open Workflow Framework

Thank you for contributing to Open Workflow Framework (OWF).

OWF is a Git-native collection of reusable workflows, agents, skills, hooks, schemas, and verification practices. Contributions should strengthen reproducibility, safety, composability, and usability.

## Development principles

1. Evidence before inference.
2. Small, reviewable changes over broad rewrites.
3. Every behavior change gets a test or an explicit justification.
4. Schemas and examples are public contracts and must remain synchronized.
5. Documentation describes observed behavior, not aspirations presented as facts.
6. Security-sensitive changes require explicit review.
7. Destructive or externally consequential behavior must be opt-in and bounded.

## Change workflow

Use:

```text
issue -> branch -> implementation -> tests -> diff review -> pull request -> review -> merge
```

Recommended branch names:

- `feat/<scope>`
- `fix/<scope>`
- `docs/<scope>`
- `test/<scope>`
- `chore/<scope>`
- `security/<scope>`

## Adding a workflow

A workflow should include:

- stable OWF identifier
- human-readable name and purpose
- version
- supported operating modes
- inputs and outputs
- safety boundaries
- required capabilities
- verification requirements
- explicit failure behavior
- references to agents and skills it composes
- tests or manifest validation

Do not add an executable behavior merely because a host appears to support it. Validate host-specific behavior first.

## Pull requests

A PR description should explain:

- what changed
- why it changed
- affected workflows/contracts
- tests executed and exact results
- security or permission implications
- remaining uncertainty
- related issues

Avoid mixing unrelated refactors into feature PRs.

## Commit messages

Prefer conventional, descriptive commits such as:

```text
feat(owf-003): add project health workflow
fix(owf-002): preserve filesystem scan errors
schema: tighten workflow output contract
```

## Reporting security issues

Do not disclose exploitable vulnerabilities in a public issue. Follow `SECURITY.md`.
