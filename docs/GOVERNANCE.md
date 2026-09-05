# OWF Governance

## Maintainer responsibility

Maintainers are responsible for preserving the integrity of public contracts, reviewing security-sensitive changes, and keeping documentation aligned with implementation.

## Decision principles

When proposals conflict, prioritize:

1. safety and least privilege
2. correctness and evidence
3. reproducibility
4. backward compatibility
5. simplicity
6. usability

## Contract changes

Changes to workflow IDs, schema semantics, operating modes, capability requirements, or safety behavior require explicit review and changelog documentation.

## Experimental work

Experimental features should be clearly labeled and should not be represented as stable guarantees. A prototype can be valuable without pretending to be production-ready.

## Deprecation

A deprecated contract should identify:

- what is deprecated
- replacement, if any
- first deprecated version
- planned removal version when known
- migration guidance

## Release authority

A release should be created only after the release checklist in `docs/RELEASING.md` is satisfied. CI success alone is not sufficient evidence of release readiness.
