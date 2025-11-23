#!/usr/bin/env pwsh
# Stop all services for AI Compute Platform

Write-Host "Stopping AI Compute Platform..." -ForegroundColor Yellow

# Stop compute service
$computeRunning = wsl bash -c "ps aux | grep compute_service | grep -v grep"
if ($computeRunning) {
    Write-Host "Stopping Compute service..." -ForegroundColor Cyan
    wsl bash -c "pkill -f compute_service"
    Start-Sleep -Seconds 2
    Write-Host "✓ Compute service stopped" -ForegroundColor Green
} else {
    Write-Host "Compute service not running" -ForegroundColor Gray
}

# Stop gateway
$gatewayRunning = wsl bash -c "ps aux | grep uvicorn | grep -v grep"
if ($gatewayRunning) {
    Write-Host "Stopping Gateway..." -ForegroundColor Cyan
    wsl bash -c "pkill -f uvicorn"
    Start-Sleep -Seconds 2
    Write-Host "✓ Gateway stopped" -ForegroundColor Green
} else {
    Write-Host "Gateway not running" -ForegroundColor Gray
}

Write-Host "`nAll services stopped." -ForegroundColor Green
