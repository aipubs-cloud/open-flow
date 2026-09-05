# OWF Testing Strategy

OWF testing is layered so that a green test suite has a clear meaning.

## Unit tests

Test individual collectors, parsers, formatters, and policy helpers with controlled inputs.

## Contract tests

Validate representative documents against their JSON/YAML contracts. Include both valid and intentionally invalid fixtures.

## Workflow tests

Verify every registered workflow has a manifest, stable identifier, supported mode, and required contract fields.

## Determinism tests

Run deterministic components more than once against the same controlled fixture and compare structured outputs. Exclude intentionally variable fields from equality or normalize them explicitly.

## Negative tests

Negative tests are mandatory for safety-sensitive code. Examples:

- invalid target path
- unsupported mode
- missing required capability
- malformed manifest
- invalid schema status
- failed verification

## Integration tests

Integration tests may exercise real GitHub, MCP, or host interfaces only when credentials and side effects are deliberately controlled. Tests must not mutate production resources by default.

## Test result language

Use precise language:

- `PASS`: the named check actually executed and succeeded.
- `FAIL`: the named check executed and failed.
- `SKIPPED`: the check did not execute and the reason is recorded.
- `UNVERIFIED`: insufficient evidence to establish the claim.

Never turn a skipped or unverified check into a pass merely because the expected behavior appears obvious.
