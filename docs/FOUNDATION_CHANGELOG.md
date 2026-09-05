# Foundation Hardening Change Set

This change set establishes the repository-level engineering foundation around the existing OWF-002 implementation.

## Added

- governance policies
- contribution guidance
- security guidance
- release and compatibility policy
- architecture and safety model
- testing strategy
- terminology and manifest standards
- schema catalog
- canonical workflow, policy, and result examples
- CI package installation and validation
- issue and pull-request templates
- standard development commands
- Python module entry point

## Contract impact

The workflow schema is tightened from an open-ended object to an explicit contract while retaining the existing required identity and step fields used by the v0.1 workflows.

## Verification intent

The branch adds automated contract tests and keeps the existing workflow validation harness. The remaining implementation hardening of OWF-002 is intentionally tracked separately so this foundation change remains reviewable.
