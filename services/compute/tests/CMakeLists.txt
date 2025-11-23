cmake_minimum_required(VERSION 3.15)

enable_testing()

# Find GTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# Test executable
add_executable(compute_tests
    test_matrix_ops.cpp
    test_stats_ops.cpp
    test_monte_carlo.cpp
)

target_link_libraries(compute_tests
    ${GTEST_LIBRARIES}
    pthread
)

# Register tests
add_test(NAME ComputeTests COMMAND compute_tests)
