param()
$ErrorActionPreference = 'Stop'
$payload = [Console]::In.ReadToEnd()
try { $event = $payload | ConvertFrom-Json } catch {
  '{"permissionDecision":"deny","permissionDecisionReason":"OWF hook received invalid JSON; failing closed."}'
  exit 0
}
$tool = [string]$event.toolName
$mode = [string]($env:OWF_CURRENT_MODE ?? 'observe').ToLower()
$approved = $env:OWF_APPROVED_ESCALATION -eq '1'
if (($tool -in @('create','edit')) -and ($mode -in @('observe','plan')) -and -not $approved) {
  @{ permissionDecision='deny'; permissionDecisionReason="OWF blocks $tool while mode=$mode. Approve the escalation gate before modifying files." } | ConvertTo-Json -Compress
  exit 0
}
if (($tool -in @('bash','powershell')) -and ($mode -in @('observe','plan')) -and -not $approved) {
  $command = [string]($event.toolArgs.command ?? $event.toolArgs.cmd ?? '')
  if ($command -match '(?i)(^|[;&|])\s*(rm|mv|cp|mkdir|rmdir|touch|chmod|chown|git\s+(commit|merge|rebase|cherry-pick|reset|checkout)|sed\s+-i|perl\s+-i|tee\b)|(>\s*[^=])') {
    @{ permissionDecision='deny'; permissionDecisionReason='OWF detected a potentially mutating shell command while the pipeline is read-only. Approve the escalation gate first.' } | ConvertTo-Json -Compress
    exit 0
  }
}
'{"permissionDecision":"allow"}'
