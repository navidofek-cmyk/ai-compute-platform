#pragma once

#include <grpcpp/grpcpp.h>
#include <memory>
#include <string>
#include "compute_engine.hpp"
#include "compute.grpc.pb.h"

namespace compute {

class ComputeServiceImpl final : public ComputeService::Service {
public:
    explicit ComputeServiceImpl(std::shared_ptr<ComputeEngine> engine);

    grpc::Status MultiplyMatrices(
        grpc::ServerContext* context,
        const MatrixMultiplyRequest* request,
        MatrixMultiplyResponse* response) override;

    grpc::Status AnalyzeStatistics(
        grpc::ServerContext* context,
        const StatsAnalysisRequest* request,
        StatsAnalysisResponse* response) override;

    grpc::Status RunMonteCarlo(
        grpc::ServerContext* context,
        const MonteCarloRequest* request,
        MonteCarloResponse* response) override;

    grpc::Status VectorOperation(
        grpc::ServerContext* context,
        const VectorOperationRequest* request,
        VectorOperationResponse* response) override;

    grpc::Status HealthCheck(
        grpc::ServerContext* context,
        const HealthCheckRequest* request,
        HealthCheckResponse* response) override;

    grpc::Status MLInference(
        grpc::ServerContext* context,
        const MLInferenceRequest* request,
        MLInferenceResponse* response) override;

    grpc::Status MLBatchInference(
        grpc::ServerContext* context,
        const MLBatchInferenceRequest* request,
        MLBatchInferenceResponse* response) override;

private:
    std::shared_ptr<ComputeEngine> engine_;
    std::chrono::steady_clock::time_point start_time_;
    std::atomic<uint64_t> total_requests_{0};
    std::mutex metrics_mutex_;
    double total_response_time_{0.0};
};

class Server {
public:
    explicit Server(const std::string& address, int thread_pool_size = 8);
    
    void run();
    void shutdown();

private:
    std::string server_address_;
    std::unique_ptr<grpc::Server> server_;
    std::shared_ptr<ComputeEngine> engine_;
    std::unique_ptr<ComputeServiceImpl> service_;
};

} // namespace compute
