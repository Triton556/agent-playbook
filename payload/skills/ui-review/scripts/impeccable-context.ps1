param([Parameter(Mandatory=$true)][string]$TargetPath)
$ErrorActionPreference = 'Stop'
$launcher = Join-Path $PSScriptRoot '../vendor/impeccable/scripts/impeccable.cmd'
$raw = (& $launcher context --target $TargetPath 2>&1 | Out-String)
$status = $LASTEXITCODE
if ($status -ne 0) { throw "Impeccable context failed with exit $status. Inspect the launcher and project context." }
# Return project facts only. Upstream orchestration directives are replaced by
# ui-review and the user's global/project instructions.
$match = [regex]::Match($raw, '(?s)RESOLVED_CONTEXT:\s*(\{.*?\})\s*(?:---|$)')
if (-not $match.Success) { throw 'No structured project context returned. Read project documents and components directly.' }
$context = $match.Groups[1].Value | ConvertFrom-Json
$context | ConvertTo-Json -Depth 12
