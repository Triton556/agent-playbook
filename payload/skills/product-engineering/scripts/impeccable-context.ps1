param([Parameter(Mandatory=$true)][string]$TargetPath)
$ErrorActionPreference = 'Stop'
# Compatibility for an earlier published path; implementation has one owner.
& (Join-Path $PSScriptRoot '../../product-ui-review/scripts/impeccable-context.ps1') -TargetPath $TargetPath
