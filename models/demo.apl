# Demo Model Definition in APL
# Run this with: Source 'models/demo.apl'

# Define a simple CNN-like structure
Layer 'Input' 'Conv2d' 3 64 3
Layer 'Relu1' 'ReLU'
Layer 'Pool1' 'MaxPool2d' 2
Layer 'Flat' 'Flatten'
Layer 'FC1' 'Linear' 1024 128
Layer 'Output' 'Linear' 128 10

# Initialize some variables
LearningRate <- 0.001
BatchSize <- 32
