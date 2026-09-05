# OWF Foundation Acceptance Criteria

This document defines what the repository foundation must establish before higher-level workflows are treated as dependable building blocks.

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

## Contracts

- [x] workflow schema
- [x] workflow registry schema
- [x] agent schema
- [x] skill schema
- [x] policy schema
- [x] hook schema
- [x] workflow result schema

## Verification

- [x] deterministic repository collector tests
- [x] canonical workflow fixture
- [x] result fixture
- [x] schema validation dependency
- [x] CI package installation
- [x] CI test execution
- [x] CI workflow validation

## Security baseline

- [x] least-capability guidance
- [x] secret handling rules
- [x] explicit destructive-operation policy
- [x] autonomous-mode boundaries
- [x] fail-safe guidance
- [x] distinction between repository instructions and real host enforcement

## Remaining foundation work

The next hardening pass should address implementation-level concerns identified during review of OWF-002, including edge-case tests, precise depth semantics, formatter coverage, and deeper survey-schema validation.

The purpose of this checklist is not to claim that OWF is secure or production-complete. It establishes a transparent baseline against which subsequent work can be measured.
