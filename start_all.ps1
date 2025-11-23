#!/usr/bin/env pwsh
# Start all services for AI Compute Platform

Write-Host "Starting AI Compute Platform..." -ForegroundColor Green

# Check if services are already running
$computeRunning = wsl bash -c "ps aux | grep compute_service | grep -v grep"
$gatewayRunning = wsl bash -c "ps aux | grep uvicorn | grep -v grep"

if ($computeRunning) {
    Write-Host "Compute service already running. Stopping..." -ForegroundColor Yellow
    wsl bash -c "pkill -f compute_service"
    Start-Sleep -Seconds 2
}

if ($gatewayRunning) {
    Write-Host "Gateway already running. Stopping..." -ForegroundColor Yellow
    wsl bash -c "pkill -f uvicorn"
    Start-Sleep -Seconds 2
}

# Start compute service
Write-Host "`nStarting C++ Compute Service..." -ForegroundColor Cyan
wsl bash -c "cd /mnt/c/ubuntu/cpp/aicpp/cppplay/services/compute/build && ./compute_service &"
Start-Sleep -Seconds 3

# Check if compute service started
$computeCheck = wsl bash -c "ps aux | grep compute_service | grep -v grep"
if ($computeCheck) {
    Write-Host "✓ Compute service started (port 50051)" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start compute service" -ForegroundColor Red
    exit 1
}

# Start gateway service
Write-Host "`nStarting Python Gateway..." -ForegroundColor Cyan
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "wsl bash -c 'cd /mnt/c/ubuntu/cpp/aicpp/cppplay/services/gateway && PYTHONPATH=/mnt/c/ubuntu/cpp/aicpp/cppplay/services/gateway /usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000'"

Start-Sleep -Seconds 5

# Check if gateway started
$gatewayCheck = wsl bash -c "ps aux | grep uvicorn | grep -v grep"
if ($gatewayCheck) {
    Write-Host "✓ Gateway started (port 8000)" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to start gateway" -ForegroundColor Red
    exit 1
}

Write-Host "`n" + "="*60 -ForegroundColor Green
Write-Host "AI Compute Platform is running!" -ForegroundColor Green
Write-Host "="*60 -ForegroundColor Green
Write-Host "`nAvailable Services:" -ForegroundColor Cyan
Write-Host "  - API Gateway:    http://localhost:8000" -ForegroundColor White
Write-Host "  - API Docs:       http://localhost:8000/docs" -ForegroundColor White
Write-Host "  - Health Check:   http://localhost:8000/health" -ForegroundColor White
Write-Host "  - Compute gRPC:   localhost:50051" -ForegroundColor White
Write-Host "`nEndpoints:" -ForegroundColor Cyan
Write-Host "  - Matrix Operations:  /api/v1/compute/matrix/*" -ForegroundColor White
Write-Host "  - Statistics:         /api/v1/compute/stats/*" -ForegroundColor White
Write-Host "  - Monte Carlo:        /api/v1/compute/monte-carlo" -ForegroundColor White
Write-Host "  - AI Assistant:       /api/v1/ai/*" -ForegroundColor White
Write-Host "  - ML Inference:       /api/v1/ml/*" -ForegroundColor White
Write-Host "`nTo stop services: Ctrl+C in gateway window, then run:" -ForegroundColor Yellow
Write-Host "  wsl bash -c 'pkill -f compute_service'" -ForegroundColor Yellow
Write-Host ""
