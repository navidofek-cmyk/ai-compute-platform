#pragma once

#include <random>
#include <vector>
#include <map>
#include <string>
#include <functional>

namespace compute {

class MonteCarlo {
public:
    struct SimulationResult {
        double result = 0.0;
        double confidence_lower = 0.0;
        double confidence_upper = 0.0;
        size_t iterations_completed = 0;
        std::map<std::string, double> additional_metrics;
    };

    // Run Monte Carlo simulation
    static SimulationResult run(size_t iterations, int dimensions, 
                               int seed, const std::string& type);

private:
    // Simulation types
    static SimulationResult estimatePi(size_t iterations, int seed);
    static SimulationResult priceOption(size_t iterations, int seed, int dimensions);
    static SimulationResult integrate(size_t iterations, int seed, int dimensions);
    
    // Helper functions
    static double calculateConfidenceInterval(const std::vector<double>& samples, 
                                              double confidence_level = 0.95);
    
    class RandomGenerator {
    public:
        explicit RandomGenerator(int seed) : gen_(seed), dist_(0.0, 1.0) {}
        
        double uniform() {
            return dist_(gen_);
        }
        
        double normal(double mean = 0.0, double stddev = 1.0) {
            std::normal_distribution<double> norm(mean, stddev);
            return norm(gen_);
        }
        
    private:
        std::mt19937_64 gen_;
        std::uniform_real_distribution<double> dist_;
    };
};

} // namespace compute
