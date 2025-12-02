#include <iostream>
#include <cassert>
#include "../include/tensor.h"

void test_tensor_creation() {
    std::vector<size_t> shape = {2, 3};
    Tensor t(shape, DataType::FLOAT32);
    
    assert(t.get_shape() == shape);
    assert(t.get_dtype() == DataType::FLOAT32);
    assert(t.get_size() == 6);
    
    std::cout << "test_tensor_creation passed!" << std::endl;
}

int main() {
    test_tensor_creation();
    return 0;
}
