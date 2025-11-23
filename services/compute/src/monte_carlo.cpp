#include "monte_carlo.hpp"
#include "stats_ops.hpp"
#include "utils/logger.hpp"
#include <cmath>
#include <algorithm>
#include <stdexcept>

namespace compute {

MonteCarlo::SimulationResult MonteCarlo::run(size_t iterations, int dimensions,
                                             int seed, const std::string& type) {
    LOG_INFO("Running Monte Carlo simulation:", type, "iterations:", iterations);
    
    if (type == "pi_estimation") {
        return estimatePi(iterations, seed);
    } else if (type == "option_pricing") {
        return priceOption(iterations, seed, dimensions);
    } else if (type == "integration") {
        return integrate(iterations, seed, dimensions);
    }
    
    throw std::invalid_argument("Unknown simulation type: " + type);
}

MonteCarlo::SimulationResult MonteCarlo::estimatePi(size_t iterations, int seed) {
    RandomGenerator rng(seed);
    size_t inside_circle = 0;
    std::vector<double> estimates;
    
    // Run simulation with periodic estimates
    size_t checkpoint = iterations / 100;
    if (checkpoint == 0) checkpoint = 1;
    
    for (size_t i = 0; i < iterations; ++i) {
        double x = rng.uniform();
        double y = rng.uniform();
        
        if (x * x + y * y <= 1.0) {
            inside_circle++;
        }
        
        if ((i + 1) % checkpoint == 0) {
            double pi_estimate = 4.0 * inside_circle / (i + 1);
            estimates.push_back(pi_estimate);
        }
    }
    
    SimulationResult result;
    result.result = 4.0 * inside_circle / iterations;
    result.iterations_completed = iterations;
    
    // Calculate confidence interval
    double mean = StatsOps::mean(estimates);
    double stddev = StatsOps::stddev(estimates, mean);
    double margin = 1.96 * stddev / std::sqrt(estimates.size());
    
    result.confidence_lower = mean - margin;
    result.confidence_upper = mean + margin;
    result.additional_metrics["actual_pi"] = M_PI;
    result.additional_metrics["error"] = std::abs(result.result - M_PI);
    result.additional_metrics["error_percentage"] = 
        std::abs(result.result - M_PI) / M_PI * 100.0;
    
    return result;
}

MonteCarlo::SimulationResult MonteCarlo::priceOption(size_t iterations, int seed, 
                                                     int dimensions) {
    RandomGenerator rng(seed);
    
    // European call option parameters
    double S0 = 100.0;      // Initial stock price
    double K = 100.0;       // Strike price
    double r = 0.05;        // Risk-free rate
    double sigma = 0.2;     // Volatility
    double T = 1.0;         // Time to maturity
    int steps = dimensions; // Time steps
    
    std::vector<double> payoffs;
    payoffs.reserve(iterations);
    
    double dt = T / steps;
    double drift = (r - 0.5 * sigma * sigma) * dt;
    double diffusion = sigma * std::sqrt(dt);
    
    for (size_t i = 0; i < iterations; ++i) {
        double S = S0;
        
        // Simulate price path
        for (int step = 0; step < steps; ++step) {
            double Z = rng.normal();
            S *= std::exp(drift + diffusion * Z);
        }
        
        // Calculate payoff
        double payoff = std::max(S - K, 0.0);
        payoffs.push_back(payoff);
    }
    
    // Discount to present value
    double discount = std::exp(-r * T);
    double option_price = discount * StatsOps::mean(payoffs);
    
    SimulationResult result;
    result.result = option_price;
    result.iterations_completed = iterations;
    
    // Calculate confidence interval
    double stddev = StatsOps::stddev(payoffs, StatsOps::mean(payoffs));
    double std_error = stddev / std::sqrt(iterations);
    double margin = 1.96 * discount * std_error;
    
    result.confidence_lower = option_price - margin;
    result.confidence_upper = option_price + margin;
    result.additional_metrics["strike"] = K;
    result.additional_metrics["spot"] = S0;
    result.additional_metrics["volatility"] = sigma;
    result.additional_metrics["time_steps"] = static_cast<double>(steps);
    
    return result;
}

MonteCarlo::SimulationResult MonteCarlo::integrate(size_t iterations, int seed, 
                                                   int dimensions) {
    RandomGenerator rng(seed);
    
    // Integrate f(x) = exp(-x^2) over [0,1]^dimensions
    std::vector<double> samples;
    samples.reserve(iterations);
    
    for (size_t i = 0; i < iterations; ++i) {
        double sum_sq = 0.0;
        
        for (int d = 0; d < dimensions; ++d) {
            double x = rng.uniform();
            sum_sq += x * x;
        }
        
        double value = std::exp(-sum_sq);
        samples.push_back(value);
    }
    
    double integral = StatsOps::mean(samples);
    
    SimulationResult result;
    result.result = integral;
    result.iterations_completed = iterations;
    
    // Calculate confidence interval
    double stddev = StatsOps::stddev(samples, integral);
    double std_error = stddev / std::sqrt(iterations);
    double margin = 1.96 * std_error;
    
    result.confidence_lower = integral - margin;
    result.confidence_upper = integral + margin;
    result.additional_metrics["dimensions"] = static_cast<double>(dimensions);
    result.additional_metrics["std_error"] = std_error;
    
    return result;
}

} // namespace compute
