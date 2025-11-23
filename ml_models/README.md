# ML Models Directory

This directory contains machine learning models and training scripts for the AI Compute Platform.

## Structure

```
ml_models/
├── train_mnist.py          # Training script for MNIST digit classification
├── requirements.txt        # Python dependencies for training
├── INSTALL_ONNX.md        # ONNX Runtime installation guide
├── mnist_model.onnx       # Trained MNIST model (generated after training)
└── README.md              # This file
```

## Quick Start

### 1. Install Dependencies

```bash
cd ml_models
pip install -r requirements.txt
```

### 2. Train MNIST Model

```bash
python train_mnist.py
```

This will:
- Download MNIST dataset automatically
- Train a simple feedforward neural network (5 epochs)
- Export the model to `mnist_model.onnx`
- Achieve ~97-98% test accuracy

Training takes approximately 2-5 minutes on CPU.

### 3. Install ONNX Runtime (for C++ inference)

Follow instructions in `INSTALL_ONNX.md` to install ONNX Runtime for C++.

Quick install on Linux:
```bash
cd /tmp
wget https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-linux-x64-1.16.3.tgz
tar -xzf onnxruntime-linux-x64-1.16.3.tgz
sudo cp -r onnxruntime-linux-x64-1.16.3/include/* /usr/local/include/onnxruntime/
sudo cp onnxruntime-linux-x64-1.16.3/lib/* /usr/local/lib/
sudo ldconfig
```

### 4. Copy Model to Services

```bash
# Copy ONNX model to compute service directory
cp mnist_model.onnx ../services/compute/models/
```

### 5. Rebuild Compute Service

```bash
cd ../services/compute
mkdir -p build && cd build
cmake ..
make -j4
```

## Using the ML Inference API

Once the service is running, you can use the ML inference endpoints:

### Classify an Image

```bash
curl -X POST http://localhost:8000/api/v1/ml/classify \
  -H "Content-Type: application/json" \
  -d '{
    "image_data": [0.0, 0.0, ..., 0.5, 0.9, ...],  # 784 floats for 28x28 image
    "model_name": "mnist",
    "top_k": 5
  }'
```

### Raw Inference

```bash
curl -X POST http://localhost:8000/api/v1/ml/inference \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "mnist",
    "input_data": [...],
    "input_shape": [1, 1, 28, 28],
    "apply_softmax": true,
    "top_k": 5
  }'
```

### List Available Models

```bash
curl http://localhost:8000/api/v1/ml/models
```

## Model Details

### MNIST Classifier

- **Architecture**: Feedforward neural network
  - Input: 784 (28x28 flattened image)
  - Hidden Layer 1: 128 neurons + ReLU
  - Hidden Layer 2: 64 neurons + ReLU
  - Output: 10 classes (digits 0-9)
  
- **Input Format**: 
  - Grayscale image normalized to [0, 1]
  - Flattened to 784 floats
  - Shape: [1, 1, 28, 28]

- **Output Format**:
  - 10 logits (or probabilities if softmax applied)
  - Top-K predictions with confidence scores

- **Performance**:
  - Accuracy: ~97-98% on MNIST test set
  - Inference time: <1ms on CPU
  - Model size: ~400 KB

## Adding New Models

To add a new model:

1. Create training script in this directory
2. Export model to ONNX format
3. Copy `.onnx` file to `services/compute/models/`
4. Add model metadata to `services/gateway/app/routers/ml.py`
5. Rebuild and restart services

## Troubleshooting

**ONNX Runtime not found during build:**
- Follow `INSTALL_ONNX.md` to install ONNX Runtime
- Verify installation: `ldconfig -p | grep onnxruntime`
- Update CMakeLists.txt if installed to custom location

**Model not found error:**
- Ensure `mnist_model.onnx` exists in `services/compute/models/`
- Check file permissions
- Verify path in service configuration

**Low inference accuracy:**
- Ensure input data is normalized correctly [0, 1]
- Verify input shape matches model expectations
- Check that model was trained successfully

## Performance Optimization

For better performance:

1. **Use GPU**: Install ONNX Runtime with CUDA support
2. **Batch inference**: Send multiple images in one request
3. **Model quantization**: Convert model to INT8 for faster inference
4. **SIMD optimization**: Build ONNX Runtime with AVX/AVX2 flags

## Resources

- [ONNX Runtime Documentation](https://onnxruntime.ai/docs/)
- [PyTorch ONNX Export Guide](https://pytorch.org/docs/stable/onnx.html)
- [MNIST Dataset](http://yann.lecun.com/exdb/mnist/)
