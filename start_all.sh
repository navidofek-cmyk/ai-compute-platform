#!/bin/bash

# Start All Services Script for Linux

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Project root
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

echo -e "${GREEN}Starting AI Compute Platform Services...${NC}"
echo "Project Root: $PROJECT_ROOT"
echo ""

# Check if services are already running
COMPUTE_PID=$(pgrep -f "compute_service" | head -1)
GATEWAY_PID=$(pgrep -f "uvicorn.*app.main:app" | head -1)

if [ ! -z "$COMPUTE_PID" ]; then
    echo -e "${YELLOW}Compute service already running (PID: $COMPUTE_PID)${NC}"
    echo "Use stop_all.sh first if you want to restart."
else
    echo -e "${GREEN}Starting Compute Service...${NC}"
    cd "$PROJECT_ROOT/services/compute/build"
    
    if [ ! -f "./compute_service" ]; then
        echo -e "${RED}ERROR: compute_service binary not found!${NC}"
        echo "Run: cd services/compute && cmake -S . -B build && cmake --build build -j4"
        exit 1
    fi
    
    nohup env LD_LIBRARY_PATH=/usr/local/lib ./compute_service > /tmp/compute.log 2>&1 &
    COMPUTE_PID=$!
    sleep 2
    
    if ps -p $COMPUTE_PID > /dev/null; then
        echo -e "${GREEN}✓ Compute service started (PID: $COMPUTE_PID)${NC}"
    else
        echo -e "${RED}✗ Failed to start compute service${NC}"
        echo "Check logs: tail -50 /tmp/compute.log"
    fi
fi

echo ""

if [ ! -z "$GATEWAY_PID" ]; then
    echo -e "${YELLOW}Gateway already running (PID: $GATEWAY_PID)${NC}"
    echo "Use stop_all.sh first if you want to restart."
else
    echo -e "${GREEN}Starting Gateway Service...${NC}"
    cd "$PROJECT_ROOT/services/gateway"
    
    if [ ! -f "app/main.py" ]; then
        echo -e "${RED}ERROR: Gateway app/main.py not found!${NC}"
        exit 1
    fi
    
    nohup env PYTHONPATH="$PROJECT_ROOT/services/gateway" python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 > /tmp/gateway.log 2>&1 &
    GATEWAY_PID=$!
    sleep 3
    
    if ps -p $GATEWAY_PID > /dev/null; then
        echo -e "${GREEN}✓ Gateway started (PID: $GATEWAY_PID)${NC}"
    else
        echo -e "${RED}✗ Failed to start gateway${NC}"
        echo "Check logs: tail -50 /tmp/gateway.log"
    fi
fi

echo ""
echo -e "${GREEN}Service Status:${NC}"
ps aux | grep -E 'compute_service|uvicorn.*app.main' | grep -v grep

echo ""
echo -e "${GREEN}Logs:${NC}"
echo "  Compute: tail -f /tmp/compute.log"
echo "  Gateway: tail -f /tmp/gateway.log"
