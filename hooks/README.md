# OWF Hooks

Hooks are optional lifecycle integrations around workflow execution.

OWF v0.1 defines the conceptual hook classes without requiring a custom runtime:

- `pre-command`: inspect or gate a proposed command
- `post-command`: record execution outcome
- `safety`: enforce repository policy before consequential operations
- `telemetry`: emit non-secret workflow events

Hook implementations must be fail-safe, must not exfiltrate secrets, and must document whether they can modify state.

Native Copilot CLI hook configuration should be added only when validated against the installed CLI schema. This directory is intentionally a Git-native extension boundary, not an invented runtime contract.
