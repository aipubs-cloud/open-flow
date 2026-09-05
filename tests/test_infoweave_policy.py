from pathlib import Path

import yaml


POLICY = Path("infoweave/policies/capability-governor-v1.yml")


def load_policy():
    return yaml.safe_load(POLICY.read_text(encoding="utf-8"))


def test_policy_has_expected_identity():
    policy = load_policy()
    assert policy["version"] == "1.0.0"
    assert policy["protocol"] == "INFOWEAVE-OMEGA-PLUS-5"
    assert policy["workflow"] == "INFOWEAVE-GITHUB-001"


def test_allowlist_is_exact_repository():
    policy = load_policy()
    patterns = policy["repository_allowlist"]
    assert patterns == [r"^aipubs-cloud/open-flow$"]


def test_read_operations_are_authorized_without_human_review():
    policy = load_policy()
    for operation in ("analyze", "read"):
        rule = policy["operations"][operation]
        assert rule["decision"] == "AUTHORIZED"
        assert rule["human_review_required"] is False


def test_mutating_operations_require_human_review():
    policy = load_policy()
    for operation in ("propose", "create_issue", "create_pr"):
        rule = policy["operations"][operation]
        assert rule["decision"] == "AUTHORIZED_WITH_HUMAN_REVIEW"
        assert rule["human_review_required"] is True


def test_policy_invariants_include_credential_and_provenance_guards():
    policy = load_policy()
    invariants = set(policy["invariants"])
    assert "AI agents never receive GitHub credentials." in invariants
    assert "Read capabilities must not mutate repository state." in invariants
    assert "Mutation capabilities require explicit human authorization." in invariants
    assert "Provenance is emitted for every workload execution." in invariants
