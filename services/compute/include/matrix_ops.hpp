#pragma once

#include <vector>
#include <memory>
#include <chrono>

namespace compute {

class MatrixOps {
public:
    struct Matrix {
        std::vector<double> data;
        size_t rows;
        size_t cols;

        Matrix(size_t r, size_t c) : data(r * c, 0.0), rows(r), cols(c) {}
        
        double& at(size_t i, size_t j) {
            return data[i * cols + j];
        }
        
        const double& at(size_t i, size_t j) const {
            return data[i * cols + j];
        }
    };

    // Matrix multiplication with optimization
    static Matrix multiply(const Matrix& a, const Matrix& b);
    
    // Parallel matrix multiplication
    static Matrix multiplyParallel(const Matrix& a, const Matrix& b, size_t num_threads = 4);
    
    // Transpose matrix
    static Matrix transpose(const Matrix& m);
    
    // Matrix addition
    static Matrix add(const Matrix& a, const Matrix& b);
    
    // Scalar multiplication
    static Matrix scalarMultiply(const Matrix& m, double scalar);

private:
    static void multiplyBlock(const Matrix& a, const Matrix& b, Matrix& result,
                             size_t start_row, size_t end_row);
};

} // namespace compute
