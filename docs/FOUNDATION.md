# OWF Foundation Acceptance Criteria

This document defines what the repository foundation must establish before higher-level workflows are treated as dependable building blocks.

A checked item means the repository contract or implementation is present. It does **not** by itself mean that the current branch has passed CI or independent review.

## Repository hygiene

- [x] standard ignore rules
- [x] contribution policy
- [x] security policy
- [x] community conduct policy
- [x] changelog
- [x] editor configuration
- [x] repeatable development commands

## Architecture

- [x] workflow/agent/skill separation
- [x] capability boundary
- [x] safety boundary
- [x] evidence model
- [x] verification model
- [x] host integration boundary

## Contracts established

- [x] workflow schema
- [x] workflow registry schema
- [x] agent schema
- [x] skill schema
- [x] policy schema
- [x] hook schema
- [x] workflow result schema
- [x] positive and negative contract coverage for public schemas

## Verification evidence

- [x] deterministic repository collector tests are present
- [x] canonical workflow fixture is present
- [x] result fixture is present
- [x] schema validation dependency is declared
- [ ] current PR head has a successful CI run
- [ ] current PR head has an independently recorded verification result

## Security baseline

- [x] least-capability guidance
- [x] secret handling rules
- [x] explicit destructive-operation policy
- [x] autonomous-mode boundaries
- [x] fail-safe guidance
- [x] distinction between repository instructions and real host enforcement
- [x] third-party GitHub Actions are pinned to immutable commit SHAs
- [x] CI dependency trust model is documented

## Deferred hardening

The foundation is intentionally not represented as production-complete. Further work may address deeper survey-schema constraints, broader integration coverage, dependency lock/hash enforcement, and implementation-specific edge cases.

The authoritative status is the combination of this checklist, CI evidence, test results, and review discussion. Unverified claims must remain explicitly marked as such.
