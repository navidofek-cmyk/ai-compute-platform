cmake_minimum_required(VERSION 3.15)
project(ComputeService VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Compiler flags for optimization and warnings
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic -O3 -march=native")
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0 -fsanitize=address")
endif()

# Find required packages
find_package(Threads REQUIRED)
find_package(Protobuf REQUIRED)
find_package(PkgConfig REQUIRED)
pkg_check_modules(GRPC REQUIRED grpc++)

# Include directories
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_BINARY_DIR}
    ${Protobuf_INCLUDE_DIRS}
)

# Generate protobuf and gRPC files
set(PROTO_PATH "${CMAKE_CURRENT_SOURCE_DIR}/../../proto")
set(PROTO_FILE "${PROTO_PATH}/compute.proto")
set(GENERATED_PROTOBUF_PATH "${CMAKE_CURRENT_BINARY_DIR}")

file(MAKE_DIRECTORY ${GENERATED_PROTOBUF_PATH})

add_custom_command(
    OUTPUT "${GENERATED_PROTOBUF_PATH}/compute.pb.cc"
           "${GENERATED_PROTOBUF_PATH}/compute.pb.h"
           "${GENERATED_PROTOBUF_PATH}/compute.grpc.pb.cc"
           "${GENERATED_PROTOBUF_PATH}/compute.grpc.pb.h"
    COMMAND protoc
    ARGS --grpc_out=${GENERATED_PROTOBUF_PATH}
         --cpp_out=${GENERATED_PROTOBUF_PATH}
         --plugin=protoc-gen-grpc=/usr/bin/grpc_cpp_plugin
         -I ${PROTO_PATH}
         ${PROTO_FILE}
    DEPENDS ${PROTO_FILE}
    COMMENT "Generating protobuf and gRPC files"
)

# Source files
set(SOURCES
    src/main.cpp
    src/server.cpp
    src/compute_engine.cpp
    src/matrix_ops.cpp
    src/stats_ops.cpp
    src/monte_carlo.cpp
    src/utils/logger.cpp
    src/utils/thread_pool.cpp
    ${GENERATED_PROTOBUF_PATH}/compute.pb.cc
    ${GENERATED_PROTOBUF_PATH}/compute.grpc.pb.cc
)

# Header files
set(HEADERS
    include/server.hpp
    include/compute_engine.hpp
    include/matrix_ops.hpp
    include/stats_ops.hpp
    include/monte_carlo.hpp
    include/utils/logger.hpp
    include/utils/thread_pool.hpp
)

# Create executable
add_executable(compute_service ${SOURCES} ${HEADERS})

# Link libraries
target_link_libraries(compute_service
    ${Protobuf_LIBRARIES}
    ${GRPC_LIBRARIES}
    Threads::Threads
)

# Install targets
install(TARGETS compute_service DESTINATION bin)

# Testing - optional
# enable_testing()
# add_subdirectory(tests)

# Print configuration
message(STATUS "Build type: ${CMAKE_BUILD_TYPE}")
message(STATUS "C++ compiler: ${CMAKE_CXX_COMPILER}")
message(STATUS "C++ flags: ${CMAKE_CXX_FLAGS}")
