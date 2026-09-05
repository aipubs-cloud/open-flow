# OWF Glossary

## Agent
A role-oriented reasoning component responsible for a defined class of analysis or execution decisions.

## Capability
A permission or integration required to perform an operation, such as filesystem write, process execution, GitHub mutation, or network access.

## Evidence
An observation or verification artifact supporting a statement made by a workflow.

## Fact
A statement directly observed or independently verified.

## Hook
A lifecycle integration point that can inspect, gate, record, or react to workflow execution.

## Inference
A conclusion derived from available evidence but not directly observed.

## MCP
Model Context Protocol. In OWF it is treated as a capability boundary for external tools and services, not as an automatic trust boundary.

## Mode
The authority level under which a workflow operates: `observe`, `plan`, `guided`, `assisted`, or `autonomous`.

## Policy
The explicit rules governing allowed modes, capabilities, side effects, secrets, confirmation, and stop conditions.

## Result
The structured record of workflow status, evidence, verification, artifacts, and limitations.

## Skill
A reusable procedural capability that can be composed into multiple workflows.

## Workflow
A versioned composition defining an objective, inputs, outputs, capabilities, safety boundaries, and verification requirements.

## Unknown
A statement for which available evidence is insufficient to establish a conclusion.

## Hypothesis
A proposed explanation or claim that requires validation before it can be treated as fact.
