# Schema Evolution Policy

OWF schemas are public interfaces between workflows, hosts, tests, and downstream consumers.

## Required properties of a schema

Every public schema should have:

- a `$schema` declaration
- a stable `$id`
- a descriptive title
- explicit required properties
- constrained enums where the vocabulary is intentionally closed
- meaningful types and ranges
- examples or fixtures when practical

## Evolution rules

### Patch-compatible

Clarifications, documentation, and constraints that cannot invalidate an existing valid document may be patch-level changes.

### Minor-compatible

New optional properties, new workflow capabilities, or additive result metadata may be minor-level changes when consumers can safely ignore them.

### Breaking

Changing the meaning of an existing property, changing its type, removing supported values, or making an optional property required is breaking and should require a major contract version.

## Consumer behavior

Consumers should fail clearly on unsupported major versions. They should not silently reinterpret unknown fields or enum values.

## Validation

Every schema change should update at least one positive fixture and one relevant negative test. CI should validate representative documents against the schema.
