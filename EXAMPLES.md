# API Examples and Usage Guide

## Authentication

If API key authentication is enabled, include the key in headers:

```bash
curl -H "X-API-Key: your-api-key-here" http://localhost:8000/health
```

## Matrix Operations

### Basic Matrix Multiplication

```bash
curl -X POST http://localhost:8000/api/v1/compute/matrix/multiply \
  -H "Content-Type: application/json" \
  -d '{
    "matrix_a": [[1, 2], [3, 4]],
    "matrix_b": [[5, 6], [7, 8]]
  }'
```

**Response:**
```json
{
  "result": [[19, 22], [43, 50]],
  "rows": 2,
  "cols": 2,
  "computation_time_ms": 0.15
}
```

### Large Matrix Multiplication

```bash
# Generate 100x100 matrices using Python
python3 << 'EOF'
import requests
import random

size = 100
matrix_a = [[random.random() for _ in range(size)] for _ in range(size)]
matrix_b = [[random.random() for _ in range(size)] for _ in range(size)]

response = requests.post(
    "http://localhost:8000/api/v1/compute/matrix/multiply",
    json={"matrix_a": matrix_a, "matrix_b": matrix_b}
)

print(f"Status: {response.status_code}")
print(f"Time: {response.json()['computation_time_ms']}ms")
EOF
```

## Statistical Analysis

### Basic Statistics

```bash
curl -X POST http://localhost:8000/api/v1/compute/stats/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "data": [1.5, 2.3, 4.7, 3.2, 5.8, 1.9, 6.4, 2.8, 3.9, 4.1],
    "operations": ["mean", "stddev", "percentiles"]
  }'
```

**Response:**
```json
{
  "mean": 3.66,
  "median": 3.55,
  "stddev": 1.58,
  "variance": 2.49,
  "percentiles": {
    "25": 2.35,
    "50": 3.55,
    "75": 4.65,
    "95": 6.07,
    "99": 6.35
  },
  "min": 1.5,
  "max": 6.4,
  "count": 10,
  "computation_time_ms": 0.08
}
```

### Time Series Analysis

```python
import requests
import numpy as np

# Generate time series data
time_series = list(np.random.normal(100, 15, 10000))

response = requests.post(
    "http://localhost:8000/api/v1/compute/stats/analyze",
    json={
        "data": time_series,
        "operations": ["mean", "stddev", "variance", "percentiles"]
    }
)

stats = response.json()
print(f"Mean: {stats['mean']:.2f}")
print(f"Std Dev: {stats['stddev']:.2f}")
print(f"95th Percentile: {stats['percentiles']['95']:.2f}")
print(f"Computation Time: {stats['computation_time_ms']}ms")
```

## Monte Carlo Simulations

### Estimate Pi

```bash
curl -X POST http://localhost:8000/api/v1/compute/simulation/monte-carlo \
  -H "Content-Type: application/json" \
  -d '{
    "iterations": 1000000,
    "dimensions": 2,
    "seed": 42,
    "simulation_type": "pi_estimation"
  }'
```

**Response:**
```json
{
  "result": 3.14159,
  "confidence_interval_lower": 3.14102,
  "confidence_interval_upper": 3.14216,
  "iterations_completed": 1000000,
  "computation_time_ms": 245.3,
  "additional_metrics": {
    "actual_pi": 3.14159265,
    "error": 0.00000265,
    "error_percentage": 0.000084
  }
}
```

### Option Pricing (Black-Scholes Monte Carlo)

```bash
curl -X POST http://localhost:8000/api/v1/compute/simulation/monte-carlo \
  -H "Content-Type: application/json" \
  -d '{
    "iterations": 100000,
    "dimensions": 252,
    "seed": 42,
    "simulation_type": "option_pricing"
  }'
```

**Response:**
```json
{
  "result": 10.45,
  "confidence_interval_lower": 10.38,
  "confidence_interval_upper": 10.52,
  "iterations_completed": 100000,
  "computation_time_ms": 1834.7,
  "additional_metrics": {
    "strike": 100.0,
    "spot": 100.0,
    "volatility": 0.2,
    "time_steps": 252.0
  }
}
```

### Numerical Integration

```bash
curl -X POST http://localhost:8000/api/v1/compute/simulation/monte-carlo \
  -H "Content-Type: application/json" \
  -d '{
    "iterations": 500000,
    "dimensions": 3,
    "seed": 42,
    "simulation_type": "integration"
  }'
```

## Python Client Example

```python
import requests
from typing import List, Dict, Any

class ComputeClient:
    """Python client for the compute API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_prefix = "/api/v1"
    
    def multiply_matrices(
        self, 
        matrix_a: List[List[float]], 
        matrix_b: List[List[float]]
    ) -> Dict[str, Any]:
        """Multiply two matrices"""
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/compute/matrix/multiply",
            json={"matrix_a": matrix_a, "matrix_b": matrix_b}
        )
        response.raise_for_status()
        return response.json()
    
    def analyze_stats(
        self,
        data: List[float],
        operations: List[str] = None
    ) -> Dict[str, Any]:
        """Analyze statistical data"""
        if operations is None:
            operations = ["mean", "stddev", "percentiles"]
        
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/compute/stats/analyze",
            json={"data": data, "operations": operations}
        )
        response.raise_for_status()
        return response.json()
    
    def monte_carlo(
        self,
        iterations: int,
        dimensions: int = 2,
        seed: int = 42,
        simulation_type: str = "pi_estimation"
    ) -> Dict[str, Any]:
        """Run Monte Carlo simulation"""
        response = requests.post(
            f"{self.base_url}{self.api_prefix}/compute/simulation/monte-carlo",
            json={
                "iterations": iterations,
                "dimensions": dimensions,
                "seed": seed,
                "simulation_type": simulation_type
            }
        )
        response.raise_for_status()
        return response.json()

# Usage
client = ComputeClient()

# Matrix multiplication
result = client.multiply_matrices(
    [[1, 2], [3, 4]],
    [[5, 6], [7, 8]]
)
print(f"Matrix result: {result['result']}")

# Statistics
stats = client.analyze_stats([1, 2, 3, 4, 5])
print(f"Mean: {stats['mean']}, StdDev: {stats['stddev']}")

# Monte Carlo
pi_estimate = client.monte_carlo(1000000, simulation_type="pi_estimation")
print(f"Pi estimate: {pi_estimate['result']}")
```

## Batch Processing Example

```python
import requests
import concurrent.futures
import time

def process_batch(batch_id: int, data: list) -> dict:
    """Process a batch of data"""
    response = requests.post(
        "http://localhost:8000/api/v1/compute/stats/analyze",
        json={"data": data, "operations": ["mean", "stddev"]}
    )
    return {"batch_id": batch_id, "result": response.json()}

# Process multiple batches in parallel
batches = [list(range(i*1000, (i+1)*1000)) for i in range(10)]

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(process_batch, i, batch) 
        for i, batch in enumerate(batches)
    ]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]

elapsed = time.time() - start
print(f"Processed {len(batches)} batches in {elapsed:.2f}s")
```

## Load Testing

```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test with 1000 requests, 10 concurrent
ab -n 1000 -c 10 -p payload.json -T application/json \
   http://localhost:8000/api/v1/compute/stats/analyze
```

**payload.json:**
```json
{"data": [1,2,3,4,5,6,7,8,9,10], "operations": ["mean"]}
```

## Error Handling

```python
import requests

try:
    response = requests.post(
        "http://localhost:8000/api/v1/compute/matrix/multiply",
        json={
            "matrix_a": [[1, 2], [3]],  # Invalid: not rectangular
            "matrix_b": [[5, 6], [7, 8]]
        },
        timeout=10
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 422:
        print("Validation error:", e.response.json())
    elif e.response.status_code == 500:
        print("Server error:", e.response.json())
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Failed to connect to service")
```

## Monitoring and Metrics

### Check Service Health

```bash
curl http://localhost:8000/health
```

### View Prometheus Metrics

```bash
curl http://localhost:8000/metrics
```

### API Documentation

Interactive API docs available at:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
