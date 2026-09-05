# Compatibility Policy

OWF has three compatibility surfaces:

1. **Workflow contracts**: IDs, versions, inputs, outputs, capabilities, modes, and safety semantics.
2. **Host integrations**: Copilot CLI, GitHub Actions, MCP, and other execution environments.
3. **Artifacts**: structured survey, result, and report formats.

## Contract compatibility

Backward-compatible additions should not invalidate existing valid documents. Changes that alter required fields, output meaning, permissions, or safety semantics require explicit versioning and migration guidance.

## Host compatibility

OWF does not assume that a host's configuration syntax is stable. Host-specific integrations should identify the validated host version or capability and should be tested against the actual interface before being presented as supported.

## Artifact compatibility

Schema identifiers and versions are part of the artifact contract. Consumers should reject unknown major versions rather than guessing their meaning.

## Unsupported behavior

When a host feature is unavailable, OWF should report the limitation instead of silently emulating a capability with different safety or semantics.
