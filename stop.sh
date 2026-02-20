#!/bin/bash
# Stop all model servers

echo "Stopping model servers..."

for pidfile in .builder.pid .reviewer.pid .drift.pid; do
    if [ -f "$pidfile" ]; then
        PID=$(cat "$pidfile")
        if kill "$PID" 2>/dev/null; then
            echo "  ✓ Stopped $pidfile (PID: $PID)"
        fi
        rm -f "$pidfile"
    fi
done

echo "All servers stopped"
