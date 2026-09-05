---
name: workflow-resolver
description: Resolve user intent into OWF workflows, artifact bindings, safety gates, and a deterministic execution graph.
---

# Workflow Resolver

Use this skill when a request spans multiple OWF workflows.

## Resolution procedure

1. Read the registered workflow manifests under `workflows/`.
2. Select only workflows that contribute directly to the objective.
3. Treat each workflow's `inputs` and `outputs` as typed handoff contracts.
4. For each input, bind the nearest compatible prior output with the form `S<n>.<artifact>`.
5. If a required input has no producer, classify it as an external input and keep it explicit.
6. Reject cycles and impossible ordering.
7. Compute the mode transition between adjacent executable steps.
8. If the next step is more privileged and enters an active mode, create a `manual_approval` gate before it.
9. If a workflow modifies files, require a gate unless the immediately preceding approved gate authorizes that modification class.
10. Emit a deterministic graph. Same manifests, sequence, and max mode must produce the same graph.

## Safety invariant

`effective_mode(step) <= max_mode` for every step.

A prior read-only step never grants write authority to a later step. Approval is an explicit pipeline state, not an inferred side effect of an earlier observation.

## Copilot handoff

After graph approval, hand off independent specialist nodes to custom agents/subagents where useful. Keep sequential artifact dependencies sequential. Use Copilot CLI Plan mode before the first write-capable stage and rely on repository `preToolUse` hooks to enforce the gate at tool execution time.
