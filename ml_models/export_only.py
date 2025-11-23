#!/usr/bin/env python3
import torch
from train_mnist import MNISTNet

# Load model
model = MNISTNet()
model.load_state_dict(torch.load('mnist_model.pth', weights_only=True))
model.eval()

# Create dummy input
dummy_input = torch.randn(1, 784)

# Export to ONNX with opset 9 (supported by ONNX Runtime 1.16.3)
print("\nExporting model to mnist_model.onnx...")
torch.onnx.export(
    model,
    dummy_input,
    'mnist_model.onnx',
    export_params=True,
    opset_version=9,  # Lower version for compatibility
    do_constant_folding=True,
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={
        'input': {0: 'batch_size'},
        'output': {0: 'batch_size'}
    }
)

import os
model_size = os.path.getsize('mnist_model.onnx')
print(f"Model exported successfully to mnist_model.onnx")
print(f"Model size: {model_size / 1024:.2f} KB")
print("Export complete!")
