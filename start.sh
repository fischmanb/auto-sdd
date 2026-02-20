#!/bin/bash
# Start all model servers

set -e

MODELS_DIR="${HOME}/ai-models"
LLAMA_DIR="./llama.cpp"

echo "Starting AI Model Servers (256GB Optimized)"
echo "============================================"
echo ""

# Check binaries exist
if [ ! -f "$LLAMA_DIR/build/bin/llama-server" ]; then
    echo "Error: llama-server not found. Run ./install.sh first"
    exit 1
fi

# Check models exist
for model in qwen2.5-coder-32b-instruct-q4_k_m.gguf \
             deepseek-coder-v2-lite-instruct-q4_k_m.gguf \
             qwen2.5-14b-instruct-q4_k_m.gguf; do
    if [ ! -f "$MODELS_DIR/$model" ]; then
        echo "Error: $model not found. Run ./download-models.sh first"
        exit 1
    fi
done

mkdir -p logs

# Start Builder (Port 8080)
echo "[1/3] Starting Builder (Qwen 32B) on port 8080..."
nohup "$LLAMA_DIR/build/bin/llama-server" \
    -m "$MODELS_DIR/qwen2.5-coder-32b-instruct-q4_k_m.gguf" \
    -c 128000 -n 4096 -t 16 \
    --host 127.0.0.1 --port 8080 \
    -ngl 999 --mlock \
    > logs/builder.log 2>&1 &
echo $! > .builder.pid

# Start Reviewer (Port 8081)
echo "[2/3] Starting Reviewer (DeepSeek 16B) on port 8081..."
nohup "$LLAMA_DIR/build/bin/llama-server" \
    -m "$MODELS_DIR/deepseek-coder-v2-lite-instruct-q4_k_m.gguf" \
    -c 64000 -n 2048 -t 8 \
    --host 127.0.0.1 --port 8081 \
    -ngl 999 --mlock \
    > logs/reviewer.log 2>&1 &
echo $! > .reviewer.pid

# Start Drift (Port 8082)
echo "[3/3] Starting Drift Checker (Qwen 14B) on port 8082..."
nohup "$LLAMA_DIR/build/bin/llama-server" \
    -m "$MODELS_DIR/qwen2.5-14b-instruct-q4_k_m.gguf" \
    -c 64000 -n 2048 -t 8 \
    --host 127.0.0.1 --port 8082 \
    -ngl 999 --mlock \
    > logs/drift.log 2>&1 &
echo $! > .drift.pid

echo ""
echo "Waiting for servers to initialize (30s)..."
sleep 30

echo ""
echo "Status:"
for port in 8080 8081 8082; do
    if curl -s "http://127.0.0.1:$port/health" > /dev/null 2>&1; then
        echo "  ✓ Port $port: Online"
    else
        echo "  ✗ Port $port: Starting..."
    fi
done

echo ""
echo "Logs: tail -f logs/*.log"
echo "Stop: ./stop.sh"
