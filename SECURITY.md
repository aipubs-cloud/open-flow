# Security Policy

## Scope

OWF is a workflow specification and repository of composable instructions, agents, skills, schemas, and supporting tooling. OWF is not itself a security boundary. Host permissions, repository policy, credentials, and external services remain authoritative.

## Security principles

- Default to read-only observation.
- Minimize permissions and capabilities.
- Never expose secrets in workflow output, telemetry, fixtures, or logs.
- Treat external input as untrusted.
- Require evidence for security findings.
- Keep autonomous behavior bounded by explicit policy.
- Prefer fail-safe behavior for safety gates.
- Do not silently escalate privileges.

## Reporting a vulnerability

Please do not publish sensitive vulnerability details in a public issue. Use the repository owner's configured GitHub private vulnerability reporting or security contact when available.

Include:

- affected file, workflow, or component
- reproduction steps
- impact
- prerequisites
- evidence
- suggested remediation, if known

Do not include live credentials, private keys, personal data, or other secrets in a report.

## Security review expectations

Changes involving command execution, network access, credentials, permissions, hooks, MCP capabilities, autonomous operation, or CI should receive explicit security review.

A security review must distinguish confirmed findings from hypotheses and should document confidence and verification status.
