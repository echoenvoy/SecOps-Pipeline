<#
.SYNOPSIS
    Semgrep SAST Runner and Report Generator for SecOps-Pipeline.
.DESCRIPTION
    Executes Semgrep SAST scans using both OWASP Top 10 rule registry and custom rules
    defined in security/semgrep/rules.yml. Produces structured reports (JSON and SARIF),
    parses findings, displays an executive summary table, and enforces a zero-tolerance
    pipeline gate on ERROR-severity findings.
#>

[CmdletBinding()]
param (
    [string]$TargetDir = "app",
    [string[]]$ConfigFiles = @("p/owasp-top-ten", "security/semgrep/rules.yml"),
    [string]$ReportsDir = "reports",
    [string]$JsonReport = "reports/semgrep.json",
    [string]$SarifReport = "reports/semgrep.sarif",
    [switch]$FailOnError = $true
)

$ErrorActionPreference = "Continue"
$env:SEMGREP_SEND_METRICS = "off"

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ">>> [SAST SCAN] Static Application Security Testing with Semgrep" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "Target directory : $TargetDir" -ForegroundColor Yellow
Write-Host "Rulesets         : $($ConfigFiles -join ', ')" -ForegroundColor Yellow
Write-Host "Report format    : JSON ($JsonReport), SARIF ($SarifReport)" -ForegroundColor Yellow
Write-Host "Fail on Error    : $FailOnError" -ForegroundColor Yellow
Write-Host ""

# Ensure reports directory exists
if (-not (Test-Path $ReportsDir)) {
    New-Item -ItemType Directory -Path $ReportsDir -Force | Out-Null
}

# Verify Semgrep CLI is available
$semgrepCmd = Get-Command "semgrep" -ErrorAction SilentlyContinue
if (-not $semgrepCmd) {
    Write-Host "[ERROR] Semgrep CLI executable not found in PATH." -ForegroundColor Red
    Write-Host "Please install it with: pip install semgrep" -ForegroundColor Red
    exit 1
}

# Build arguments list for JSON report
$argsList = @("scan")
foreach ($cfg in $ConfigFiles) {
    $argsList += @("--config", $cfg)
}
$argsList += @("--json", "-o", $JsonReport)
$argsList += @($TargetDir)

Write-Host "Running: semgrep $($argsList -join ' ')" -ForegroundColor DarkGray
$scanStartTime = Get-Date

# Execute Semgrep for JSON output
& semgrep $argsList
$exitCode = $LASTEXITCODE
$scanDuration = [Math]::Round(((Get-Date) - $scanStartTime).TotalSeconds, 2)

# If SARIF output is requested, generate it as well
if ($SarifReport) {
    $sarifArgs = @("scan")
    foreach ($cfg in $ConfigFiles) {
        $sarifArgs += @("--config", $cfg)
    }
    $sarifArgs += @("--sarif", "-o", $SarifReport)
    $sarifArgs += @($TargetDir)
    Write-Host "Generating SARIF report at $SarifReport..." -ForegroundColor DarkGray
    & semgrep $sarifArgs | Out-Null
}

Write-Host ""
Write-Host "SAST scan execution finished in $scanDuration seconds (Semgrep exit code $exitCode)." -ForegroundColor DarkGray

# Parse and display JSON report
if (Test-Path $JsonReport) {
    try {
        $jsonContent = Get-Content $JsonReport -Raw | ConvertFrom-Json
        $results = $jsonContent.results
        $errorsCount = 0
        $warningsCount = 0
        $infosCount = 0

        foreach ($r in $results) {
            $sev = $r.extra.severity
            if ($sev -eq "ERROR") { $errorsCount++ }
            elseif ($sev -eq "WARNING") { $warningsCount++ }
            else { $infosCount++ }
        }

        Write-Host ""
        Write-Host "--------------------------------------------------------------------------------" -ForegroundColor Cyan
        Write-Host "SAST EXECUTIVE SUMMARY" -ForegroundColor Cyan
        Write-Host "--------------------------------------------------------------------------------" -ForegroundColor Cyan
        Write-Host ("Total Findings Detected : " + $results.Count) -ForegroundColor White
        Write-Host ("  - High Severity (ERROR)   : " + $errorsCount) -ForegroundColor $(if ($errorsCount -gt 0) { "Red" } else { "Green" })
        Write-Host ("  - Medium Severity (WARN)  : " + $warningsCount) -ForegroundColor $(if ($warningsCount -gt 0) { "Yellow" } else { "Green" })
        Write-Host ("  - Low Severity (INFO)     : " + $infosCount) -ForegroundColor "DarkCyan"
        Write-Host "--------------------------------------------------------------------------------" -ForegroundColor Cyan

        if ($results.Count -gt 0) {
            Write-Host ""
            Write-Host "Detailed Findings Breakdown:" -ForegroundColor White
            $index = 1
            foreach ($r in $results) {
                $sev = $r.extra.severity
                $color = if ($sev -eq "ERROR") { "Red" } elseif ($sev -eq "WARNING") { "Yellow" } else { "Gray" }
                $ruleId = $r.check_id
                $filePath = $r.path
                $lineNum = $r.start.line
                $msg = $r.extra.message
                Write-Host ("[$index] [$sev] $ruleId") -ForegroundColor $color
                Write-Host ("    Location: $filePath : Line $lineNum") -ForegroundColor DarkGray
                Write-Host ("    Details : $msg") -ForegroundColor Gray
                $index++
            }
        }

        Write-Host ""
        if ($errorsCount -gt 0 -and $FailOnError) {
            Write-Host "[PIPELINE GATE FAILED] SAST Quality Gate triggered: $errorsCount high-severity finding(s) detected!" -ForegroundColor Red
            Write-Host "Shift-Left Security Gate Enforced: Blocking subsequent build and deployment stages." -ForegroundColor Red
            exit 1
        } else {
            Write-Host "[PIPELINE GATE PASSED] No blocking security errors identified." -ForegroundColor Green
            exit 0
        }
    } catch {
        Write-Host "[WARNING] Unable to parse JSON report: $_" -ForegroundColor Yellow
        exit $exitCode
    }
} else {
    Write-Host "[ERROR] Semgrep JSON report was not generated at $JsonReport" -ForegroundColor Red
    exit 1
}
