# Foundation Review Checklist

Reviewers should evaluate this branch as a repository foundation, not merely as a documentation change.

## Structure

- Are responsibilities separated between workflows, agents, skills, hooks, and host integrations?
- Are public contracts represented by schemas?
- Are examples safe and minimal?

## Behavior

- Are executable claims backed by tests?
- Are deterministic claims bounded by explicit assumptions?
- Are error paths represented?

## Safety

- Are capabilities explicit?
- Are destructive operations opt-in?
- Are secrets excluded from artifacts?
- Does autonomous mode remain bounded?

## Compatibility

- Are existing OWF-001 through OWF-010 manifests compatible with the strengthened workflow schema?
- Are host-specific claims clearly separated from core OWF contracts?

## Release readiness

- Does the changelog describe contract changes?
- Does CI install and test the package from a clean environment?
- Can another contributor reproduce the validation commands?
