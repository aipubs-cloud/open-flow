import pytest

from core.repository_creator import (
    CreationStatus,
    RepositoryPlan,
    build_result,
    normalize_provider_result,
    render_preflight,
)


@pytest.fixture
def plan():
    return RepositoryPlan(
        project_goal="A small Python research-notes tool",
        repository_name="research-notes-tool",
        owner="example-owner",
        visibility="public",
        description="Organize research notes.",
        initialize_readme=True,
        license="MIT",
        gitignore_template="Python",
        ecosystem="python",
    )


def successful_provider_result():
    return {
        "created": True,
        "repository": {
            "owner": "example-owner",
            "name": "research-notes-tool",
            "visibility": "public",
            "url": "https://github.com/example-owner/research-notes-tool",
        },
        "metadata": {
            "readme": "initialized",
            "license": "selected",
            "gitignore": "selected",
        },
    }


def test_preflight_contains_all_consequential_choices(plan):
    rendered = render_preflight(plan)
    assert "Owner:        example-owner" in rendered
    assert "Name:         research-notes-tool" in rendered
    assert "Visibility:   public" in rendered
    assert "README:       yes" in rendered
    assert "License:      MIT" in rendered
    assert ".gitignore:   Python" in rendered
    assert "CREATE ONE NEW GITHUB REPOSITORY" in rendered
    assert "[yes] [change something] [cancel]" in rendered


def test_invalid_owner_is_blocked_before_write(plan):
    invalid = RepositoryPlan(**{**plan.to_dict(), "owner": "unknown"})
    with pytest.raises(ValueError, match="owner"):
        invalid.validate()


def test_existing_repository_conflict_is_not_normalized_as_success(plan):
    result = normalize_provider_result(
        plan,
        {"created": False, "reason": "repository_exists", "repository": {"owner": "example-owner", "name": "research-notes-tool"}},
    )
    assert result["status"] == CreationStatus.FAILED.value
    assert result["repository"]["created"] is False
    assert result["repository"]["url"] == "unknown"


def test_capability_unavailable_fails_closed(plan):
    result = build_result(plan, CreationStatus.BLOCKED.value)
    assert result["status"] == "blocked"
    assert result["reason"] == "capability_unavailable"
    assert result["repository"]["created"] is False
    assert result["repository"]["url"] == "unknown"
    assert result["graduation"]["status"] == "not_ready"
    assert result["next_workflow"]["id"] == "none"


def test_cancellation_never_counts_as_creation(plan):
    result = build_result(plan, CreationStatus.CANCELLED.value)
    assert result["status"] == "cancelled"
    assert result["repository"]["created"] is False
    assert result["graduation"]["status"] == "not_ready"


def test_success_requires_observed_state_and_concept_check(plan):
    result = build_result(
        plan,
        CreationStatus.COMPLETED.value,
        successful_provider_result(),
        concept_check_passed=True,
    )
    assert result["repository"]["created"] is True
    assert result["repository"]["owner_verified"] is True
    assert result["repository"]["name_verified"] is True
    assert result["repository"]["visibility_verified"] is True
    assert result["metadata"]["readme"] == "initialized"
    assert result["graduation"]["status"] == "passed"
    assert result["next_workflow"]["id"] == "AIPUBS-START-003"


def test_missing_metadata_remains_unknown_and_blocks_graduation(plan):
    provider = successful_provider_result()
    provider["metadata"]["gitignore"] = "unknown"
    result = build_result(plan, CreationStatus.COMPLETED.value, provider, concept_check_passed=True)
    assert result["metadata"]["gitignore"] == "unknown"
    assert result["graduation"]["status"] == "not_ready"


def test_plan_is_deterministic(plan):
    assert render_preflight(plan) == render_preflight(plan)
