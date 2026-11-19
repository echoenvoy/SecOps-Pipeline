# Demonstration and Verification Harness for Phase 3 SAST Gates (Before / After).
$ErrorActionPreference = "Continue"

Write-Host "================================================================================" -ForegroundColor Magenta
Write-Host ">>> PHASE 3 SAST INTEGRATION - BEFORE / AFTER DEMONSTRATION HARNESS" -ForegroundColor Magenta
Write-Host "================================================================================" -ForegroundColor Magenta
Write-Host ""

# Scenario 1: Vulnerable Code
Write-Host ">>> RUNNING SCENARIO 1: Intentionally Vulnerable Application (Target: app/)" -ForegroundColor Yellow
$scriptPath = Join-Path $PSScriptRoot "simulate-pipeline.ps1"
& powershell -ExecutionPolicy Bypass -File $scriptPath -RealSast -TargetDir "app"
$codeA = $LASTEXITCODE

# Scenario 2: Remediated Code
Write-Host ""
Write-Host ">>> RUNNING SCENARIO 2: Remediated Application (Target: app_remediated/)" -ForegroundColor Cyan
& powershell -ExecutionPolicy Bypass -File $scriptPath -RealSast -TargetDir "app_remediated"
$codeB = $LASTEXITCODE

# Summary Verification Matrix
Write-Host ""
Write-Host "================================================================================" -ForegroundColor Magenta
Write-Host "PHASE 3 SAST VERIFICATION SUMMARY" -ForegroundColor Magenta
Write-Host "================================================================================" -ForegroundColor Magenta
if ($codeA -ne 0) {
    Write-Host "Scenario 1 (Vulnerable Code) : Exit Code $codeA -> GATE ENFORCED (BLOCKED) [PASS]" -ForegroundColor Green
} else {
    Write-Host "Scenario 1 (Vulnerable Code) : Exit Code $codeA -> FAILED TO BLOCK" -ForegroundColor Red
}

if ($codeB -eq 0) {
    Write-Host "Scenario 2 (Remediated Code) : Exit Code $codeB -> PIPELINE PASSED (GREEN)   [PASS]" -ForegroundColor Green
} else {
    Write-Host "Scenario 2 (Remediated Code) : Exit Code $codeB -> FAILED TO PASS" -ForegroundColor Red
}
Write-Host "================================================================================" -ForegroundColor Magenta

if ($codeA -ne 0 -and $codeB -eq 0) {
    Write-Host "[SUCCESS] Phase 3 SAST integration and Shift-Left gating successfully verified!" -ForegroundColor Green
    exit 0
} else {
    Write-Host "[FAILURE] SAST verification failed to satisfy before/after gate criteria." -ForegroundColor Red
    exit 1
}
