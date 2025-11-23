#include <gtest/gtest.h>
#include "../include/monte_carlo.hpp"
#include <cmath>

using namespace compute;

TEST(MonteCarloTest, PiEstimation) {
    auto result = MonteCarlo::run(100000, 2, 42, "pi_estimation");
    
    EXPECT_GT(result.iterations_completed, 0);
    EXPECT_NEAR(result.result, M_PI, 0.1);
    EXPECT_LT(result.confidence_lower, result.result);
    EXPECT_GT(result.confidence_upper, result.result);
}

TEST(MonteCarloTest, Integration) {
    auto result = MonteCarlo::run(10000, 3, 42, "integration");
    
    EXPECT_GT(result.iterations_completed, 0);
    EXPECT_GT(result.result, 0.0);
    EXPECT_LT(result.result, 1.0);
}

int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
