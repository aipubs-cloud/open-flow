# OWF Engineering Principles

## 1. Understand before modifying

Repository context, current behavior, and constraints come before implementation.

## 2. Evidence before conclusions

Observed facts and verified results must remain distinguishable from inference and hypothesis.

## 3. Least capability

A workflow should request only the authority it needs. Read access is not write access; local write access is not remote write access.

## 4. Verification is part of the feature

A change without a meaningful verification path is incomplete when the behavior is testable.

## 5. Explicit uncertainty

Unknown information should remain unknown until evidence resolves it.

## 6. Reversibility

Prefer changes that can be inspected, reverted, or safely retried.

## 7. Human control for consequence

The greater the external consequence, the stronger the confirmation and review requirements should be.

## 8. Host truth

Repository instructions describe intended behavior. The execution host enforces actual permissions and isolation.

## 9. Public contracts deserve discipline

Schemas, workflow IDs, modes, and result semantics should be treated as APIs.

## 10. Small composable primitives

Prefer narrowly defined agents, skills, and workflows that can be composed rather than a single opaque mega-workflow.
