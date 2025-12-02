cmake_minimum_required(VERSION 3.15)
project(AI_APL_Interpreter VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Optional CUDA support
option(USE_CUDA "Enable CUDA support" OFF)

if(USE_CUDA)
    enable_language(CUDA)
    add_definitions(-DUSE_CUDA)
endif()

include_directories(include)

# Source files
file(GLOB_RECURSE SOURCES "src/*.cpp")

# Add executable
add_executable(ai_apl ${SOURCES})

if(USE_CUDA)
    file(GLOB_RECURSE CUDA_SOURCES "src/*.cu")
    target_sources(ai_apl PRIVATE ${CUDA_SOURCES})
    set_target_properties(ai_apl PROPERTIES CUDA_SEPARABLE_COMPILATION ON)
endif()

# Link libraries (add others as needed, e.g., OpenMP, BLAS)
find_package(OpenMP)
if(OpenMP_CXX_FOUND)
    target_link_libraries(ai_apl PRIVATE OpenMP::OpenMP_CXX)
endif()

# Tests
enable_testing()
add_executable(test_tensor tests/test_tensor.cpp src/tensor.cpp)
add_test(NAME TensorTest COMMAND test_tensor)
