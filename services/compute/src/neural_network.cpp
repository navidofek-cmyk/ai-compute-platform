#include "neural_network.hpp"
#include "utils/logger.hpp"
#include <algorithm>
#include <numeric>
#include <cmath>
#include <stdexcept>
#include <thread>

namespace compute {

NeuralNetworkEngine::NeuralNetworkEngine(const std::string& model_path, bool use_gpu)
    : is_initialized_(false) {
    try {
        initialize_session(model_path, use_gpu);
        extract_model_info();
        is_initialized_ = true;
        LOG_INFO("Neural network engine initialized with model: " + model_path);
    } catch (const std::exception& e) {
        LOG_ERROR("Failed to initialize neural network: " + std::string(e.what()));
        throw;
    }
}

NeuralNetworkEngine::~NeuralNetworkEngine() {
    LOG_INFO("Neural network engine destroyed");
}

void NeuralNetworkEngine::initialize_session(const std::string& model_path, bool use_gpu) {
    // Create ONNX Runtime environment
    env_ = std::make_unique<Ort::Env>(ORT_LOGGING_LEVEL_WARNING, "NeuralNetworkEngine");
    
    // Create session options
    session_options_ = std::make_unique<Ort::SessionOptions>();
    session_options_->SetIntraOpNumThreads(std::thread::hardware_concurrency());
    session_options_->SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
    
    // Enable GPU if requested and available
    if (use_gpu) {
        try {
            // Try to use CUDA provider
            OrtCUDAProviderOptions cuda_options{};
            session_options_->AppendExecutionProvider_CUDA(cuda_options);
            LOG_INFO("CUDA provider enabled for GPU acceleration");
        } catch (const std::exception& e) {
            LOG_WARNING("CUDA not available, falling back to CPU: " + std::string(e.what()));
        }
    }
    
    // Create session
    session_ = std::make_unique<Ort::Session>(*env_, model_path.c_str(), *session_options_);
    
    // Create allocator
    allocator_ = std::make_unique<Ort::AllocatorWithDefaultOptions>();
}

void NeuralNetworkEngine::extract_model_info() {
    // Get input info
    size_t num_input_nodes = session_->GetInputCount();
    for (size_t i = 0; i < num_input_nodes; i++) {
        auto input_name = session_->GetInputNameAllocated(i, *allocator_);
        input_node_names_str_.push_back(std::string(input_name.get()));
        input_node_names_.push_back(input_node_names_str_.back().c_str());
        
        auto type_info = session_->GetInputTypeInfo(i);
        auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
        input_shape_ = tensor_info.GetShape();
    }
    
    // Get output info
    size_t num_output_nodes = session_->GetOutputCount();
    for (size_t i = 0; i < num_output_nodes; i++) {
        auto output_name = session_->GetOutputNameAllocated(i, *allocator_);
        output_node_names_str_.push_back(std::string(output_name.get()));
        output_node_names_.push_back(output_node_names_str_.back().c_str());
        
        auto type_info = session_->GetOutputTypeInfo(i);
        auto tensor_info = type_info.GetTensorTypeAndShapeInfo();
        output_shape_ = tensor_info.GetShape();
    }
}

std::vector<float> NeuralNetworkEngine::predict(
    const std::vector<float>& input_data,
    const std::vector<int64_t>& input_shape) {
    
    if (!is_initialized_) {
        throw std::runtime_error("Neural network engine not initialized");
    }
    
    // Calculate total elements
    int64_t total_elements = std::accumulate(
        input_shape.begin(), input_shape.end(), 1LL, std::multiplies<int64_t>());
    
    if (input_data.size() != static_cast<size_t>(total_elements)) {
        throw std::invalid_argument(
            "Input data size mismatch. Expected: " + std::to_string(total_elements) +
            ", Got: " + std::to_string(input_data.size()));
    }
    
    // Create input tensor
    auto memory_info = Ort::MemoryInfo::CreateCpu(OrtArenaAllocator, OrtMemTypeDefault);
    Ort::Value input_tensor = Ort::Value::CreateTensor<float>(
        memory_info,
        const_cast<float*>(input_data.data()),
        input_data.size(),
        input_shape.data(),
        input_shape.size()
    );
    
    // Run inference
    auto output_tensors = session_->Run(
        Ort::RunOptions{nullptr},
        input_node_names_.data(),
        &input_tensor,
        1,
        output_node_names_.data(),
        output_node_names_.size()
    );
    
    // Extract output
    float* float_array = output_tensors[0].GetTensorMutableData<float>();
    size_t output_size = output_tensors[0].GetTensorTypeAndShapeInfo().GetElementCount();
    
    return std::vector<float>(float_array, float_array + output_size);
}

std::vector<std::vector<float>> NeuralNetworkEngine::predict_batch(
    const std::vector<std::vector<float>>& batch_data,
    const std::vector<int64_t>& input_shape) {
    
    std::vector<std::vector<float>> results;
    results.reserve(batch_data.size());
    
    for (const auto& input : batch_data) {
        results.push_back(predict(input, input_shape));
    }
    
    return results;
}

std::vector<int64_t> NeuralNetworkEngine::get_input_shape() const {
    return input_shape_;
}

std::vector<int64_t> NeuralNetworkEngine::get_output_shape() const {
    return output_shape_;
}

std::string NeuralNetworkEngine::get_model_info() const {
    std::string info = "Model Information:\n";
    info += "  Input nodes: " + std::to_string(input_node_names_.size()) + "\n";
    info += "  Output nodes: " + std::to_string(output_node_names_.size()) + "\n";
    
    info += "  Input shape: [";
    for (size_t i = 0; i < input_shape_.size(); i++) {
        info += std::to_string(input_shape_[i]);
        if (i < input_shape_.size() - 1) info += ", ";
    }
    info += "]\n";
    
    info += "  Output shape: [";
    for (size_t i = 0; i < output_shape_.size(); i++) {
        info += std::to_string(output_shape_[i]);
        if (i < output_shape_.size() - 1) info += ", ";
    }
    info += "]";
    
    return info;
}

std::vector<float> NeuralNetworkEngine::softmax(const std::vector<float>& logits) {
    std::vector<float> probabilities(logits.size());
    
    // Find max for numerical stability
    float max_logit = *std::max_element(logits.begin(), logits.end());
    
    // Compute exp(x - max) and sum
    float sum = 0.0f;
    for (size_t i = 0; i < logits.size(); i++) {
        probabilities[i] = std::exp(logits[i] - max_logit);
        sum += probabilities[i];
    }
    
    // Normalize
    for (size_t i = 0; i < probabilities.size(); i++) {
        probabilities[i] /= sum;
    }
    
    return probabilities;
}

std::vector<std::pair<int, float>> NeuralNetworkEngine::get_top_k(
    const std::vector<float>& probabilities, int k) {
    
    std::vector<std::pair<int, float>> indexed_probs;
    indexed_probs.reserve(probabilities.size());
    
    for (size_t i = 0; i < probabilities.size(); i++) {
        indexed_probs.emplace_back(static_cast<int>(i), probabilities[i]);
    }
    
    // Sort by probability (descending)
    std::partial_sort(
        indexed_probs.begin(),
        indexed_probs.begin() + std::min(k, static_cast<int>(indexed_probs.size())),
        indexed_probs.end(),
        [](const auto& a, const auto& b) { return a.second > b.second; }
    );
    
    // Return top k
    int actual_k = std::min(k, static_cast<int>(indexed_probs.size()));
    return std::vector<std::pair<int, float>>(
        indexed_probs.begin(), indexed_probs.begin() + actual_k);
}

} // namespace compute
