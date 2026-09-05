# Host Integration Boundaries

OWF is designed to compose with host environments rather than replace them.

## GitHub Copilot CLI

Copilot CLI is an execution host for instructions, agents, skills, tools, and repository context. OWF repository files should describe validated behavior and avoid claiming host features that have not been tested against the target CLI version.

## GitHub Actions

GitHub Actions provides CI enforcement. Workflow permissions should use least privilege. Pull-request jobs must be treated as untrusted with respect to repository-controlled inputs where applicable.

## MCP

MCP provides an external capability interface. Each integration should document:

- server identity
- capabilities exposed
- read/write behavior
- trust assumptions
- data sent to the server
- credentials required
- failure behavior

## Git

Git provides the primary audit trail for repository changes. Prefer branches and pull requests for material changes. Do not rewrite shared history unless explicitly authorized.

## Host-independent principle

OWF manifests should remain meaningful even if the execution host changes. Provider-specific configuration belongs in integration documentation or adapter files rather than being confused with the core workflow contract.
