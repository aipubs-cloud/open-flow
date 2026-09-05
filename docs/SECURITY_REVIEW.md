# OWF Security Review Checklist

Use this checklist for changes that can affect execution authority, data exposure, or external state.

## Capabilities

- [ ] New capabilities are explicitly declared.
- [ ] Unused capabilities are disabled.
- [ ] Remote write access is separately distinguished from remote read access.
- [ ] Process execution is not assumed merely because a workflow can describe a command.

## Secrets

- [ ] No credentials are committed.
- [ ] Logs and artifacts cannot intentionally contain secret values.
- [ ] Fixtures contain synthetic values only.
- [ ] Telemetry excludes sensitive payloads.

## Commands and filesystem

- [ ] Inputs are treated as untrusted.
- [ ] Shell interpolation is avoided or safely constrained.
- [ ] Paths are validated where mutation occurs.
- [ ] Destructive commands have explicit gates.

## CI and supply chain

- [ ] GitHub Actions permissions use least privilege.
- [ ] Third-party actions are pinned or otherwise governed according to project policy.
- [ ] Dependency additions are justified.
- [ ] Build scripts are reviewed for arbitrary command execution.

## Autonomous behavior

- [ ] Objective is bounded.
- [ ] Stop conditions are explicit.
- [ ] Verification gates exist.
- [ ] Failure cannot silently become success.
- [ ] Autonomous mode cannot broaden its own capabilities.

## Findings

For every security finding record:

- severity
- location
- evidence
- impact
- confidence
- remediation
- verification method

Never report a vulnerability solely because a pattern looks suspicious. Establish the relevant execution path and evidence first.
