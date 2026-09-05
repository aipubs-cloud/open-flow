# OWF Operations

## Lifecycle

A workflow execution should move through explicit states:

```text
DISCOVERED -> PLANNED -> AUTHORIZED -> EXECUTING -> VERIFYING -> COMPLETE
                                  |                  |
                                  +-> BLOCKED       +-> FAILED
```

`COMPLETE` means the workflow's stated verification requirements were satisfied. It does not mean every broader project concern has been resolved.

## Audit record

Where the host permits, record:

- workflow ID/version
- mode
- input identifiers without secret values
- capabilities used
- commands or actions performed
- verification checks
- artifacts produced
- failures
- unresolved uncertainty

## Idempotence

Workflows that may be retried should define whether actions are idempotent. External writes should use stable identifiers or preflight checks when possible.

## Recovery

If verification fails:

1. stop dependent actions
2. preserve evidence
3. report the failure
4. identify the last known-good state
5. require an explicit recovery plan

Do not hide partial completion behind a success message.

## Observability

Telemetry should be minimal and non-secret. Prefer event metadata such as workflow ID, phase, status, duration, and verification outcome rather than raw user content or command output.
