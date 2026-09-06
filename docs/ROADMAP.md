# Open Flow Engineering Roadmap

This roadmap converts the current repository state into an ordered implementation program. It is derived from the canonical workflow registry, foundation acceptance criteria, CI configuration, and open development work.

## Current baseline

The registry currently declares 31 workflows. Registration is not equivalent to implementation readiness. The project therefore needs to finish the infrastructure that makes workflow identity, contracts, execution, safety, testing, orchestration, and readiness measurable.

The foundation records repository contracts and deterministic collector tests, but explicitly leaves current-head CI evidence and independent verification as open gates.

## Priority sequence

### P0 — Authoritative foundation

1. **#26 — Canonical workflow registry and reference integrity**
2. **#49 — Reconcile OWF-002 / START-003 identity and canonical paths**
3. **#27 — Schema-driven workflow discovery/validation**

### P1 — Executable workflow contracts

4. **#30 — Deterministic execution and dry-run contract**
5. **#28 — Composer/resolver contract tests**
6. **#36 — Safety monotonicity**
7. **#32 — Versioning and compatibility policy**
8. **#41 — Learner artifact contracts**

### P2 — Reliability and verification

9. **#59 — Deterministic test-fixture matrix**
10. **#33 — Adversarial safety/prompt-injection regression suite**
11. **#58 — Workflow maturity/readiness gates**
12. **#31 — Documentation/schema link integrity**
13. **#61 — Self-updating workflow catalog/registry consistency**

### P3 — Learner orchestration

14. **#60 — Journey Orchestrator learner-state handoff**
15. Complete **AIPUBS-START-003 / PR #56** after registry, routing, fixture, orchestration, and CI gates pass.
16. Complete **AIPUBS-START-001** against the same contracts.
17. Add deterministic end-to-end beginner journey fixtures.

### P4 — Workflow family expansion

Only after the foundation is stable should implementation proceed systematically through START, GIT, GITHUB, BUILD, VERIFY, RELEASE, DEPLOY, OPERATE, SHIELD, and MENTOR families.

## Definition of a completed workflow

A workflow is not considered production-ready merely because `workflow.yaml` exists. At minimum it should have canonical registry identity, valid manifest and schema contracts, explicit inputs/outputs and capability/safety boundaries, deterministic positive and negative fixtures, execution/result semantics where applicable, composition/routing contracts where applicable, documentation, passing CI, and an explicit maturity/readiness state.

## PR policy

All implementation work must occur on a dedicated branch and enter `main` through a pull request. Documentation and roadmap changes must not become an alternative path around engineering gates.
