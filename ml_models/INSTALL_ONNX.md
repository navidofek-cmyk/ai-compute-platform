# ONNX Runtime Installation Guide

## Option 1: Download prebuilt package (Recommended)

### Linux x86_64:
```bash
# Download ONNX Runtime 1.16.3
cd /tmp
wget https://github.com/microsoft/onnxruntime/releases/download/v1.16.3/onnxruntime-linux-x64-1.16.3.tgz

# Extract
tar -xzf onnxruntime-linux-x64-1.16.3.tgz

# Install to /usr/local
sudo cp -r onnxruntime-linux-x64-1.16.3/include/* /usr/local/include/
sudo mkdir -p /usr/local/include/onnxruntime
sudo cp -r onnxruntime-linux-x64-1.16.3/include/* /usr/local/include/onnxruntime/
sudo cp onnxruntime-linux-x64-1.16.3/lib/* /usr/local/lib/
sudo ldconfig
```

### Alternative: Install via package manager

```bash
# Ubuntu/Debian (if available in repos)
sudo apt-get update
sudo apt-get install libonnxruntime-dev

# Or build from source (advanced)
git clone --recursive https://github.com/Microsoft/onnxruntime
cd onnxruntime
./build.sh --config Release --build_shared_lib --parallel
```

## Option 2: Use system-specific paths

If you install to a different location, update CMakeLists.txt:

```cmake
set(ONNXRUNTIME_ROOT_PATH "/your/path/to/onnxruntime" CACHE PATH "ONNX Runtime root directory")
```

## Verify Installation:

```bash
# Check if library is found
ldconfig -p | grep onnxruntime

# Check include files
ls -la /usr/local/include/onnxruntime/

# Test compilation
g++ -I/usr/local/include/onnxruntime -L/usr/local/lib -lonnxruntime test.cpp
```

## Windows Installation:

Download from: https://github.com/microsoft/onnxruntime/releases
Extract and add to system PATH.
