#!/bin/bash
# Download quantized models (optimized for 2Gbps+ connections)

set -e

MODELS_DIR="${HOME}/ai-models"
mkdir -p "$MODELS_DIR"

echo "Downloading models to $MODELS_DIR..."
echo "Estimated time: 10-15 minutes on 2Gbps fiber"
echo ""

# Install huggingface-cli if needed
if ! command -v huggingface-cli &> /dev/null; then
    pip3 install -q huggingface-hub hf-transfer
fi

export HF_HUB_ENABLE_HF_TRANSFER=1

cd "$MODELS_DIR"

# Qwen 32B (Builder)
echo "[1/3] Downloading Qwen2.5-Coder-32B (~20GB)..."
huggingface-cli download \
    Qwen/Qwen2.5-Coder-32B-Instruct-GGUF \
    qwen2.5-coder-32b-instruct-q4_k_m.gguf \
    --local-dir . \
    --local-dir-use-symlinks False

# DeepSeek 16B (Reviewer)
echo "[2/3] Downloading DeepSeek-Coder-V2-16B (~10GB)..."
huggingface-cli download \
    deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct-GGUF \
    deepseek-coder-v2-lite-instruct-q4_k_m.gguf \
    --local-dir . \
    --local-dir-use-symlinks False

# Qwen 14B (Drift)
echo "[3/3] Downloading Qwen2.5-14B (~9GB)..."
huggingface-cli download \
    Qwen/Qwen2.5-14B-Instruct-GGUF \
    qwen2.5-14b-instruct-q4_k_m.gguf \
    --local-dir . \
    --local-dir-use-symlinks False

echo ""
echo "✓ All models downloaded"
ls -lh *.gguf
