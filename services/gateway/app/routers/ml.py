from fastapi import APIRouter, HTTPException
from app.models.ml_schemas import (
    MLInferenceRequest,
    MLInferenceResponse,
    ImageClassificationRequest,
    ImageClassificationResponse
)
from app.services.compute_client import get_compute_client
from app import compute_pb2
import time

router = APIRouter(prefix="/api/v1/ml", tags=["Machine Learning"])

@router.post("/inference", response_model=MLInferenceResponse)
async def ml_inference(request: MLInferenceRequest):
    """
    Run neural network inference on input data
    
    - **model_name**: Name of the model to use (e.g., "mnist")
    - **input_data**: Flattened input array
    - **input_shape**: Shape of input tensor [batch, channels, height, width]
    - **apply_softmax**: Whether to apply softmax to outputs
    - **top_k**: Number of top predictions to return
    """
    try:
        client = get_compute_client()
        
        # Create gRPC request
        grpc_request = compute_pb2.MLInferenceRequest(
            model_name=request.model_name,
            input_data=request.input_data,
            input_shape=request.input_shape,
            apply_softmax=request.apply_softmax,
            top_k=request.top_k
        )
        
        # Call C++ service
        response = client.MLInference(grpc_request)
        
        # Convert to response model
        return MLInferenceResponse(
            output=list(response.output),
            probabilities=list(response.probabilities) if response.probabilities else None,
            top_classes=list(response.top_classes) if response.top_classes else None,
            top_probabilities=list(response.top_probabilities) if response.top_probabilities else None,
            inference_time_ms=response.inference_time_ms,
            model_info=response.model_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"ML inference failed: {str(e)}")

@router.post("/classify", response_model=ImageClassificationResponse)
async def classify_image(request: ImageClassificationRequest):
    """
    Classify an image using a pretrained model
    
    - **image_data**: Flattened image array (e.g., 784 floats for 28x28 MNIST)
    - **model_name**: Model to use for classification
    - **top_k**: Number of top predictions to return
    """
    try:
        # Determine input shape based on model
        if request.model_name == "mnist":
            input_shape = [1, 1, 28, 28]
        else:
            # Default shape
            input_shape = [1, len(request.image_data)]
        
        # Create inference request
        inference_request = MLInferenceRequest(
            model_name=request.model_name,
            input_data=request.image_data,
            input_shape=input_shape,
            apply_softmax=True,
            top_k=request.top_k
        )
        
        # Run inference
        result = await ml_inference(inference_request)
        
        # Format predictions
        predictions = []
        if result.top_classes and result.top_probabilities:
            for cls, prob in zip(result.top_classes, result.top_probabilities):
                predictions.append({
                    "class": cls,
                    "probability": float(prob)
                })
        
        return ImageClassificationResponse(
            predictions=predictions,
            inference_time_ms=result.inference_time_ms
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image classification failed: {str(e)}")

@router.get("/models")
async def list_models():
    """
    List available ML models
    """
    return {
        "available_models": [
            {
                "name": "mnist",
                "description": "MNIST digit classification (0-9)",
                "input_shape": [1, 1, 28, 28],
                "output_classes": 10,
                "type": "image_classification"
            }
        ]
    }

@router.get("/health")
async def ml_health():
    """
    Check ML inference service health
    """
    try:
        client = get_compute_client()
        # Simple health check - try to connect
        return {
            "status": "healthy",
            "message": "ML inference service is operational"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"ML service unavailable: {str(e)}")
