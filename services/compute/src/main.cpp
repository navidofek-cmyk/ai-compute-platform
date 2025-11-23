#include "server.hpp"
#include "utils/logger.hpp"
#include <csignal>
#include <memory>
#include <cstdlib>

namespace {
    std::unique_ptr<compute::Server> g_server;
    
    void signalHandler(int signal) {
        LOG_INFO("Received signal", signal, "- shutting down gracefully");
        if (g_server) {
            g_server->shutdown();
        }
        std::exit(0);
    }
}

int main(int argc, char** argv) {
    // Set up signal handlers
    std::signal(SIGINT, signalHandler);
    std::signal(SIGTERM, signalHandler);
    
    // Configure logger
    const char* log_level_env = std::getenv("LOG_LEVEL");
    if (log_level_env) {
        std::string log_level(log_level_env);
        if (log_level == "debug") {
            compute::utils::Logger::instance().setLogLevel(compute::utils::LogLevel::DEBUG);
        } else if (log_level == "warning") {
            compute::utils::Logger::instance().setLogLevel(compute::utils::LogLevel::WARNING);
        } else if (log_level == "error") {
            compute::utils::Logger::instance().setLogLevel(compute::utils::LogLevel::ERROR);
        }
    }
    
    // Get configuration from environment
    const char* port_env = std::getenv("GRPC_PORT");
    std::string port = port_env ? port_env : "50051";
    
    const char* threads_env = std::getenv("THREAD_POOL_SIZE");
    int thread_pool_size = threads_env ? std::atoi(threads_env) : 8;
    
    std::string server_address = "0.0.0.0:" + port;
    
    LOG_INFO("=== Compute Service Starting ===");
    LOG_INFO("Address:", server_address);
    LOG_INFO("Thread pool size:", thread_pool_size);
    
    try {
        g_server = std::make_unique<compute::Server>(server_address, thread_pool_size);
        g_server->run();
    } catch (const std::exception& e) {
        LOG_ERROR("Fatal error:", e.what());
        return 1;
    }
    
    return 0;
}
