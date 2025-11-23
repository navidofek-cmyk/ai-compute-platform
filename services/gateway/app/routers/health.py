from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.services.compute_client import get_compute_client
from app.config import get_settings
import time

router = APIRouter(tags=["health"])

start_time = time.time()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check the health status of the gateway and compute services"
)
async def health_check():
    """Health check endpoint"""
    settings = get_settings()
    
    # Check compute service
    client = get_compute_client()
    compute_health = await client.health_check()
    compute_status = compute_health.get("status", "unknown")
    
    return HealthResponse(
        status="healthy" if compute_status == "healthy" else "degraded",
        service=settings.app_name,
        version=settings.app_version,
        compute_service_status=compute_status,
        uptime_seconds=time.time() - start_time
    )


@router.get("/")
async def root():
    """Root endpoint"""
    settings = get_settings()
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }
