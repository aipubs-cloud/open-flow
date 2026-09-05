# Manifest Authoring Standard

A workflow manifest is the smallest durable description of a workflow.

## Required identity

```yaml
id: OWF-123
name: stable-name
version: 0.1.0
purpose: One sentence describing the objective.
```

## Required operational meaning

A useful manifest should identify:

- supported modes
- capabilities
- inputs
- ordered steps
- outputs
- safety rules
- verification requirements

## Step design

Each step should have a stable local ID and a plain-language action. When composition is used, identify the agent or skill responsible for the step.

A step should not conceal a materially different capability from the workflow declaration.

## Input design

Inputs should be explicit. Avoid magic discovery when an operation depends on user intent. Treat paths, commands, URLs, repository names, and external content as untrusted input unless the host establishes trust.

## Output design

Prefer structured output for machine consumption and human-readable output for explanation. When an output has a schema, reference the schema directly.

## Safety design

State what the workflow cannot do, not only what it intends to do. A declaration such as `filesystem_write: false` is more useful than a prose statement that the workflow is "safe".

## Verification design

Verification should be observable and falsifiable. "Looks correct" is not a sufficient verification step for a machine-readable contract.
