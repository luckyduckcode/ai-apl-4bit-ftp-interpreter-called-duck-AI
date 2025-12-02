#pragma once

#include <vector>
#include <cstdint>
#include <memory>
#include <string>

enum class DataType {
    FLOAT32,
    FLOAT16,
    INT8,
    INT4,
    INT2,
    BIT1 // 1-bit quantization
};

enum class Device {
    CPU,
    GPU
};

class Tensor {
public:
    Tensor(const std::vector<size_t>& shape, DataType dtype, Device device = Device::CPU);
    ~Tensor();

    // Basic accessors
    const std::vector<size_t>& get_shape() const;
    DataType get_dtype() const;
    Device get_device() const;
    size_t get_size() const; // Total number of elements

    // Data management
    void* get_data();
    const void* get_data() const;

    // Operations (placeholders)
    static std::shared_ptr<Tensor> matmul(const std::shared_ptr<Tensor>& a, const std::shared_ptr<Tensor>& b);
    
    // Quantization utilities
    void quantize(DataType target_type);
    void dequantize(DataType target_type);

private:
    std::vector<size_t> shape_;
    DataType dtype_;
    Device device_;
    size_t size_;
    void* data_; // Raw data pointer (could be host or device memory)
    
    void allocate();
    void free();
};
