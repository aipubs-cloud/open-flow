# OWF Foundation Map

```text
open-flow/
├── .copilot/                 Host-facing agent, skill, and instruction layer
├── .github/                  CI and contribution workflow layer
├── docs/                     Human-readable architecture and governance contracts
├── examples/                 Safe canonical contract fixtures
├── hooks/                    Hook integration boundary
├── mcp/                      MCP capability boundary
├── schemas/                  Machine-readable contracts
├── src/owf002/               Executable OWF-002 collector
├── tests/                    Regression and contract verification
├── workflows/                Versioned OWF workflow definitions
├── workflow.yaml             Root workflow registry
├── pyproject.toml            Python package/build metadata
├── Makefile                  Standard local commands
├── CHANGELOG.md              Release history
├── CONTRIBUTING.md           Contribution rules
├── SECURITY.md               Security policy
└── LICENSE                   Open-source license
```

## Dependency direction

The intended dependency direction is:

```text
schemas / contracts
       ^
       |
workflows
       ^
       |
agents + skills
       ^
       |
host integrations
       ^
       |
execution environment
```

Core contracts should not depend on one specific host implementation. Host integrations should adapt to the contracts rather than redefine them.
