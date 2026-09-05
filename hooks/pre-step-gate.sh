#!/usr/bin/env bash
# OWF pre-step gate for GitHub Copilot CLI preToolUse hooks.
# Reads the hook payload from stdin and returns a JSON permission decision.
set -euo pipefail

payload="$(cat)"

python3 - "$payload" <<'PY'
import json
import os
import re
import sys

raw = sys.argv[1] if len(sys.argv) > 1 else "{}"
try:
    event = json.loads(raw)
except json.JSONDecodeError:
    print(json.dumps({
        "permissionDecision": "deny",
        "permissionDecisionReason": "OWF hook received invalid JSON; failing closed."
    }))
    raise SystemExit(0)

tool = event.get("toolName", "")
args = event.get("toolArgs", {})
mode = os.environ.get("OWF_CURRENT_MODE", "observe").lower()
approved = os.environ.get("OWF_APPROVED_ESCALATION", "0") == "1"

active_modes = {"guided", "assisted", "autonomous"}
write_tools = {"create", "edit"}

# Direct file mutation tools are unambiguously consequential.
if tool in write_tools and mode in {"observe", "plan"}:
    decision = "allow" if approved else "deny"
    reason = (
        "OWF escalation gate approved for this session."
        if approved else
        f"OWF blocks {tool} while mode={mode}. Approve the escalation gate before modifying files."
    )
    print(json.dumps({"permissionDecision": decision, "permissionDecisionReason": reason}))
    raise SystemExit(0)

# Shell commands require conservative mutation detection. Read-only shell commands remain usable.
if tool in {"bash", "powershell"} and mode in {"observe", "plan"}:
    command = ""
    if isinstance(args, dict):
        command = str(args.get("command") or args.get("cmd") or "")
    mutation = re.compile(
        r"(^|[;&|])\s*(rm|mv|cp|mkdir|rmdir|touch|chmod|chown|git\s+(commit|merge|rebase|cherry-pick|reset|checkout)|"
        r"sed\s+-i|perl\s+-i|tee\b)|(?:>\s*[^=])"
    )
    if mutation.search(command) and not approved:
        print(json.dumps({
            "permissionDecision": "deny",
            "permissionDecisionReason": "OWF detected a potentially mutating shell command while the pipeline is read-only. Approve the escalation gate first."
        }))
        raise SystemExit(0)

print(json.dumps({"permissionDecision": "allow"}))
PY
