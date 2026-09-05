import pytest

from core.safety import SafetyPolicy, SafetyResolutionError, assert_non_escalating, capability_status, resolve_safety


def policy(**overrides):
    base = {
        "mode": "assisted",
        "write": True,
        "destructive_operations": False,
        "require_confirmation_for_write": True,
        "force_push": False,
        "delete_operations": False,
        "secret_exposure": False,
        "credential_requests": False,
        "network": False,
        "dry_run": False,
        "filesystem_scope": ["src/"],
        "repository_scope": ["aipubs-cloud/open-flow"],
        "capabilities": ["read_repo", "write_repo"],
        "evidence_required": True,
    }
    base.update(overrides)
    return SafetyPolicy.from_mapping(base)


def test_observe_child_cannot_become_write_capable():
    child = policy(mode="observe", write=False, dry_run=True, capabilities=["read_repo"])
    parent = policy(mode="assisted", write=True, dry_run=False, capabilities=["read_repo", "write_repo"])
    effective = resolve_safety(child, parent)
    assert effective.mode == "observe"
    assert effective.write is False
    assert effective.dry_run is True
    assert effective.capabilities == frozenset({"read_repo"})


def test_restrictions_are_preserved():
    child = policy(destructive_operations=False, force_push=False, delete_operations=False)
    parent = policy(destructive_operations=True, force_push=True, delete_operations=True)
    effective = resolve_safety(child, parent)
    assert effective.destructive is False
    assert effective.force_push is False
    assert effective.delete_operations is False


def test_confirmation_and_evidence_cannot_be_removed():
    child = policy(require_confirmation_for_write=True, evidence_required=True)
    parent = policy(require_confirmation_for_write=False, evidence_required=False)
    effective = resolve_safety(child, parent)
    assert effective.require_confirmation is True
    assert effective.evidence_required is True


def test_dry_run_is_sticky():
    child = policy(dry_run=True)
    parent = policy(dry_run=False)
    assert resolve_safety(child, parent).dry_run is True


def test_scopes_and_capabilities_intersect():
    child = policy(filesystem_scope=["src/", "tests/"], capabilities=["read_repo", "write_repo"])
    parent = policy(filesystem_scope=["src/"], capabilities=["read_repo"])
    effective = resolve_safety(child, parent)
    assert effective.filesystem_scope == frozenset({"src/"})
    assert effective.capabilities == frozenset({"read_repo"})


def test_missing_capability_fails_closed():
    effective = resolve_safety(policy(capabilities=["read_repo"]), policy(capabilities=["read_repo", "write_repo"]))
    assert capability_status(effective, ["write_repo"]) == "capability_unavailable"
    assert capability_status(effective, ["read_repo"]) == "allowed"


def test_non_escalation_accepts_resolved_policy():
    child = policy(mode="observe", write=False, capabilities=["read_repo"], dry_run=True)
    effective = resolve_safety(child, policy())
    assert_non_escalating(child, effective)


def test_non_escalation_rejects_write_escalation():
    child = policy(mode="observe", write=False, capabilities=["read_repo"], dry_run=True)
    with pytest.raises(SafetyResolutionError):
        assert_non_escalating(child, policy())


def test_non_escalation_rejects_confirmation_removal():
    child = policy(require_confirmation_for_write=True)
    effective = policy(require_confirmation_for_write=False)
    with pytest.raises(SafetyResolutionError):
        assert_non_escalating(child, effective)


def test_nested_composition_remains_monotonic():
    observe = policy(mode="observe", write=False, capabilities=["read_repo"], dry_run=True)
    assisted = policy(mode="assisted", write=True, capabilities=["read_repo", "write_repo"], dry_run=False)
    autonomous = policy(mode="autonomous", write=True, capabilities=["read_repo", "write_repo"], dry_run=False)
    effective = resolve_safety(observe, assisted, autonomous)
    assert effective.mode == "observe"
    assert effective.write is False
    assert effective.capabilities == frozenset({"read_repo"})
    assert effective.dry_run is True
