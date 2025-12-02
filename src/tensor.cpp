#include "tensor.h"
#include <iostream>
#include <numeric>
#include <cstdlib>
#include <cstring>

Tensor::Tensor(const std::vector<size_t>& shape, DataType dtype, Device device)
    : shape_(shape), dtype_(dtype), device_(device), data_(nullptr) {
    
    size_ = std::accumulate(shape.begin(), shape.end(), 1, std::multiplies<size_t>());
    allocate();
}

Tensor::~Tensor() {
    free();
}

const std::vector<size_t>& Tensor::get_shape() const { return shape_; }
DataType Tensor::get_dtype() const { return dtype_; }
Device Tensor::get_device() const { return device_; }
size_t Tensor::get_size() const { return size_; }

void* Tensor::get_data() { return data_; }
const void* Tensor::get_data() const { return data_; }

void Tensor::allocate() {
    size_t bytes = 0;
    switch (dtype_) {
        case DataType::FLOAT32: bytes = size_ * sizeof(float); break;
        case DataType::FLOAT16: bytes = size_ * 2; break; // Placeholder
        case DataType::INT8:    bytes = size_ * 1; break;
        case DataType::INT4:    bytes = (size_ + 1) / 2; break; // Packed
        case DataType::INT2:    bytes = (size_ + 3) / 4; break; // Packed
        case DataType::BIT1:    bytes = (size_ + 7) / 8; break; // Packed
    }

    if (device_ == Device::CPU) {
        data_ = std::malloc(bytes);
        // Initialize to zero for safety
        std::memset(data_, 0, bytes);
    } else {
        // TODO: CUDA malloc
        std::cerr << "GPU allocation not yet implemented" << std::endl;
        data_ = nullptr;
    }
}

void Tensor::free() {
    if (data_) {
        if (device_ == Device::CPU) {
            std::free(data_);
        } else {
            // TODO: CUDA free
        }
        data_ = nullptr;
    }
}

std::shared_ptr<Tensor> Tensor::matmul(const std::shared_ptr<Tensor>& a, const std::shared_ptr<Tensor>& b) {
    // Placeholder for matrix multiplication logic
    // This is where the optimized kernels (XNOR, etc.) would be dispatched
    std::cout << "Executing matmul..." << std::endl;
    
    // Check dimensions, types, etc.
    
    // Return result
    // For now, return a dummy tensor
    return std::make_shared<Tensor>(std::vector<size_t>{a->get_shape()[0], b->get_shape()[1]}, DataType::FLOAT32);
}

void Tensor::quantize(DataType target_type) {
    // Placeholder for quantization logic
    std::cout << "Quantizing tensor..." << std::endl;
}

void Tensor::dequantize(DataType target_type) {
    // Placeholder for dequantization logic
    std::cout << "Dequantizing tensor..." << std::endl;
}
