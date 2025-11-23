# Multi-stage build for Python gateway service

FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY app/ ./app/
COPY proto/ ./proto/

# Generate protobuf files
RUN python -m grpc_tools.protoc \
    -I./proto \
    --python_out=./app/services \
    --grpc_python_out=./app/services \
    ./proto/compute.proto

# Create non-root user
RUN useradd -r -s /bin/false gateway && \
    chown -R gateway:gateway /app

USER gateway

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health')" || exit 1

# Environment variables
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=info
ENV COMPUTE_SERVICE_URL=compute:50051

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
