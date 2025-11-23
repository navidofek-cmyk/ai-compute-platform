# Multi-stage build for C++ compute service

# Stage 1: Builder
FROM ubuntu:22.04 AS builder

# Install dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    pkg-config \
    autoconf \
    libtool \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install gRPC and protobuf
RUN apt-get update && apt-get install -y \
    libgrpc++-dev \
    libprotobuf-dev \
    protobuf-compiler-grpc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy proto files and source
COPY proto/ /app/proto/
COPY services/compute/ /app/

# Build
RUN mkdir -p build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc)

# Stage 2: Runtime
FROM ubuntu:22.04

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    libgrpc++1.43 \
    libprotobuf23 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/build/compute_service /app/compute_service

# Create non-root user
RUN useradd -r -s /bin/false compute && \
    chown -R compute:compute /app

USER compute

# Expose gRPC port
EXPOSE 50051

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
    CMD grpc_health_probe -addr=:50051 || exit 1

# Set environment variables
ENV GRPC_PORT=50051
ENV THREAD_POOL_SIZE=8
ENV LOG_LEVEL=info

CMD ["./compute_service"]
