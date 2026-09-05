# OWF MCP Profiles

MCP is the capability extension boundary for workflows that need external tools or project services.

Suggested profile families:

- `github/`
- `filesystem/`
- `research/`
- `project-memory/`

A profile should declare its purpose, required capabilities, trust assumptions, data boundaries, and safety mode.

OWF does not ship a custom MCP server in v0.1. Native MCP configuration should be represented using the host environment's validated configuration format rather than an invented OWF-specific protocol.
