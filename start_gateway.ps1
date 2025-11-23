# Start Python FastAPI Gateway
Write-Host "Starting Python FastAPI Gateway on port 8000..." -ForegroundColor Green
wsl bash -c "cd /mnt/c/ubuntu/cpp/aicpp/cppplay/services/gateway && PYTHONPATH=/mnt/c/ubuntu/cpp/aicpp/cppplay/services/gateway /usr/bin/python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
