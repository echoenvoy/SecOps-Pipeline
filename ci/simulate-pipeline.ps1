<#
.SYNOPSIS
    Local DevSecOps CI/CD Pipeline Simulator.
.DESCRIPTION
    Executes the 4-stage pipeline skeleton locally to validate:
    1. Stage sequencing (sast -> quality-gate -> build -> deploy).
    2. Dependency gating (failure in earlier stage halts subsequent stages).
    3. Proper execution order and environment contract.
#>

[CmdletBinding()]
param (
    [switch]$FailOnSast = $false,
    [switch]$FailOnQualityGate = $false,
    [switch]$FailOnBuild = $false
)

$ErrorActionPreference = "Stop"

function Write-StageHeader {
    param ([string]$StageNumber, [string]$StageName, [string]$Tool)
    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Cyan
    Write-Host (">>> STAGE " + $StageNumber + ": " + $StageName) -ForegroundColor Cyan
    Write-Host (">>> Planned Tool: " + $Tool) -ForegroundColor DarkGray
    Write-Host "================================================================================" -ForegroundColor Cyan
}

function Run-Pipeline {
    $commitSha = $(git rev-parse --short HEAD 2>$null)
    if (-not $commitSha) { $commitSha = "local-dev" }

    Write-Host "Starting DevSecOps CI/CD Pipeline Simulation..." -ForegroundColor Yellow
    Write-Host "Commit SHA: $commitSha"
    Write-Host "Workspace:  $PWD"
    Write-Host "Timestamp:  $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

    # -------------------------------------------------------------
    # Stage 1: SAST
    # -------------------------------------------------------------
    Write-StageHeader "1" "Static Application Security Testing (SAST)" "Semgrep"
    Write-Host "Executing stage script: echo 'semgrep placeholder'"
    Start-Sleep -Milliseconds 400
    
    if ($FailOnSast) {
        Write-Host "[ERROR] SAST scan found high-severity vulnerabilities. Quality Gate failed!" -ForegroundColor Red
        Write-Host "Pipeline execution HALTED at Stage 1 (Shift-Left Gate Triggered)." -ForegroundColor Red
        return $false
    }
    Write-Host "[SUCCESS] SAST scan placeholder completed successfully." -ForegroundColor Green

    # -------------------------------------------------------------
    # Stage 2: Code Quality & Security Gate
    # -------------------------------------------------------------
    Write-StageHeader "2" "Code Quality & Security Gate" "SonarQube Scanner"
    Write-Host "Executing stage script: echo 'sonarqube placeholder'"
    Start-Sleep -Milliseconds 400

    if ($FailOnQualityGate) {
        Write-Host "[ERROR] SonarQube Quality Gate conditions not met (Coverage/Hotspots). Build blocked!" -ForegroundColor Red
        Write-Host "Pipeline execution HALTED at Stage 2." -ForegroundColor Red
        return $false
    }
    Write-Host "[SUCCESS] SonarQube quality gate placeholder passed." -ForegroundColor Green

    # -------------------------------------------------------------
    # Stage 3: Container Build
    # -------------------------------------------------------------
    Write-StageHeader "3" "Container Build & Packaging" "Docker Engine"
    Write-Host "Executing stage script: echo 'docker build placeholder'"
    Write-Host "Target Image: target-app:$commitSha"
    Start-Sleep -Milliseconds 400

    if ($FailOnBuild) {
        Write-Host "[ERROR] Docker build failed. Packaging aborted!" -ForegroundColor Red
        Write-Host "Pipeline execution HALTED at Stage 3." -ForegroundColor Red
        return $false
    }
    Write-Host "[SUCCESS] Docker build placeholder completed successfully." -ForegroundColor Green

    # -------------------------------------------------------------
    # Stage 4: Orchestration & Deployment
    # -------------------------------------------------------------
    Write-StageHeader "4" "Orchestration & Staging Deployment" "Kubernetes (kubectl)"
    Write-Host "Executing stage script: echo 'kubectl apply placeholder'"
    Write-Host "Target Cluster: kind-devsecops-lab"
    Start-Sleep -Milliseconds 400

    Write-Host "[SUCCESS] Kubernetes deployment placeholder applied successfully." -ForegroundColor Green

    Write-Host ""
    Write-Host "================================================================================" -ForegroundColor Green
    Write-Host "PIPELINE RUN STATUS: GREEN (ALL 4 STAGES COMPLETED IN ORDER)" -ForegroundColor Green
    Write-Host "================================================================================" -ForegroundColor Green
    return $true
}

$success = Run-Pipeline
if (-not $success) {
    exit 1
} else {
    exit 0
}
