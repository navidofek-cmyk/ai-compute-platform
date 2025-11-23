#include "stats_ops.hpp"
#include "utils/logger.hpp"
#include <algorithm>
#include <cmath>
#include <numeric>
#include <stdexcept>

namespace compute {

StatsOps::Statistics StatsOps::analyze(const std::vector<double>& data,
                                       const std::vector<std::string>& operations) {
    if (data.empty()) {
        throw std::invalid_argument("Cannot analyze empty dataset");
    }
    
    Statistics stats;
    stats.count = data.size();
    stats.min = *std::min_element(data.begin(), data.end());
    stats.max = *std::max_element(data.begin(), data.end());
    
    // Calculate mean
    stats.mean = mean(data);
    
    // Process requested operations
    for (const auto& op : operations) {
        if (op == "mean") {
            // Already calculated
        } else if (op == "median") {
            stats.median = median(data);
        } else if (op == "stddev") {
            stats.variance = variance(data, stats.mean);
            stats.stddev = std::sqrt(stats.variance);
        } else if (op == "variance") {
            stats.variance = variance(data, stats.mean);
        } else if (op == "percentiles") {
            stats.percentiles[25] = percentile(data, 25);
            stats.percentiles[50] = percentile(data, 50);
            stats.percentiles[75] = percentile(data, 75);
            stats.percentiles[95] = percentile(data, 95);
            stats.percentiles[99] = percentile(data, 99);
        }
    }
    
    return stats;
}

double StatsOps::mean(const std::vector<double>& data) {
    return std::accumulate(data.begin(), data.end(), 0.0) / data.size();
}

double StatsOps::median(std::vector<double> data) {
    size_t n = data.size();
    std::nth_element(data.begin(), data.begin() + n / 2, data.end());
    
    if (n % 2 == 0) {
        double median1 = data[n / 2];
        std::nth_element(data.begin(), data.begin() + n / 2 - 1, data.end());
        double median2 = data[n / 2 - 1];
        return (median1 + median2) / 2.0;
    }
    
    return data[n / 2];
}

double StatsOps::variance(const std::vector<double>& data, double m) {
    double sum_sq_diff = 0.0;
    
    for (double value : data) {
        double diff = value - m;
        sum_sq_diff += diff * diff;
    }
    
    return sum_sq_diff / data.size();
}

double StatsOps::stddev(const std::vector<double>& data, double m) {
    return std::sqrt(variance(data, m));
}

double StatsOps::percentile(std::vector<double> data, int p) {
    if (p < 0 || p > 100) {
        throw std::invalid_argument("Percentile must be between 0 and 100");
    }
    
    std::sort(data.begin(), data.end());
    
    double index = (p / 100.0) * (data.size() - 1);
    size_t lower = static_cast<size_t>(std::floor(index));
    size_t upper = static_cast<size_t>(std::ceil(index));
    
    if (lower == upper) {
        return data[lower];
    }
    
    double weight = index - lower;
    return data[lower] * (1 - weight) + data[upper] * weight;
}

double StatsOps::skewness(const std::vector<double>& data) {
    double m = mean(data);
    double s = stddev(data, m);
    
    double sum_cubed = 0.0;
    for (double value : data) {
        double diff = (value - m) / s;
        sum_cubed += diff * diff * diff;
    }
    
    return sum_cubed / data.size();
}

double StatsOps::kurtosis(const std::vector<double>& data) {
    double m = mean(data);
    double s = stddev(data, m);
    
    double sum_fourth = 0.0;
    for (double value : data) {
        double diff = (value - m) / s;
        sum_fourth += diff * diff * diff * diff;
    }
    
    return (sum_fourth / data.size()) - 3.0;
}

std::vector<double> StatsOps::movingAverage(const std::vector<double>& data, size_t window) {
    if (window == 0 || window > data.size()) {
        throw std::invalid_argument("Invalid window size");
    }
    
    std::vector<double> result;
    result.reserve(data.size() - window + 1);
    
    double sum = std::accumulate(data.begin(), data.begin() + window, 0.0);
    result.push_back(sum / window);
    
    for (size_t i = window; i < data.size(); ++i) {
        sum = sum - data[i - window] + data[i];
        result.push_back(sum / window);
    }
    
    return result;
}

} // namespace compute
