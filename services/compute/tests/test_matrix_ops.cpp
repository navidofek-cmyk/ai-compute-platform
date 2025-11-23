#include <gtest/gtest.h>
#include "../include/matrix_ops.hpp"

using namespace compute;

TEST(MatrixOpsTest, MultiplicationBasic) {
    MatrixOps::Matrix a(2, 2);
    a.at(0, 0) = 1; a.at(0, 1) = 2;
    a.at(1, 0) = 3; a.at(1, 1) = 4;
    
    MatrixOps::Matrix b(2, 2);
    b.at(0, 0) = 5; b.at(0, 1) = 6;
    b.at(1, 0) = 7; b.at(1, 1) = 8;
    
    auto result = MatrixOps::multiply(a, b);
    
    EXPECT_DOUBLE_EQ(result.at(0, 0), 19);
    EXPECT_DOUBLE_EQ(result.at(0, 1), 22);
    EXPECT_DOUBLE_EQ(result.at(1, 0), 43);
    EXPECT_DOUBLE_EQ(result.at(1, 1), 50);
}

TEST(MatrixOpsTest, MultiplicationIdentity) {
    MatrixOps::Matrix a(2, 2);
    a.at(0, 0) = 1; a.at(0, 1) = 2;
    a.at(1, 0) = 3; a.at(1, 1) = 4;
    
    MatrixOps::Matrix identity(2, 2);
    identity.at(0, 0) = 1; identity.at(0, 1) = 0;
    identity.at(1, 0) = 0; identity.at(1, 1) = 1;
    
    auto result = MatrixOps::multiply(a, identity);
    
    EXPECT_DOUBLE_EQ(result.at(0, 0), 1);
    EXPECT_DOUBLE_EQ(result.at(0, 1), 2);
    EXPECT_DOUBLE_EQ(result.at(1, 0), 3);
    EXPECT_DOUBLE_EQ(result.at(1, 1), 4);
}

TEST(MatrixOpsTest, Transpose) {
    MatrixOps::Matrix a(2, 3);
    a.at(0, 0) = 1; a.at(0, 1) = 2; a.at(0, 2) = 3;
    a.at(1, 0) = 4; a.at(1, 1) = 5; a.at(1, 2) = 6;
    
    auto result = MatrixOps::transpose(a);
    
    EXPECT_EQ(result.rows, 3);
    EXPECT_EQ(result.cols, 2);
    EXPECT_DOUBLE_EQ(result.at(0, 0), 1);
    EXPECT_DOUBLE_EQ(result.at(0, 1), 4);
    EXPECT_DOUBLE_EQ(result.at(1, 0), 2);
    EXPECT_DOUBLE_EQ(result.at(1, 1), 5);
}

int main(int argc, char** argv) {
    testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
