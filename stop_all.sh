#!/bin/bash

# Stop All Services Script for Linux

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Stopping AI Compute Platform Services...${NC}"

# Find and kill compute service
COMPUTE_PIDS=$(pgrep -f "compute_service")
if [ ! -z "$COMPUTE_PIDS" ]; then
    echo "Stopping compute service (PIDs: $COMPUTE_PIDS)..."
    pkill -f "compute_service"
    sleep 1
    
    # Check if still running
    if pgrep -f "compute_service" > /dev/null; then
        echo -e "${RED}Force killing compute service...${NC}"
        pkill -9 -f "compute_service"
    fi
    echo -e "${GREEN}✓ Compute service stopped${NC}"
else
    echo "Compute service not running"
fi

# Find and kill gateway
GATEWAY_PIDS=$(pgrep -f "uvicorn.*app.main:app")
if [ ! -z "$GATEWAY_PIDS" ]; then
    echo "Stopping gateway (PIDs: $GATEWAY_PIDS)..."
    pkill -f "uvicorn.*app.main:app"
    sleep 1
    
    # Check if still running
    if pgrep -f "uvicorn.*app.main:app" > /dev/null; then
        echo -e "${RED}Force killing gateway...${NC}"
        pkill -9 -f "uvicorn.*app.main:app"
    fi
    echo -e "${GREEN}✓ Gateway stopped${NC}"
else
    echo "Gateway not running"
fi

echo ""
echo -e "${GREEN}All services stopped${NC}"
