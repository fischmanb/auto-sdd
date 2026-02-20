#!/bin/bash
# Check model server status

echo "Model Server Status"
echo "==================="
echo ""

for port in 8080 8081 8082; do
    NAME=""
    case $port in
        8080) NAME="Builder (Qwen 32B)" ;;
        8081) NAME="Reviewer (DeepSeek 16B)" ;;
        8082) NAME="Drift (Qwen 14B)" ;;
    esac
    
    if curl -s "http://127.0.0.1:$port/health" > /dev/null 2>&1; then
        echo "✓ $NAME on port $port: ONLINE"
    else
        echo "✗ $NAME on port $port: OFFLINE"
    fi
done

echo ""
echo "Memory Usage:"
vm_stat | grep -E "(free|active|inactive|wired)" | head -4
