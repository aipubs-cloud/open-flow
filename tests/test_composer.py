import pytest
from core.composer import PipelineComposer, WorkflowRegistry, ROOT


@pytest.fixture
def composer():
    return PipelineComposer(WorkflowRegistry(ROOT / "workflows"))


def test_artifact_binding_from_repository_explorer_to_project_doctor(composer):
    result = composer.compose(["OWF-002", "OWF-003"], max_mode="observe")
    assert {b["artifact"] for b in result["bindings"]} == {"repository-map", "architecture-map"}
    assert all(b["from"].startswith("S1.") for b in result["bindings"])
    assert result["external_inputs"] == ["S1.repository_path", "S1.max_depth", "S1.format"]


def test_artifact_binding_reaches_security_auditor(composer):
    result = composer.compose(["OWF-002", "OWF-003", "OWF-006"], max_mode="observe")
    binding_pairs = {(b["from"], b["to"]) for b in result["bindings"]}
    assert ("S1.repository-map", "S3.repository-map") in binding_pairs
    assert ("S2.health-report", "S3.health-report") in binding_pairs


def test_composer_escalation_gate(composer):
    result = composer.compose(["OWF-002", "OWF-004"], max_mode="guided")
    step_2 = result["pipeline"][1]
    assert "gate" in step_2
    assert step_2["gate"]["type"] == "manual_approval"
    assert result["gates"][0]["before_step"] == 2


def test_composer_respects_max_mode(composer):
    with pytest.raises(PermissionError):
        composer.compose(["OWF-002", "OWF-010"], max_mode="observe")


def test_composer_rejects_unknown_workflow(composer):
    with pytest.raises(ValueError, match="Unknown workflow ID"):
        composer.compose(["OWF-999"], max_mode="observe")


def test_composer_is_deterministic(composer):
    first = composer.compose(["OWF-002", "OWF-003", "OWF-006"], max_mode="observe")
    second = composer.compose(["OWF-002", "OWF-003", "OWF-006"], max_mode="observe")
    assert first == second
