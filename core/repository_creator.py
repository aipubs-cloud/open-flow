#!/usr/bin/env python3
"""Deterministic planner/result model for AIPUBS-START-002.

This module deliberately does not contain provider credentials or a concrete
GitHub write implementation. It validates the creation boundary, renders a
stable preflight plan, and normalizes provider results. A host may inject a
provider adapter when it exposes repository creation capability.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import argparse
import json
import re
from typing import Any, Dict, Iterable, List, Mapping, Optional


REPOSITORY_NAME = re.compile(r"^[A-Za-z0-9._-]{1,100}$")


class CreationStatus(str, Enum):
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    BLOCKED = "blocked"
    FAILED = "failed"


@dataclass(frozen=True)
class RepositoryPlan:
    project_goal: str
    repository_name: str
    owner: str
    visibility: str
    description: str = ""
    initialize_readme: bool = True
    license: str = "deferred"
    gitignore_template: str = "deferred"
    ecosystem: str = "unknown"

    def validate(self) -> None:
        if not self.project_goal.strip():
            raise ValueError("project_goal must not be empty")
        if not REPOSITORY_NAME.fullmatch(self.repository_name):
            raise ValueError("repository_name must contain only letters, numbers, '.', '_' or '-'")
        if not self.owner.strip() or self.owner == "unknown":
            raise ValueError("owner must be established before creation")
        if self.visibility not in {"public", "private"}:
            raise ValueError("visibility must be 'public' or 'private'")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "project_goal": self.project_goal,
            "repository_name": self.repository_name,
            "owner": self.owner,
            "visibility": self.visibility,
            "description": self.description,
            "initialize_readme": self.initialize_readme,
            "license": self.license,
            "gitignore_template": self.gitignore_template,
            "ecosystem": self.ecosystem,
        }


def render_preflight(plan: RepositoryPlan) -> str:
    """Render the exact human-readable write boundary."""
    plan.validate()
    return "\n".join(
        [
            "AIPubs Open Flow — Repository Creation Plan",
            "",
            f"Owner:        {plan.owner}",
            f"Name:         {plan.repository_name}",
            f"Visibility:   {plan.visibility}",
            f"Description:  {plan.description or '(none)'}",
            f"README:       {'yes' if plan.initialize_readme else 'no'}",
            f"License:      {plan.license}",
            f".gitignore:   {plan.gitignore_template}",
            "",
            "Action: CREATE ONE NEW GITHUB REPOSITORY",
            "Destructive actions: NONE",
            "",
            "Proceed with creation?",
            "[yes] [change something] [cancel]",
        ]
    )


def normalize_provider_result(plan: RepositoryPlan, provider_result: Optional[Mapping[str, Any]]) -> Dict[str, Any]:
    """Normalize a provider response without inventing missing evidence."""
    if not provider_result:
        return {
            "status": CreationStatus.BLOCKED.value,
            "reason": "capability_unavailable",
            "repository": {
                "created": False,
                "url": "unknown",
                "owner_verified": "unknown",
                "visibility_verified": "unknown",
            },
        }

    created = bool(provider_result.get("created", False))
    repository = provider_result.get("repository", {}) or {}
    owner = repository.get("owner")
    visibility = repository.get("visibility")
    name = repository.get("name")

    owner_verified = owner == plan.owner if owner is not None else "unknown"
    visibility_verified = visibility == plan.visibility if visibility is not None else "unknown"
    name_verified = name == plan.repository_name if name is not None else "unknown"

    if not created:
        return {
            "status": CreationStatus.FAILED.value,
            "reason": str(provider_result.get("reason", "provider_creation_failed")),
            "repository": {
                "created": False,
                "url": "unknown",
                "owner_verified": owner_verified,
                "name_verified": name_verified,
                "visibility_verified": visibility_verified,
            },
        }

    return {
        "status": CreationStatus.COMPLETED.value,
        "reason": "creation_returned_success",
        "repository": {
            "created": True,
            "url": repository.get("url", "unknown"),
            "owner_verified": owner_verified,
            "name_verified": name_verified,
            "visibility_verified": visibility_verified,
        },
    }


def evaluate_graduation(result: Mapping[str, Any], selected_metadata: Mapping[str, Any], concept_check_passed: bool) -> Dict[str, Any]:
    """Determine graduation from observable state, never narrative claims."""
    repository = result.get("repository", {}) or {}
    required = [
        repository.get("created") is True,
        repository.get("owner_verified") is True,
        repository.get("name_verified") is True,
        repository.get("visibility_verified") is True,
        concept_check_passed,
    ]

    for field_name, selected in selected_metadata.items():
        if selected and field_name not in {"license", "gitignore", "readme"}:
            continue
        # Metadata is supplied by the provider/verification layer. Missing values
        # are intentionally not promoted to true here.
        if selected and result.get("metadata", {}).get(field_name) in {None, "unknown"}:
            required.append(False)

    return {"status": "passed" if all(required) else "not_ready"}


def build_result(plan: RepositoryPlan, status: str, provider_result: Optional[Mapping[str, Any]] = None, concept_check_passed: bool = False) -> Dict[str, Any]:
    if status == CreationStatus.CANCELLED.value:
        normalized = {
            "status": status,
            "reason": "learner_cancelled_before_write",
            "repository": {"created": False, "url": "unknown", "owner_verified": "unknown", "name_verified": "unknown", "visibility_verified": "unknown"},
        }
    elif status == CreationStatus.BLOCKED.value and provider_result is None:
        normalized = normalize_provider_result(plan, None)
    else:
        normalized = normalize_provider_result(plan, provider_result)
        normalized["status"] = status

    normalized["workflow_id"] = "AIPUBS-START-002"
    normalized["version"] = "0.1.1"
    normalized["inputs"] = plan.to_dict()
    normalized.setdefault("metadata", {})
    normalized.setdefault("evidence", {"observed": [], "inferred": [], "unknown": []})
    normalized["concept_check"] = {"status": "passed" if concept_check_passed else "needs_review"}
    normalized["graduation"] = evaluate_graduation(normalized, {
        "readme": plan.initialize_readme,
        "license": plan.license not in {"deferred", "unknown"},
        "gitignore": plan.gitignore_template not in {"deferred", "unknown", "none"},
    }, concept_check_passed)
    if normalized["graduation"]["status"] == "passed":
        normalized["next_workflow"] = {"id": "AIPUBS-START-003", "reason": "Repository creation and baseline verification are complete."}
    else:
        normalized["next_workflow"] = {"id": "none", "reason": "Repository graduation evidence is incomplete."}
    return normalized


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan AIPUBS-START-002 repository creation")
    parser.add_argument("--goal", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--owner", required=True)
    parser.add_argument("--visibility", choices=["public", "private"], required=True)
    parser.add_argument("--description", default="")
    parser.add_argument("--license", default="deferred")
    parser.add_argument("--gitignore", default="deferred")
    parser.add_argument("--no-readme", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    plan = RepositoryPlan(
        project_goal=args.goal,
        repository_name=args.name,
        owner=args.owner,
        visibility=args.visibility,
        description=args.description,
        initialize_readme=not args.no_readme,
        license=args.license,
        gitignore_template=args.gitignore,
    )
    plan.validate()
    output = {"workflow_id": "AIPUBS-START-002", "version": "0.1.1", "preflight": render_preflight(plan), "plan": plan.to_dict()}
    print(json.dumps(output, indent=2) if args.json else output["preflight"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
