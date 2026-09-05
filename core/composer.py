#!/usr/bin/env python3
"""Deterministic OWF workflow composition engine.

The engine compiles an explicit workflow sequence into a composite manifest. It
never executes tools, changes files, or grants permissions. Safety policy is
resolved for every stage using the most restrictive applicable policy.
"""
from __future__ import annotations

from dataclasses import dataclass
import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

import yaml

try:
    from .safety import MODE_RANK, SafetyPolicy, resolve_safety
except ImportError:  # pragma: no cover - supports ``python core/composer.py``
    from safety import MODE_RANK, SafetyPolicy, resolve_safety

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS_DIR = ROOT / "workflows"
ACTIVE_MODES = {"guided", "assisted", "autonomous"}


@dataclass(frozen=True)
class WorkflowNode:
    id: str
    name: str
    mode: str
    path: Path
    inputs: Tuple[str, ...] = ()
    outputs: Tuple[str, ...] = ()
    modifies_files: bool = False
    requires_confirmation: bool = False
    safety: SafetyPolicy = SafetyPolicy()


class WorkflowRegistry:
    def __init__(self, root: Path = WORKFLOWS_DIR):
        self.workflows: Dict[str, WorkflowNode] = {}
        self._load(root)

    @staticmethod
    def _names(values: Iterable[Any]) -> Tuple[str, ...]:
        names: List[str] = []
        for value in values or []:
            if isinstance(value, str):
                names.append(value)
            elif isinstance(value, dict):
                names.extend(str(k) for k in value)
            else:
                raise TypeError(f"Unsupported workflow contract entry: {value!r}")
        return tuple(names)

    def _load(self, root: Path) -> None:
        for manifest_path in sorted(root.glob("**/workflow.yaml")):
            data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            workflow_id = data.get("id")
            if not workflow_id:
                raise ValueError(f"Missing workflow id: {manifest_path}")
            if workflow_id in self.workflows:
                raise ValueError(f"Duplicate workflow id: {workflow_id}")
            mode = data.get("mode", "guided")
            if mode not in MODE_RANK:
                raise ValueError(f"Unsupported mode {mode!r} in {manifest_path}")
            safety_data = dict(data.get("safety", {}) or {})
            safety_data["mode"] = mode
            safety_data.setdefault("write", bool(safety_data.get("modifies_files", False)))
            safety = SafetyPolicy.from_mapping(safety_data)
            self.workflows[workflow_id] = WorkflowNode(
                id=workflow_id,
                name=str(data["name"]),
                mode=mode,
                path=manifest_path.parent,
                inputs=self._names(data.get("inputs", [])),
                outputs=self._names(data.get("outputs", [])),
                modifies_files=bool(safety_data.get("modifies_files", False) or safety_data.get("write", False)),
                requires_confirmation=bool(safety_data.get("requires_confirmation_before_modification", safety.require_confirmation)),
                safety=safety,
            )


class PipelineComposer:
    def __init__(self, registry: WorkflowRegistry):
        self.registry = registry

    def _resolve_bindings(self, pipeline: List[WorkflowNode]) -> Tuple[List[Dict[str, str]], List[str]]:
        produced: Dict[str, str] = {}
        bindings: List[Dict[str, str]] = []
        external: List[str] = []
        for index, workflow in enumerate(pipeline, start=1):
            for input_name in workflow.inputs:
                if input_name in produced:
                    bindings.append({
                        "to": f"S{index}.{input_name}",
                        "from": produced[input_name],
                        "artifact": input_name,
                    })
                else:
                    external.append(f"S{index}.{input_name}")
            for output_name in workflow.outputs:
                produced[output_name] = f"S{index}.{output_name}"
        return bindings, external

    @staticmethod
    def _assert_no_duplicate_outputs(pipeline: List[WorkflowNode]) -> None:
        owners: Dict[str, str] = {}
        for workflow in pipeline:
            for output in workflow.outputs:
                if output in owners:
                    raise ValueError(
                        f"Ambiguous artifact '{output}' produced by both {owners[output]} and {workflow.id}"
                    )
                owners[output] = workflow.id

    def compose(self, workflow_sequence: List[str], max_mode: str = "guided") -> Dict[str, Any]:
        if max_mode not in MODE_RANK:
            raise ValueError(f"Unsupported max_mode: {max_mode}")
        if not workflow_sequence:
            raise ValueError("workflow_sequence must not be empty")

        pipeline: List[WorkflowNode] = []
        for workflow_id in workflow_sequence:
            try:
                workflow = self.registry.workflows[workflow_id]
            except KeyError as exc:
                raise ValueError(f"Unknown workflow ID: {workflow_id}") from exc
            if MODE_RANK[workflow.mode] > MODE_RANK[max_mode]:
                raise PermissionError(
                    f"Workflow {workflow.id} ({workflow.name}) requires mode '{workflow.mode}', "
                    f"which exceeds max_mode '{max_mode}'."
                )
            pipeline.append(workflow)

        self._assert_no_duplicate_outputs(pipeline)
        bindings, external_inputs = self._resolve_bindings(pipeline)

        entries: List[Dict[str, Any]] = []
        gates: List[Dict[str, Any]] = []
        previous_level = MODE_RANK["observe"]
        host_policy = SafetyPolicy(mode=max_mode, write=True, dry_run=False)

        for index, workflow in enumerate(pipeline, start=1):
            level = MODE_RANK[workflow.mode]
            effective_safety = resolve_safety(workflow.safety, host_policy)
            escalates_to_active = level >= MODE_RANK["guided"] and previous_level < MODE_RANK["guided"]
            needs_modification_gate = workflow.modifies_files or workflow.requires_confirmation
            requires_gate = escalates_to_active or needs_modification_gate

            entry: Dict[str, Any] = {
                "step": index,
                "workflow": workflow.id,
                "name": workflow.name,
                "mode": workflow.mode,
                "effective_mode": effective_safety.mode,
                "artifacts_produced": list(workflow.outputs),
                "safety": effective_safety.to_dict(),
            }
            if requires_gate:
                gate_id = f"G{index}"
                reason = (
                    "Privilege escalation from read-only mode to an active mode."
                    if escalates_to_active
                    else "Workflow requires explicit confirmation before modification."
                )
                gate = {
                    "id": gate_id,
                    "before_step": index,
                    "type": "manual_approval",
                    "reason": reason,
                    "approval_env": "OWF_APPROVED_ESCALATION=1",
                }
                entry["gate"] = gate
                gates.append(gate)

            entries.append(entry)
            previous_level = level

        result: Dict[str, Any] = {
            "type": "composite",
            "version": "0.1.0",
            "max_mode": max_mode,
            "effective_safety_policy": {
                "mode_cap": max_mode,
                "composition_rule": "restriction_preserving",
            },
            "pipeline": entries,
            "bindings": bindings,
            "external_inputs": external_inputs,
            "gates": gates,
            "total_artifacts": sorted({artifact for wf in pipeline for artifact in wf.outputs}),
        }
        result["mermaid"] = generate_mermaid_dag(result)
        result["copilot_plan"] = generate_copilot_plan(result)
        return result


def generate_mermaid_dag(pipeline_data: Dict[str, Any]) -> str:
    lines = ["graph TD"]
    for item in pipeline_data["pipeline"]:
        step_id = f"S{item['step']}"
        label = f"{item['workflow']}<br/>{item['name']}<br/>({item['effective_mode']})"
        lines.append(f'    {step_id}["{label}"]')
        if "gate" in item:
            gate_id = item["gate"]["id"]
            lines.append(f'    {gate_id}{{"Checkpoint: approve escalation"}}')
            lines.append(f"    {gate_id} -->|Approved| {step_id}")

    for binding in pipeline_data["bindings"]:
        source = binding["from"].split(".", 1)[0]
        target = binding["to"].split(".", 1)[0]
        if source != target:
            lines.append(f"    {source} -->|{binding['artifact']}| {target}")

    for left, right in zip(pipeline_data["pipeline"], pipeline_data["pipeline"][1:]):
        left_id, right_id = f"S{left['step']}", f"S{right['step']}"
        has_binding = any(
            b["from"].startswith(left_id + ".") and b["to"].startswith(right_id + ".")
            for b in pipeline_data["bindings"]
        )
        if not has_binding:
            lines.append(f"    {left_id} --> {right_id}")
    return "\n".join(lines)


def generate_copilot_plan(pipeline_data: Dict[str, Any]) -> str:
    lines = [
        "1. Enter Copilot CLI Plan mode with Shift+Tab (or /plan).",
        "2. Review the generated OWF graph, every artifact binding, and every effective safety policy.",
    ]
    for item in pipeline_data["pipeline"]:
        line = f"3. Run {item['workflow']} ({item['effective_mode']})"
        if "gate" in item:
            line += " only after the checkpoint is explicitly approved"
        lines.append(line + ".")
    lines.extend([
        "4. Use custom agents/subagents for independent specialist stages where appropriate.",
        "5. Keep sequential stages ordered by their artifact bindings.",
        "6. Keep the OWF preToolUse hook enabled so tool execution cannot silently cross the declared safety boundary.",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile an OWF workflow sequence into a safety-gated DAG")
    parser.add_argument("workflow", nargs="+", help="Workflow IDs, for example OWF-002 OWF-003 OWF-006")
    parser.add_argument("--max-mode", default="guided", choices=sorted(MODE_RANK, key=MODE_RANK.get))
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of YAML")
    args = parser.parse_args()

    result = PipelineComposer(WorkflowRegistry()).compose(args.workflow, args.max_mode)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(yaml.safe_dump(result, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
