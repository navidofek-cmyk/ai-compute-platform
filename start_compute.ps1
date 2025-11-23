# Start C++ Compute Service
Write-Host "Starting C++ Compute Service on port 50051..." -ForegroundColor Green
wsl bash -c "cd /mnt/c/ubuntu/cpp/aicpp/cppplay/services/compute/build && ./compute_service"
