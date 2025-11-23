#pragma once

#include <memory>
#include <string>
#include "matrix_ops.hpp"
#include "stats_ops.hpp"
#include "monte_carlo.hpp"
#include "utils/thread_pool.hpp"

namespace compute {

class ComputeEngine {
public:
    explicit ComputeEngine(size_t thread_pool_size = 8);
    ~ComputeEngine() = default;

    // Matrix operations
    MatrixOps::Matrix multiplyMatrices(const MatrixOps::Matrix& a, 
                                       const MatrixOps::Matrix& b);

    // Statistical operations
    StatsOps::Statistics analyzeStatistics(const std::vector<double>& data,
                                          const std::vector<std::string>& operations);

    // Monte Carlo simulations
    MonteCarlo::SimulationResult runMonteCarlo(size_t iterations, 
                                              int dimensions,
                                              int seed,
                                              const std::string& type);

    // Vector operations
    double dotProduct(const std::vector<double>& a, const std::vector<double>& b);
    std::vector<double> crossProduct(const std::vector<double>& a, 
                                    const std::vector<double>& b);
    double vectorNorm(const std::vector<double>& v);
    double euclideanDistance(const std::vector<double>& a, 
                           const std::vector<double>& b);

    // Performance metrics
    size_t getThreadPoolSize() const { return thread_pool_size_; }
    uint64_t getTotalOperations() const { return total_operations_; }

private:
    size_t thread_pool_size_;
    std::unique_ptr<utils::ThreadPool> thread_pool_;
    std::atomic<uint64_t> total_operations_{0};
};

} // namespace compute
