#!/usr/bin/env python3
"""Test direct gRPC call to MLInference"""

import sys
sys.path.insert(0, "/mnt/c/ubuntu/cpp/aicpp/cppplay/services/gateway")

import grpc
from app import compute_pb2
from app import compute_pb2_grpc

# Create test data - simple 28x28 image
test_data = [0.0] * 784
test_data[350:430] = [1.0] * 80  # Vertical line

# Connect to service
channel = grpc.insecure_channel('localhost:50051')
stub = compute_pb2_grpc.ComputeServiceStub(channel)

# Create request
request = compute_pb2.MLInferenceRequest(
    model_name="mnist",
    input_data=test_data,
    input_shape=[1, 1, 28, 28],
    apply_softmax=True,
    top_k=5
)

print("Sending MLInference request...")
print(f"  Model: {request.model_name}")
print(f"  Input shape: {request.input_shape}")
print(f"  Data size: {len(request.input_data)}")

try:
    response = stub.MLInference(request)
    print("\n✅ SUCCESS!")
    print(f"  Inference time: {response.inference_time_ms:.2f}ms")
    print(f"  Model info: {response.model_info}")
    print(f"  Top classes: {response.top_classes}")
    print(f"  Top probabilities: {response.top_probabilities}")
except grpc.RpcError as e:
    print(f"\n❌ ERROR: {e.code()}")
    print(f"  Details: {e.details()}")
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
finally:
    channel.close()
