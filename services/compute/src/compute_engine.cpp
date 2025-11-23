#include "compute_engine.hpp"
#include "utils/logger.hpp"
#include <cmath>
#include <numeric>
#include <stdexcept>

namespace compute {

ComputeEngine::ComputeEngine(size_t thread_pool_size)
    : thread_pool_size_(thread_pool_size),
      thread_pool_(std::make_unique<utils::ThreadPool>(thread_pool_size)) {
    LOG_INFO("ComputeEngine initialized with", thread_pool_size, "threads");
}

MatrixOps::Matrix ComputeEngine::multiplyMatrices(const MatrixOps::Matrix& a,
                                                  const MatrixOps::Matrix& b) {
    total_operations_++;
    
    // Use parallel multiplication for large matrices
    if (a.rows > 100 && b.cols > 100) {
        return MatrixOps::multiplyParallel(a, b, thread_pool_size_);
    }
    
    return MatrixOps::multiply(a, b);
}

StatsOps::Statistics ComputeEngine::analyzeStatistics(
    const std::vector<double>& data,
    const std::vector<std::string>& operations) {
    
    total_operations_++;
    return StatsOps::analyze(data, operations);
}

MonteCarlo::SimulationResult ComputeEngine::runMonteCarlo(
    size_t iterations,
    int dimensions,
    int seed,
    const std::string& type) {
    
    total_operations_++;
    return MonteCarlo::run(iterations, dimensions, seed, type);
}

double ComputeEngine::dotProduct(const std::vector<double>& a,
                                const std::vector<double>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must have same size");
    }
    
    total_operations_++;
    return std::inner_product(a.begin(), a.end(), b.begin(), 0.0);
}

std::vector<double> ComputeEngine::crossProduct(const std::vector<double>& a,
                                               const std::vector<double>& b) {
    if (a.size() != 3 || b.size() != 3) {
        throw std::invalid_argument("Cross product only defined for 3D vectors");
    }
    
    total_operations_++;
    return {
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0]
    };
}

double ComputeEngine::vectorNorm(const std::vector<double>& v) {
    total_operations_++;
    double sum_sq = std::inner_product(v.begin(), v.end(), v.begin(), 0.0);
    return std::sqrt(sum_sq);
}

double ComputeEngine::euclideanDistance(const std::vector<double>& a,
                                       const std::vector<double>& b) {
    if (a.size() != b.size()) {
        throw std::invalid_argument("Vectors must have same size");
    }
    
    total_operations_++;
    double sum_sq = 0.0;
    for (size_t i = 0; i < a.size(); ++i) {
        double diff = a[i] - b[i];
        sum_sq += diff * diff;
    }
    
    return std::sqrt(sum_sq);
}

} // namespace compute
