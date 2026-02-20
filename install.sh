#!/bin/bash
# Install llama.cpp with Metal support for M3 Ultra

set -e

echo "Installing llama.cpp for Apple Silicon..."

# Check for Metal
if ! system_profiler SPDisplaysDataType | grep -q "Metal"; then
    echo "Error: Metal not available"
    exit 1
fi

# Clone and build
if [ ! -d "llama.cpp" ]; then
    git clone --depth 1 https://github.com/ggerganov/llama.cpp.git
fi

cd llama.cpp

echo "Building with Metal support..."
cmake -B build \
    -DLLAMA_METAL=ON \
    -DLLAMA_METAL_EMBED_LIBRARY=ON \
    -DCMAKE_BUILD_TYPE=Release

cmake --build build --config Release -j $(sysctl -n hw.ncpu)

echo "✓ llama.cpp built successfully"
echo "Binary: $(pwd)/build/bin/llama-server"
