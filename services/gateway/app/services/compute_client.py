import grpc
import sys
from pathlib import Path
from typing import Optional
from tenacity import retry, stop_after_attempt, wait_exponential
import structlog

# Import generated protobuf files
from app import compute_pb2
from app import compute_pb2_grpc

from app.config import get_settings
from app.models.schemas import (
    MatrixMultiplyRequest, MatrixMultiplyResponse,
    StatsAnalysisRequest, StatsAnalysisResponse,
    MonteCarloRequest, MonteCarloResponse,
    VectorOperationRequest, VectorOperationResponse
)

logger = structlog.get_logger()


class ComputeServiceClient:
    """gRPC client for compute service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.channel: Optional[grpc.Channel] = None
        self.stub: Optional[compute_pb2_grpc.ComputeServiceStub] = None
        self._connect()
    
    def _connect(self):
        """Establish gRPC connection"""
        try:
            self.channel = grpc.insecure_channel(
                self.settings.compute_service_url,
                options=[
                    ('grpc.max_send_message_length', 100 * 1024 * 1024),
                    ('grpc.max_receive_message_length', 100 * 1024 * 1024),
                ]
            )
            self.stub = compute_pb2_grpc.ComputeServiceStub(self.channel)
            logger.info("connected_to_compute_service", 
                       url=self.settings.compute_service_url)
        except Exception as e:
            logger.error("failed_to_connect", error=str(e))
            raise
    
    def close(self):
        """Close gRPC channel"""
        if self.channel:
            self.channel.close()
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def multiply_matrices(
        self, 
        request: MatrixMultiplyRequest
    ) -> MatrixMultiplyResponse:
        """Multiply matrices via gRPC"""
        try:
            # Flatten matrices
            flat_a = [val for row in request.matrix_a for val in row]
            flat_b = [val for row in request.matrix_b for val in row]
            
            grpc_request = compute_pb2.MatrixMultiplyRequest(
                matrix_a=flat_a,
                matrix_b=flat_b,
                rows_a=len(request.matrix_a),
                cols_a=len(request.matrix_a[0]),
                cols_b=len(request.matrix_b[0])
            )
            
            response = self.stub.MultiplyMatrices(
                grpc_request,
                timeout=self.settings.grpc_timeout
            )
            
            # Reshape result
            result_matrix = []
            for i in range(response.rows):
                row = list(response.result[i * response.cols:(i + 1) * response.cols])
                result_matrix.append(row)
            
            return MatrixMultiplyResponse(
                result=result_matrix,
                rows=response.rows,
                cols=response.cols,
                computation_time_ms=response.computation_time_ms
            )
            
        except grpc.RpcError as e:
            logger.error("grpc_error", error=str(e), code=e.code())
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def analyze_statistics(
        self,
        request: StatsAnalysisRequest
    ) -> StatsAnalysisResponse:
        """Analyze statistics via gRPC"""
        try:
            grpc_request = compute_pb2.StatsAnalysisRequest(
                data=request.data,
                operations=request.operations
            )
            
            response = self.stub.AnalyzeStatistics(
                grpc_request,
                timeout=self.settings.grpc_timeout
            )
            
            return StatsAnalysisResponse(
                mean=response.mean,
                median=response.median if response.median != 0 else None,
                stddev=response.stddev if response.stddev != 0 else None,
                variance=response.variance if response.variance != 0 else None,
                percentiles=dict(response.percentiles) if response.percentiles else None,
                min=response.min,
                max=response.max,
                count=response.count,
                computation_time_ms=response.computation_time_ms
            )
            
        except grpc.RpcError as e:
            logger.error("grpc_error", error=str(e), code=e.code())
            raise
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=10)
    )
    async def run_monte_carlo(
        self,
        request: MonteCarloRequest
    ) -> MonteCarloResponse:
        """Run Monte Carlo simulation via gRPC"""
        try:
            grpc_request = compute_pb2.MonteCarloRequest(
                iterations=request.iterations,
                dimensions=request.dimensions,
                seed=request.seed,
                simulation_type=request.simulation_type
            )
            
            response = self.stub.RunMonteCarlo(
                grpc_request,
                timeout=self.settings.grpc_timeout
            )
            
            return MonteCarloResponse(
                result=response.result,
                confidence_interval_lower=response.confidence_interval_lower,
                confidence_interval_upper=response.confidence_interval_upper,
                iterations_completed=response.iterations_completed,
                computation_time_ms=response.computation_time_ms,
                additional_metrics=dict(response.additional_metrics)
            )
            
        except grpc.RpcError as e:
            logger.error("grpc_error", error=str(e), code=e.code())
            raise
    
    def MLInference(self, request):
        """
        Execute ML inference via gRPC
        
        Args:
            request: compute_pb2.MLInferenceRequest
            
        Returns:
            compute_pb2.MLInferenceResponse
        """
        try:
            response = self.stub.MLInference(
                request,
                timeout=self.settings.grpc_timeout
            )
            return response
        except grpc.RpcError as e:
            logger.error("ml_inference_grpc_error", error=str(e), code=e.code())
            raise
    
    async def health_check(self) -> dict:
        """Check compute service health"""
        try:
            grpc_request = compute_pb2.HealthCheckRequest()
            response = self.stub.HealthCheck(
                grpc_request,
                timeout=5
            )
            
            return {
                "status": response.status,
                "uptime_seconds": response.uptime_seconds,
                "total_requests": response.total_requests,
                "avg_response_time_ms": response.avg_response_time_ms
            }
        except Exception as e:
            logger.error("health_check_failed", error=str(e))
            return {"status": "unhealthy", "error": str(e)}


# Global client instance
_client: Optional[ComputeServiceClient] = None


def get_compute_client() -> ComputeServiceClient:
    """Get or create compute service client"""
    global _client
    if _client is None:
        _client = ComputeServiceClient()
    return _client


def close_compute_client():
    """Close compute service client"""
    global _client
    if _client is not None:
        _client.close()
        _client = None
