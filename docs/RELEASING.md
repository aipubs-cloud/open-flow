# Release Procedure

## Release goals

A release is a verified snapshot of OWF contracts and components. It should be reproducible from Git and understandable without private context.

## Pre-release checklist

- [ ] working tree and target branch are understood
- [ ] intended version is selected
- [ ] workflow IDs are stable
- [ ] schemas validate current examples
- [ ] test suite passes
- [ ] CI passes
- [ ] documentation matches behavior
- [ ] changelog is updated
- [ ] security-sensitive changes have been reviewed
- [ ] breaking changes are explicitly documented
- [ ] Git diff has been reviewed

## Versioning

OWF uses Semantic Versioning for public contracts:

- `MAJOR`: incompatible contract or behavioral changes
- `MINOR`: backward-compatible features
- `PATCH`: backward-compatible fixes and clarifications

A workflow can evolve independently of the repository release when its contract is explicitly versioned.

## Release sequence

```text
AUDIT -> TEST -> DIFF -> DOCUMENT -> VERSION -> REVIEW -> TAG -> PUBLISH
```

Do not create a release solely because CI is green. CI proves only the checks it actually executes.

## Release artifacts

At minimum, a release should provide:

- source commit/tag
- changelog entry
- version metadata
- test/verification status
- compatibility notes
- known limitations

## Rollback

Prefer reverting or selecting a known-good Git tag over editing a release artifact in place. If a published contract must be withdrawn, document the reason and compatibility impact.
