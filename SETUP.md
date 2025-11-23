# Setup and Build Instructions

## Quick Start with Docker (Recommended)

The fastest way to get the entire system running:

```bash
# Start all services
docker-compose up --build

# Access the API
curl http://localhost:8000/docs
```

## Manual Setup

### Prerequisites

**System Requirements:**
- Ubuntu 22.04 or similar Linux distribution
- Docker & Docker Compose (for containerized deployment)
- WSL2 (for Windows development)

**C++ Service:**
- g++ 11+ with C++17 support
- CMake 3.15+
- gRPC and Protocol Buffers
- Google Test (for testing)

**Python Service:**
- Python 3.11+
- pip and virtualenv

### Building the C++ Compute Service

```bash
cd services/compute

# Install dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y \
    build-essential \
    cmake \
    libgrpc++-dev \
    libprotobuf-dev \
    protobuf-compiler-grpc \
    libgtest-dev

# Generate protobuf files
mkdir -p build
cd build
protoc --grpc_out=. --cpp_out=. \
    --plugin=protoc-gen-grpc=`which grpc_cpp_plugin` \
    -I ../../proto ../../proto/compute.proto

# Build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j$(nproc)

# Run tests
ctest --verbose

# Run service
./compute_service
```

### Setting up the Python Gateway

```bash
cd services/gateway

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Generate protobuf files
python -m grpc_tools.protoc \
    -I../../proto \
    --python_out=./app/services \
    --grpc_python_out=./app/services \
    ../../proto/compute.proto

# Run tests
pytest tests/ -v --cov

# Run service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Configuration

### Environment Variables

Copy the example environment files:

```bash
cp services/compute/.env.example services/compute/.env
cp services/gateway/.env.example services/gateway/.env
```

Edit the `.env` files to customize:
- Port numbers
- Thread pool sizes
- Logging levels
- Rate limits
- Security settings

## Testing

### C++ Tests

```bash
cd services/compute/build
ctest --verbose --output-on-failure
```

### Python Tests

```bash
cd services/gateway
pytest tests/ -v --cov --cov-report=html
```

### Integration Tests

```bash
# Start services
docker-compose up -d

# Wait for services to be ready
sleep 10

# Test matrix multiplication
curl -X POST http://localhost:8000/api/v1/compute/matrix/multiply \
  -H "Content-Type: application/json" \
  -d '{"matrix_a":[[1,2],[3,4]],"matrix_b":[[5,6],[7,8]]}'

# Test statistics
curl -X POST http://localhost:8000/api/v1/compute/stats/analyze \
  -H "Content-Type: application/json" \
  -d '{"data":[1.5,2.3,4.7,3.2,5.8,1.9],"operations":["mean","stddev"]}'

# Test Monte Carlo
curl -X POST http://localhost:8000/api/v1/compute/simulation/monte-carlo \
  -H "Content-Type: application/json" \
  -d '{"iterations":100000,"dimensions":2,"seed":42,"simulation_type":"pi_estimation"}'
```

## Development Workflow

### Code Formatting

**C++:**
```bash
cd services/compute
clang-format -i src/**/*.cpp include/**/*.hpp
```

**Python:**
```bash
cd services/gateway
black app/
isort app/
flake8 app/ --max-line-length=100
mypy app/
```

### Adding New Features

1. **Define protobuf message** in `proto/compute.proto`
2. **Implement C++ backend** in `services/compute/src/`
3. **Add Python endpoint** in `services/gateway/app/routers/`
4. **Write tests** for both services
5. **Update documentation**

## Deployment

### Docker Compose (Development)

```bash
docker-compose up -d
docker-compose logs -f
```

### Production Deployment

**Build optimized images:**
```bash
docker build -t compute-service:latest -f services/compute/Dockerfile .
docker build -t gateway-service:latest -f services/gateway/Dockerfile .
```

**Push to registry:**
```bash
docker tag compute-service:latest your-registry/compute-service:latest
docker tag gateway-service:latest your-registry/gateway-service:latest
docker push your-registry/compute-service:latest
docker push your-registry/gateway-service:latest
```

### Monitoring

**Access Prometheus:**
```bash
http://localhost:9090
```

**Access Grafana:**
```bash
http://localhost:3000
# Default credentials: admin/admin
```

## Troubleshooting

### Common Issues

**gRPC connection refused:**
- Check if compute service is running: `docker-compose ps`
- Verify port mapping: `docker-compose port compute 50051`
- Check logs: `docker-compose logs compute`

**Python import errors:**
- Regenerate protobuf files
- Verify virtual environment is activated
- Check PYTHONPATH

**Build errors (C++):**
- Ensure all dependencies installed
- Clear build directory: `rm -rf build && mkdir build`
- Check CMake version: `cmake --version` (need 3.15+)

**Memory issues:**
- Reduce thread pool size in config
- Limit matrix dimensions
- Adjust Docker resource limits

## Performance Tuning

### C++ Service

- **Thread pool size:** Set `THREAD_POOL_SIZE` based on CPU cores
- **Compiler optimizations:** Use `-O3 -march=native` flags
- **SIMD:** Enable for matrix operations on compatible CPUs

### Python Service

- **Workers:** Set based on CPU cores (typically 2-4x cores)
- **Connection pooling:** Adjust gRPC channel options
- **Rate limiting:** Configure based on expected load

### System

- **Docker resources:** Allocate sufficient CPU/memory
- **Network:** Use host networking for lower latency
- **Storage:** Use volumes for persistent data

## License

MIT License - see LICENSE file for details
