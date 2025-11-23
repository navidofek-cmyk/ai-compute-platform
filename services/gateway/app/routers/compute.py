from fastapi import APIRouter, HTTPException, status
from app.models.schemas import (
    MatrixMultiplyRequest, MatrixMultiplyResponse,
    StatsAnalysisRequest, StatsAnalysisResponse,
    MonteCarloRequest, MonteCarloResponse,
    VectorOperationRequest, VectorOperationResponse
)
from app.services.compute_client import get_compute_client
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/compute", tags=["compute"])


@router.post(
    "/matrix/multiply",
    response_model=MatrixMultiplyResponse,
    summary="Multiply two matrices",
    description="Performs high-performance matrix multiplication using C++ backend"
)
async def multiply_matrices(request: MatrixMultiplyRequest):
    """Multiply two matrices"""
    try:
        logger.info(
            "matrix_multiply_request",
            rows_a=len(request.matrix_a),
            cols_a=len(request.matrix_a[0]),
            rows_b=len(request.matrix_b),
            cols_b=len(request.matrix_b[0])
        )
        
        client = get_compute_client()
        result = await client.multiply_matrices(request)
        
        logger.info(
            "matrix_multiply_success",
            computation_time_ms=result.computation_time_ms
        )
        
        return result
        
    except Exception as e:
        logger.error("matrix_multiply_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Matrix multiplication failed: {str(e)}"
        )


@router.post(
    "/stats/analyze",
    response_model=StatsAnalysisResponse,
    summary="Analyze statistical data",
    description="Performs comprehensive statistical analysis on numerical data"
)
async def analyze_statistics(request: StatsAnalysisRequest):
    """Analyze statistical data"""
    try:
        logger.info(
            "stats_analysis_request",
            data_points=len(request.data),
            operations=request.operations
        )
        
        client = get_compute_client()
        result = await client.analyze_statistics(request)
        
        logger.info(
            "stats_analysis_success",
            computation_time_ms=result.computation_time_ms
        )
        
        return result
        
    except Exception as e:
        logger.error("stats_analysis_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Statistical analysis failed: {str(e)}"
        )


@router.post(
    "/simulation/monte-carlo",
    response_model=MonteCarloResponse,
    summary="Run Monte Carlo simulation",
    description="Performs Monte Carlo simulations for various problem types"
)
async def run_monte_carlo(request: MonteCarloRequest):
    """Run Monte Carlo simulation"""
    try:
        logger.info(
            "monte_carlo_request",
            iterations=request.iterations,
            dimensions=request.dimensions,
            simulation_type=request.simulation_type
        )
        
        client = get_compute_client()
        result = await client.run_monte_carlo(request)
        
        logger.info(
            "monte_carlo_success",
            computation_time_ms=result.computation_time_ms,
            result=result.result
        )
        
        return result
        
    except Exception as e:
        logger.error("monte_carlo_error", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Monte Carlo simulation failed: {str(e)}"
        )
