#pragma once

#include <string>
#include <vector>
#include <memory>
#include <onnxruntime_cxx_api.h>

namespace compute {

/**
 * Neural Network Inference Engine using ONNX Runtime
 * Provides fast inference for pretrained models
 */
class NeuralNetworkEngine {
public:
    /**
     * Constructor
     * @param model_path Path to ONNX model file
     * @param use_gpu Whether to use GPU acceleration (if available)
     */
    explicit NeuralNetworkEngine(const std::string& model_path, bool use_gpu = false);
    
    /**
     * Destructor
     */
    ~NeuralNetworkEngine();
    
    /**
     * Run inference on input data
     * @param input_data Flattened input vector
     * @param input_shape Shape of input tensor (e.g., {1, 1, 28, 28} for MNIST)
     * @return Output predictions
     */
    std::vector<float> predict(const std::vector<float>& input_data,
                               const std::vector<int64_t>& input_shape);
    
    /**
     * Run batch inference on multiple inputs
     * @param batch_data Vector of input vectors
     * @param input_shape Shape of single input (batch size will be determined automatically)
     * @return Vector of output predictions for each input
     */
    std::vector<std::vector<float>> predict_batch(
        const std::vector<std::vector<float>>& batch_data,
        const std::vector<int64_t>& input_shape);
    
    /**
     * Get model input shape
     * @return Input tensor dimensions
     */
    std::vector<int64_t> get_input_shape() const;
    
    /**
     * Get model output shape
     * @return Output tensor dimensions
     */
    std::vector<int64_t> get_output_shape() const;
    
    /**
     * Get model information
     * @return String with model metadata
     */
    std::string get_model_info() const;
    
    /**
     * Get class probabilities from logits
     * @param logits Raw output from model
     * @return Softmax probabilities
     */
    static std::vector<float> softmax(const std::vector<float>& logits);
    
    /**
     * Get top-k predictions
     * @param probabilities Class probabilities
     * @param k Number of top predictions to return
     * @return Vector of (class_index, probability) pairs sorted by probability
     */
    static std::vector<std::pair<int, float>> get_top_k(
        const std::vector<float>& probabilities, int k = 5);

private:
    std::unique_ptr<Ort::Env> env_;
    std::unique_ptr<Ort::Session> session_;
    std::unique_ptr<Ort::SessionOptions> session_options_;
    std::unique_ptr<Ort::AllocatorWithDefaultOptions> allocator_;
    
    std::vector<const char*> input_node_names_;
    std::vector<const char*> output_node_names_;
    std::vector<std::string> input_node_names_str_;
    std::vector<std::string> output_node_names_str_;
    
    std::vector<int64_t> input_shape_;
    std::vector<int64_t> output_shape_;
    
    bool is_initialized_;
    
    void initialize_session(const std::string& model_path, bool use_gpu);
    void extract_model_info();
};

} // namespace compute
