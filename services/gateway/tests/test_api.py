import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_health_check():
    """Test health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "service" in data


@pytest.mark.asyncio
async def test_matrix_multiplication():
    """Test matrix multiplication endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "matrix_a": [[1, 2], [3, 4]],
            "matrix_b": [[5, 6], [7, 8]]
        }
        response = await client.post("/api/v1/compute/matrix/multiply", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "result" in data
        assert "computation_time_ms" in data


@pytest.mark.asyncio
async def test_stats_analysis():
    """Test statistical analysis endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "data": [1.5, 2.3, 4.7, 3.2, 5.8, 1.9],
            "operations": ["mean", "stddev"]
        }
        response = await client.post("/api/v1/compute/stats/analyze", json=payload)
        
        assert response.status_code == 200
        data = response.json()
        assert "mean" in data
        assert "stddev" in data


@pytest.mark.asyncio
async def test_invalid_matrix():
    """Test validation for invalid matrix"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        payload = {
            "matrix_a": [[1, 2], [3]],  # Invalid: not rectangular
            "matrix_b": [[5, 6], [7, 8]]
        }
        response = await client.post("/api/v1/compute/matrix/multiply", json=payload)
        
        assert response.status_code == 422  # Validation error
