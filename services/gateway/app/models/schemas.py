from pydantic import BaseModel, Field, validator
from typing import List, Dict, Optional


class MatrixMultiplyRequest(BaseModel):
    """Request for matrix multiplication"""
    matrix_a: List[List[float]] = Field(..., description="First matrix (rows x cols)")
    matrix_b: List[List[float]] = Field(..., description="Second matrix (rows x cols)")
    
    @validator('matrix_a', 'matrix_b')
    def validate_matrix(cls, v):
        if not v or not all(len(row) == len(v[0]) for row in v):
            raise ValueError("Matrix must be rectangular (all rows same length)")
        return v
    
    @validator('matrix_b')
    def validate_dimensions(cls, v, values):
        if 'matrix_a' in values:
            matrix_a = values['matrix_a']
            if len(matrix_a[0]) != len(v):
                raise ValueError("Matrix dimensions incompatible for multiplication")
        return v


class MatrixMultiplyResponse(BaseModel):
    """Response for matrix multiplication"""
    result: List[List[float]]
    rows: int
    cols: int
    computation_time_ms: float


class StatsAnalysisRequest(BaseModel):
    """Request for statistical analysis"""
    data: List[float] = Field(..., min_items=1, description="Data points to analyze")
    operations: List[str] = Field(
        default=["mean", "stddev", "percentiles"],
        description="Statistical operations to perform"
    )
    
    @validator('operations')
    def validate_operations(cls, v):
        valid_ops = {"mean", "median", "stddev", "variance", "percentiles"}
        invalid = set(v) - valid_ops
        if invalid:
            raise ValueError(f"Invalid operations: {invalid}. Valid: {valid_ops}")
        return v


class StatsAnalysisResponse(BaseModel):
    """Response for statistical analysis"""
    mean: float
    median: Optional[float] = None
    stddev: Optional[float] = None
    variance: Optional[float] = None
    percentiles: Optional[Dict[int, float]] = None
    min: float
    max: float
    count: int
    computation_time_ms: float


class MonteCarloRequest(BaseModel):
    """Request for Monte Carlo simulation"""
    iterations: int = Field(..., gt=0, le=10_000_000, description="Number of iterations")
    dimensions: int = Field(default=2, ge=1, le=10, description="Problem dimensions")
    seed: int = Field(default=42, description="Random seed for reproducibility")
    simulation_type: str = Field(
        default="pi_estimation",
        description="Type of simulation: pi_estimation, option_pricing, integration"
    )
    
    @validator('simulation_type')
    def validate_simulation_type(cls, v):
        valid_types = {"pi_estimation", "option_pricing", "integration"}
        if v not in valid_types:
            raise ValueError(f"Invalid simulation type. Valid: {valid_types}")
        return v


class MonteCarloResponse(BaseModel):
    """Response for Monte Carlo simulation"""
    result: float
    confidence_interval_lower: float
    confidence_interval_upper: float
    iterations_completed: int
    computation_time_ms: float
    additional_metrics: Dict[str, float] = {}


class VectorOperationRequest(BaseModel):
    """Request for vector operations"""
    vector_a: List[float] = Field(..., min_items=1)
    vector_b: List[float] = Field(..., min_items=1)
    operation: str = Field(..., description="dot_product, cross_product, norm, distance")
    
    @validator('operation')
    def validate_operation(cls, v):
        valid_ops = {"dot_product", "cross_product", "norm", "distance"}
        if v not in valid_ops:
            raise ValueError(f"Invalid operation. Valid: {valid_ops}")
        return v
    
    @validator('vector_b')
    def validate_vectors(cls, v, values):
        if 'vector_a' in values and 'operation' in values:
            vector_a = values['vector_a']
            operation = values['operation']
            
            if operation == "cross_product" and (len(vector_a) != 3 or len(v) != 3):
                raise ValueError("Cross product requires 3D vectors")
            
            if operation in {"dot_product", "distance"} and len(vector_a) != len(v):
                raise ValueError(f"{operation} requires same-length vectors")
        return v


class VectorOperationResponse(BaseModel):
    """Response for vector operations"""
    result_vector: Optional[List[float]] = None
    result_scalar: Optional[float] = None
    computation_time_ms: float


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    service: str
    version: str
    compute_service_status: str
    uptime_seconds: Optional[float] = None


class ErrorResponse(BaseModel):
    """Error response"""
    error: str
    detail: Optional[str] = None
    request_id: Optional[str] = None
