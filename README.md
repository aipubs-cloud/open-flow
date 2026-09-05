# Open Flow

Open Flow is an open-source workflow ecosystem for repository intelligence, AI-assisted development, learning, verification, and bounded automation.

## OWF-002: Repository Explorer

OWF-002 is the first evidence-collection workflow. It performs a deterministic, read-only survey of a repository and emits either Markdown for human/LLM context or JSON for downstream workflows.

### Guarantees

- Python 3.8+ standard library only
- Repository analysis does not modify repository files
- Common build, dependency, cache, IDE, and VCS directories are excluded
- Results contain an explicit schema version
- Filesystem failures are reported rather than silently treated as absence
- Output is deterministic for a stable filesystem state

### Usage

From the repository root:

```bash
PYTHONPATH=src python -m owf002.repo_explorer .
PYTHONPATH=src python -m owf002.repo_explorer . --format json -o survey.json
PYTHONPATH=src python -m owf002.repo_explorer /path/to/repo -o survey.md
```

### Workflow contract

```text
Repository
   |
   v
OWF-002 Explorer
   |
   +--> survey.json  (machine contract)
   +--> survey.md    (LLM/human context)
   |
   v
OWF-003+ downstream analysis
```

OWF-002 reports evidence. It does not claim to understand repository intent, code quality, security posture, or correctness. Those concerns belong to downstream workflows.

## Planned workflow family

```text
OWF-001 Workflow Bootstrap
OWF-002 Repository Explorer
OWF-003 Repository Mapper
OWF-004 Architecture Analyzer
OWF-005 Execution Analyzer
OWF-006 Quality Analyzer
OWF-007 Deployment Analyzer
OWF-008 Repository Synthesizer
OWF-009 Learning Journey
OWF-010 Autonomous Builder
```

Each workflow should have a versioned contract, deterministic tests where practical, explicit safety boundaries, and machine-readable outputs.
