#pragma once

#include <vector>
#include <map>
#include <string>
#include <algorithm>
#include <cmath>
#include <numeric>

namespace compute {

class StatsOps {
public:
    struct Statistics {
        double mean = 0.0;
        double median = 0.0;
        double stddev = 0.0;
        double variance = 0.0;
        double min = 0.0;
        double max = 0.0;
        size_t count = 0;
        std::map<int, double> percentiles;
    };

    // Calculate comprehensive statistics
    static Statistics analyze(const std::vector<double>& data, 
                             const std::vector<std::string>& operations);
    
    // Individual operations
    static double mean(const std::vector<double>& data);
    static double median(std::vector<double> data);
    static double variance(const std::vector<double>& data, double mean);
    static double stddev(const std::vector<double>& data, double mean);
    static double percentile(std::vector<double> data, int p);
    
    // Advanced operations
    static double skewness(const std::vector<double>& data);
    static double kurtosis(const std::vector<double>& data);
    static std::vector<double> movingAverage(const std::vector<double>& data, size_t window);
};

} // namespace compute
