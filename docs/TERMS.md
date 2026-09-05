# Foundational Terms

OWF uses these terms consistently across manifests, documentation, tests, and reviews.

| Term | Contract meaning |
|---|---|
| Workflow | Versioned composition of an objective, steps, capabilities, safety rules, and verification. |
| Agent | Role-specific reasoning component. |
| Skill | Reusable procedural method. |
| Hook | Lifecycle extension point around workflow execution. |
| Capability | Explicit authority or integration needed for an operation. |
| Policy | Rules controlling modes, capabilities, side effects, secrets, and stop conditions. |
| Evidence | Observable or verified support for a claim. |
| Verification | A check that tests whether a stated condition actually holds. |
| Artifact | A file or structured output produced by a workflow. |
| Mode | The authority level governing execution behavior. |
| Host | The environment that actually executes tools and enforces permissions. |
| Composition | Combining workflows, agents, skills, and capabilities into a larger process. |
| Contract | A machine-readable or documented agreement about structure and behavior. |
| FACT | Directly observed or independently verified statement. |
| INFERENCE | Conclusion derived from evidence. |
| HYPOTHESIS | Claim requiring validation. |
| UNKNOWN | Claim for which available evidence is insufficient. |

These terms are intentionally narrower than informal AI-agent terminology. Precision is part of the project's engineering safety model.
