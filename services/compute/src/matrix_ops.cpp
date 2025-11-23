#include "matrix_ops.hpp"
#include "utils/logger.hpp"
#include <stdexcept>
#include <thread>
#include <future>

namespace compute {

MatrixOps::Matrix MatrixOps::multiply(const Matrix& a, const Matrix& b) {
    if (a.cols != b.rows) {
        throw std::invalid_argument("Matrix dimensions don't match for multiplication");
    }

    Matrix result(a.rows, b.cols);
    
    // Cache-friendly matrix multiplication
    for (size_t i = 0; i < a.rows; ++i) {
        for (size_t k = 0; k < a.cols; ++k) {
            double a_ik = a.at(i, k);
            for (size_t j = 0; j < b.cols; ++j) {
                result.at(i, j) += a_ik * b.at(k, j);
            }
        }
    }
    
    return result;
}

MatrixOps::Matrix MatrixOps::multiplyParallel(const Matrix& a, const Matrix& b, size_t num_threads) {
    if (a.cols != b.rows) {
        throw std::invalid_argument("Matrix dimensions don't match for multiplication");
    }

    Matrix result(a.rows, b.cols);
    
    // Determine rows per thread
    size_t rows_per_thread = a.rows / num_threads;
    std::vector<std::future<void>> futures;
    
    for (size_t t = 0; t < num_threads; ++t) {
        size_t start_row = t * rows_per_thread;
        size_t end_row = (t == num_threads - 1) ? a.rows : (t + 1) * rows_per_thread;
        
        futures.push_back(std::async(std::launch::async, 
            [&a, &b, &result, start_row, end_row]() {
                multiplyBlock(a, b, result, start_row, end_row);
            }
        ));
    }
    
    // Wait for all threads to complete
    for (auto& future : futures) {
        future.get();
    }
    
    return result;
}

void MatrixOps::multiplyBlock(const Matrix& a, const Matrix& b, Matrix& result,
                              size_t start_row, size_t end_row) {
    for (size_t i = start_row; i < end_row; ++i) {
        for (size_t k = 0; k < a.cols; ++k) {
            double a_ik = a.at(i, k);
            for (size_t j = 0; j < b.cols; ++j) {
                result.at(i, j) += a_ik * b.at(k, j);
            }
        }
    }
}

MatrixOps::Matrix MatrixOps::transpose(const Matrix& m) {
    Matrix result(m.cols, m.rows);
    
    for (size_t i = 0; i < m.rows; ++i) {
        for (size_t j = 0; j < m.cols; ++j) {
            result.at(j, i) = m.at(i, j);
        }
    }
    
    return result;
}

MatrixOps::Matrix MatrixOps::add(const Matrix& a, const Matrix& b) {
    if (a.rows != b.rows || a.cols != b.cols) {
        throw std::invalid_argument("Matrix dimensions don't match for addition");
    }
    
    Matrix result(a.rows, a.cols);
    
    for (size_t i = 0; i < a.data.size(); ++i) {
        result.data[i] = a.data[i] + b.data[i];
    }
    
    return result;
}

MatrixOps::Matrix MatrixOps::scalarMultiply(const Matrix& m, double scalar) {
    Matrix result(m.rows, m.cols);
    
    for (size_t i = 0; i < m.data.size(); ++i) {
        result.data[i] = m.data[i] * scalar;
    }
    
    return result;
}

} // namespace compute
