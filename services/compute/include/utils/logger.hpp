#pragma once

#include <string>
#include <sstream>
#include <iostream>
#include <mutex>
#include <chrono>
#include <iomanip>

namespace compute {
namespace utils {

enum class LogLevel {
    DEBUG,
    INFO,
    WARNING,
    ERROR
};

class Logger {
public:
    static Logger& instance();

    void setLogLevel(LogLevel level) { log_level_ = level; }
    
    void debug(const std::string& message);
    void info(const std::string& message);
    void warning(const std::string& message);
    void error(const std::string& message);

    template<typename... Args>
    void debug(Args&&... args) {
        log(LogLevel::DEBUG, format(std::forward<Args>(args)...));
    }

    template<typename... Args>
    void info(Args&&... args) {
        log(LogLevel::INFO, format(std::forward<Args>(args)...));
    }

    template<typename... Args>
    void warning(Args&&... args) {
        log(LogLevel::WARNING, format(std::forward<Args>(args)...));
    }

    template<typename... Args>
    void error(Args&&... args) {
        log(LogLevel::ERROR, format(std::forward<Args>(args)...));
    }

private:
    Logger() = default;
    
    void log(LogLevel level, const std::string& message);
    std::string getCurrentTimestamp();
    std::string levelToString(LogLevel level);

    template<typename T>
    std::string format(T&& arg) {
        std::ostringstream oss;
        oss << std::forward<T>(arg);
        return oss.str();
    }

    template<typename T, typename... Args>
    std::string format(T&& first, Args&&... args) {
        std::ostringstream oss;
        oss << std::forward<T>(first);
        return oss.str() + " " + format(std::forward<Args>(args)...);
    }

    LogLevel log_level_ = LogLevel::INFO;
    std::mutex mutex_;
};

// Convenience macros
#define LOG_DEBUG(...) compute::utils::Logger::instance().debug(__VA_ARGS__)
#define LOG_INFO(...) compute::utils::Logger::instance().info(__VA_ARGS__)
#define LOG_WARNING(...) compute::utils::Logger::instance().warning(__VA_ARGS__)
#define LOG_ERROR(...) compute::utils::Logger::instance().error(__VA_ARGS__)

} // namespace utils
} // namespace compute
