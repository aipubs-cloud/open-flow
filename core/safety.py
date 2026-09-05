"""Safety policy resolution for composed Open Flow workflows.

The resolver is deliberately dependency-free and fail-closed. Composition can
only preserve or add restrictions. It can never broaden a child workflow's
authority.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable, Mapping

MODES = ("observe", "plan", "guided", "assisted", "autonomous")
MODE_RANK = {mode: index for index, mode in enumerate(MODES)}


class SafetyResolutionError(ValueError):
    """Raised when a policy is malformed or cannot be safely resolved."""


@dataclass(frozen=True)
class SafetyPolicy:
    """Canonical, restriction-oriented execution policy."""

    mode: str = "observe"
    write: bool = False
    destructive: bool = False
    require_confirmation: bool = True
    force_push: bool = False
    delete_operations: bool = False
    secret_exposure: bool = False
    credential_requests: bool = False
    network: bool = False
    dry_run: bool = True
    filesystem_scope: frozenset[str] = field(default_factory=frozenset)
    repository_scope: frozenset[str] = field(default_factory=frozenset)
    capabilities: frozenset[str] = field(default_factory=frozenset)
    evidence_required: bool = True

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "SafetyPolicy":
        if value is None:
            return cls()
        mode = str(value.get("mode", "observe"))
        if mode not in MODE_RANK:
            raise SafetyResolutionError(f"unsupported mode: {mode!r}")

        # Missing authority is intentionally restrictive. A capability must be
        # explicitly named before composition can retain it.
        return cls(
            mode=mode,
            write=bool(value.get("write", False)),
            destructive=bool(value.get("destructive_operations", value.get("destructive", False))),
            require_confirmation=bool(value.get("require_confirmation_for_write", value.get("require_confirmation", True))),
            force_push=bool(value.get("force_push", False)),
            delete_operations=bool(value.get("delete_operations", False)),
            secret_exposure=bool(value.get("secret_exposure", False)),
            credential_requests=bool(value.get("credential_requests", False)),
            network=bool(value.get("network", False)),
            dry_run=bool(value.get("dry_run", True)),
            filesystem_scope=_as_scope(value.get("filesystem_scope")),
            repository_scope=_as_scope(value.get("repository_scope")),
            capabilities=_as_scope(value.get("capabilities")),
            evidence_required=bool(value.get("evidence_required", True)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "write": self.write,
            "destructive_operations": self.destructive,
            "require_confirmation_for_write": self.require_confirmation,
            "force_push": self.force_push,
            "delete_operations": self.delete_operations,
            "secret_exposure": self.secret_exposure,
            "credential_requests": self.credential_requests,
            "network": self.network,
            "dry_run": self.dry_run,
            "filesystem_scope": sorted(self.filesystem_scope),
            "repository_scope": sorted(self.repository_scope),
            "capabilities": sorted(self.capabilities),
            "evidence_required": self.evidence_required,
        }


def _as_scope(value: Any) -> frozenset[str]:
    if value is None:
        return frozenset()
    if isinstance(value, str):
        return frozenset({value})
    if isinstance(value, Iterable) and not isinstance(value, (bytes, bytearray, Mapping)):
        return frozenset(str(item) for item in value)
    raise SafetyResolutionError("scope/capabilities must be a string or iterable")


def _intersect_scopes(values: list[frozenset[str]]) -> frozenset[str]:
    non_empty = [value for value in values if value]
    if not non_empty:
        return frozenset()
    result = set(non_empty[0])
    for value in non_empty[1:]:
        result.intersection_update(value)
    return frozenset(result)


def resolve_safety(*policies: SafetyPolicy | Mapping[str, Any] | None) -> SafetyPolicy:
    """Resolve policies using the most restrictive safe combination.

    Boolean authority fields use logical AND. Restrictions such as required
    confirmation, dry-run, and evidence requirements use logical OR. Scopes
    and capabilities are intersected when multiple explicit scopes exist.
    """
    normalized = [
        policy if isinstance(policy, SafetyPolicy) else SafetyPolicy.from_mapping(policy)
        for policy in policies
        if policy is not None
    ]
    if not normalized:
        return SafetyPolicy()

    return SafetyPolicy(
        mode=min(normalized, key=lambda p: MODE_RANK[p.mode]).mode,
        write=all(p.write for p in normalized),
        destructive=all(p.destructive for p in normalized),
        require_confirmation=any(p.require_confirmation for p in normalized),
        force_push=all(p.force_push for p in normalized),
        delete_operations=all(p.delete_operations for p in normalized),
        secret_exposure=all(p.secret_exposure for p in normalized),
        credential_requests=all(p.credential_requests for p in normalized),
        network=all(p.network for p in normalized),
        dry_run=any(p.dry_run for p in normalized),
        filesystem_scope=_intersect_scopes([p.filesystem_scope for p in normalized]),
        repository_scope=_intersect_scopes([p.repository_scope for p in normalized]),
        capabilities=_intersect_scopes([p.capabilities for p in normalized]),
        evidence_required=any(p.evidence_required for p in normalized),
    )


def capability_status(policy: SafetyPolicy, requested: Iterable[str]) -> str:
    """Return ``allowed`` only when every requested capability is retained."""
    requested_set = {str(item) for item in requested}
    if requested_set <= policy.capabilities:
        return "allowed"
    return "capability_unavailable"


def assert_non_escalating(child: SafetyPolicy, effective: SafetyPolicy) -> None:
    """Raise if an effective policy broadens any inherited restriction."""
    if MODE_RANK[effective.mode] > MODE_RANK[child.mode]:
        raise SafetyResolutionError("effective mode escalates beyond child policy")
    if child.write and not effective.write:
        return
    if not child.write and effective.write:
        raise SafetyResolutionError("write authority escalated")
    for name in ("destructive", "force_push", "delete_operations", "secret_exposure", "credential_requests", "network"):
        if getattr(effective, name) and not getattr(child, name):
            raise SafetyResolutionError(f"{name} authority escalated")
    if child.require_confirmation and not effective.require_confirmation:
        raise SafetyResolutionError("confirmation requirement removed")
    if child.dry_run and not effective.dry_run:
        raise SafetyResolutionError("dry-run restriction removed")
    if child.evidence_required and not effective.evidence_required:
        raise SafetyResolutionError("evidence requirement removed")
