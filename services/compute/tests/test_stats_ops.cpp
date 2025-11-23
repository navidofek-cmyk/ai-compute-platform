#include <gtest/gtest.h>
#include "../include/stats_ops.hpp"

using namespace compute;

TEST(StatsOpsTest, Mean) {
    std::vector<double> data = {1.0, 2.0, 3.0, 4.0, 5.0};
    double result = StatsOps::mean(data);
    EXPECT_DOUBLE_EQ(result, 3.0);
}

TEST(StatsOpsTest, Median) {
    std::vector<double> data = {1.0, 2.0, 3.0, 4.0, 5.0};
    double result = StatsOps::median(data);
    EXPECT_DOUBLE_EQ(result, 3.0);
}

TEST(StatsOpsTest, Variance) {
    std::vector<double> data = {2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0};
    double m = StatsOps::mean(data);
    double result = StatsOps::variance(data, m);
    EXPECT_NEAR(result, 4.0, 0.01);
}

int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
