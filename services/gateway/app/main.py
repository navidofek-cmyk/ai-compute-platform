from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
import structlog
import time

from app.config import get_settings
from app.routers import compute, health, ai, ml
from app.services.compute_client import get_compute_client, close_compute_client

# Configure structured logging
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.JSONRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

COMPUTE_OPERATIONS = Counter(
    'compute_operations_total',
    'Total compute operations',
    ['operation_type']
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    settings = get_settings()
    logger.info(
        "application_starting",
        name=settings.app_name,
        version=settings.app_version
    )
    
    # Initialize compute client
    try:
        get_compute_client()
        logger.info("compute_client_initialized")
    except Exception as e:
        logger.error("compute_client_init_failed", error=str(e))
    
    yield
    
    # Cleanup
    logger.info("application_shutting_down")
    close_compute_client()


# Create FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="High-performance microservice API gateway",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)


# Middleware for logging and metrics
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and track metrics"""
    start_time = time.time()
    
    # Generate request ID
    request_id = request.headers.get("X-Request-ID", f"{time.time()}")
    
    logger.info(
        "request_started",
        method=request.method,
        path=request.url.path,
        request_id=request_id
    )
    
    try:
        response = await call_next(request)
        duration = time.time() - start_time
        
        # Track metrics
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        REQUEST_DURATION.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        logger.info(
            "request_completed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration * 1000,
            request_id=request_id
        )
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            "request_failed",
            method=request.method,
            path=request.url.path,
            error=str(e),
            duration_ms=duration * 1000,
            request_id=request_id
        )
        raise


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors"""
    logger.warning(
        "validation_error",
        path=request.url.path,
        errors=exc.errors()
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation error",
            "detail": exc.errors()
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        error=str(exc),
        exc_info=True
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )


# Metrics endpoint
@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


# Include routers
app.include_router(health.router)
app.include_router(compute.router, prefix=settings.api_prefix)
app.include_router(ai.router)  # AI Assistant endpoints
app.include_router(ml.router)  # ML Inference endpoints


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        workers=settings.workers,
        log_level=settings.log_level.lower(),
        reload=settings.debug
    )
