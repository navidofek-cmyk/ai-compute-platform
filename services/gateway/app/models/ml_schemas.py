from pydantic import BaseModel
from typing import List, Optional

class MLInferenceRequest(BaseModel):
    """Request for ML inference"""
    model_name: str
    input_data: List[float]
    input_shape: List[int]
    apply_softmax: bool = True
    top_k: int = 5

class MLInferenceResponse(BaseModel):
    """Response from ML inference"""
    output: List[float]
    probabilities: Optional[List[float]] = None
    top_classes: Optional[List[int]] = None
    top_probabilities: Optional[List[float]] = None
    inference_time_ms: float
    model_info: str

class ImageClassificationRequest(BaseModel):
    """Request for image classification"""
    image_data: List[float]  # Flattened image array
    model_name: str = "mnist"
    top_k: int = 5

class ImageClassificationResponse(BaseModel):
    """Response from image classification"""
    predictions: List[dict]  # List of {"class": int, "probability": float}
    inference_time_ms: float
