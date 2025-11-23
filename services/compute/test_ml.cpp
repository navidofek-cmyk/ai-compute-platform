#include "neural_network.hpp"
#include "utils/logger.hpp"
#include <iostream>
#include <vector>
#include <random>

int main(int argc, char** argv) {
    try {
        // Get model path from command line or use default
        std::string model_path = (argc > 1) ? argv[1] : "../models/mnist_model.onnx";
        
        LOG_INFO("Starting ML inference test...");
        LOG_INFO("Loading model from: " + model_path);
        
        // Initialize neural network
        compute::NeuralNetworkEngine engine(model_path, false);
        
        LOG_INFO("Neural network loaded successfully");
        
        // Create dummy input (784 floats - 28x28 image)
        std::vector<float> input(784);
        
        // Generate a simple pattern (vertical line in the middle - looks like "1")
        for (int i = 0; i < 28; i++) {
            for (int j = 0; j < 28; j++) {
                if (j >= 12 && j <= 15) {
                    input[i * 28 + j] = 1.0f;  // White pixel
                } else {
                    input[i * 28 + j] = 0.0f;  // Black pixel
                }
            }
        }
        
        // Run inference
        LOG_INFO("Running inference...");
        std::vector<int64_t> input_shape = {1, 1, 28, 28};  // Batch size 1, 1 channel, 28x28 image
        auto output = engine.predict(input, input_shape);
        
        // Apply softmax and get top-k
        auto probabilities = compute::NeuralNetworkEngine::softmax(output);
        auto top_k = compute::NeuralNetworkEngine::get_top_k(probabilities, 3);
        
        // Display results
        std::cout << "\n=== MNIST Inference Results ===" << std::endl;
        std::cout << "Top 3 predictions:" << std::endl;
        
        for (size_t i = 0; i < top_k.size(); i++) {
            std::cout << "  " << (i+1) << ". Digit " << top_k[i].first 
                     << " - Probability: " << (top_k[i].second * 100.0f) 
                     << "%" << std::endl;
        }
        
        std::cout << "================================\n" << std::endl;
        
        LOG_INFO("Test completed successfully!");
        return 0;
        
    } catch (const std::exception& e) {
        LOG_ERROR("Test failed: " + std::string(e.what()));
        return 1;
    }
}
