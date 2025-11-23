#include "server.hpp"
#include "utils/logger.hpp"
#include <chrono>

namespace compute {

ComputeServiceImpl::ComputeServiceImpl(std::shared_ptr<ComputeEngine> engine)
    : engine_(engine), start_time_(std::chrono::steady_clock::now()) {
    LOG_INFO("ComputeServiceImpl initialized");
}

grpc::Status ComputeServiceImpl::MultiplyMatrices(
    grpc::ServerContext* context,
    const MatrixMultiplyRequest* request,
    MatrixMultiplyResponse* response) {
    
    auto start = std::chrono::high_resolution_clock::now();
    total_requests_++;
    
    try {
        // Convert proto data to matrices
        MatrixOps::Matrix a(request->rows_a(), request->cols_a());
        MatrixOps::Matrix b(request->cols_a(), request->cols_b());
        
        std::copy(request->matrix_a().begin(), request->matrix_a().end(), a.data.begin());
        std::copy(request->matrix_b().begin(), request->matrix_b().end(), b.data.begin());
        
        // Perform multiplication
        auto result = engine_->multiplyMatrices(a, b);
        
        // Set response
        for (double val : result.data) {
            response->add_result(val);
        }
        response->set_rows(result.rows);
        response->set_cols(result.cols);
        
        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration<double, std::milli>(end - start).count();
        response->set_computation_time_ms(elapsed);
        {
            std::lock_guard<std::mutex> lock(metrics_mutex_);
            total_response_time_ += elapsed;
        }
        
        LOG_INFO("Matrix multiplication completed in", elapsed, "ms");
        return grpc::Status::OK;
        
    } catch (const std::exception& e) {
        LOG_ERROR("Matrix multiplication failed:", e.what());
        return grpc::Status(grpc::StatusCode::INTERNAL, e.what());
    }
}

grpc::Status ComputeServiceImpl::AnalyzeStatistics(
    grpc::ServerContext* context,
    const StatsAnalysisRequest* request,
    StatsAnalysisResponse* response) {
    
    auto start = std::chrono::high_resolution_clock::now();
    total_requests_++;
    
    try {
        std::vector<double> data(request->data().begin(), request->data().end());
        std::vector<std::string> ops(request->operations().begin(), request->operations().end());
        
        auto stats = engine_->analyzeStatistics(data, ops);
        
        response->set_mean(stats.mean);
        response->set_median(stats.median);
        response->set_stddev(stats.stddev);
        response->set_variance(stats.variance);
        response->set_min(stats.min);
        response->set_max(stats.max);
        response->set_count(stats.count);
        
        for (const auto& [percentile, value] : stats.percentiles) {
            (*response->mutable_percentiles())[percentile] = value;
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration<double, std::milli>(end - start).count();
        response->set_computation_time_ms(elapsed);
        {
            std::lock_guard<std::mutex> lock(metrics_mutex_);
            total_response_time_ += elapsed;
        }
        
        LOG_INFO("Statistical analysis completed in", elapsed, "ms");
        return grpc::Status::OK;
        
    } catch (const std::exception& e) {
        LOG_ERROR("Statistical analysis failed:", e.what());
        return grpc::Status(grpc::StatusCode::INTERNAL, e.what());
    }
}

grpc::Status ComputeServiceImpl::RunMonteCarlo(
    grpc::ServerContext* context,
    const MonteCarloRequest* request,
    MonteCarloResponse* response) {
    
    auto start = std::chrono::high_resolution_clock::now();
    total_requests_++;
    
    try {
        auto result = engine_->runMonteCarlo(
            request->iterations(),
            request->dimensions(),
            request->seed(),
            request->simulation_type()
        );
        
        response->set_result(result.result);
        response->set_confidence_interval_lower(result.confidence_lower);
        response->set_confidence_interval_upper(result.confidence_upper);
        response->set_iterations_completed(result.iterations_completed);
        
        for (const auto& [key, value] : result.additional_metrics) {
            (*response->mutable_additional_metrics())[key] = value;
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration<double, std::milli>(end - start).count();
        response->set_computation_time_ms(elapsed);
        {
            std::lock_guard<std::mutex> lock(metrics_mutex_);
            total_response_time_ += elapsed;
        }
        
        LOG_INFO("Monte Carlo simulation completed in", elapsed, "ms");
        return grpc::Status::OK;
        
    } catch (const std::exception& e) {
        LOG_ERROR("Monte Carlo simulation failed:", e.what());
        return grpc::Status(grpc::StatusCode::INTERNAL, e.what());
    }
}

grpc::Status ComputeServiceImpl::VectorOperation(
    grpc::ServerContext* context,
    const VectorOperationRequest* request,
    VectorOperationResponse* response) {
    
    auto start = std::chrono::high_resolution_clock::now();
    total_requests_++;
    
    try {
        std::vector<double> a(request->vector_a().begin(), request->vector_a().end());
        std::vector<double> b(request->vector_b().begin(), request->vector_b().end());
        
        if (request->operation() == "dot_product") {
            double result = engine_->dotProduct(a, b);
            response->set_result_scalar(result);
        } else if (request->operation() == "cross_product") {
            auto result = engine_->crossProduct(a, b);
            for (double val : result) {
                response->add_result_vector(val);
            }
        } else if (request->operation() == "norm") {
            double result = engine_->vectorNorm(a);
            response->set_result_scalar(result);
        } else if (request->operation() == "distance") {
            double result = engine_->euclideanDistance(a, b);
            response->set_result_scalar(result);
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration<double, std::milli>(end - start).count();
        response->set_computation_time_ms(elapsed);
        {
            std::lock_guard<std::mutex> lock(metrics_mutex_);
            total_response_time_ += elapsed;
        }
        
        return grpc::Status::OK;
        
    } catch (const std::exception& e) {
        LOG_ERROR("Vector operation failed:", e.what());
        return grpc::Status(grpc::StatusCode::INTERNAL, e.what());
    }
}

grpc::Status ComputeServiceImpl::HealthCheck(
    grpc::ServerContext* context,
    const HealthCheckRequest* request,
    HealthCheckResponse* response) {
    
    auto now = std::chrono::steady_clock::now();
    double uptime = std::chrono::duration<double>(now - start_time_).count();
    
    response->set_status("healthy");
    response->set_uptime_seconds(uptime);
    response->set_total_requests(total_requests_.load());
    
    {
        std::lock_guard<std::mutex> lock(const_cast<std::mutex&>(metrics_mutex_));
        if (total_requests_ > 0) {
            response->set_avg_response_time_ms(total_response_time_ / total_requests_);
        }
    }
    
    return grpc::Status::OK;
}

Server::Server(const std::string& address, int thread_pool_size)
    : server_address_(address),
      engine_(std::make_shared<ComputeEngine>(thread_pool_size)),
      service_(std::make_unique<ComputeServiceImpl>(engine_)) {
}

void Server::run() {
    grpc::ServerBuilder builder;
    builder.AddListeningPort(server_address_, grpc::InsecureServerCredentials());
    builder.RegisterService(service_.get());
    
    server_ = builder.BuildAndStart();
    LOG_INFO("Server listening on", server_address_);
    
    server_->Wait();
}

void Server::shutdown() {
    if (server_) {
        LOG_INFO("Shutting down server...");
        server_->Shutdown();
    }
}

} // namespace compute
