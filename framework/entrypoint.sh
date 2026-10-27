#!/usr/bin/env bash
set -e

echo "============================================================"
echo " Digital Twin Metamorphic Testing Framework (Docker)"
echo "============================================================"

# Resolve host.docker.internal dynamically if not already in /etc/hosts
if ! getent hosts host.docker.internal >/dev/null 2>&1; then
    HOST_GATEWAY=$(ip route show default 2>/dev/null | awk '{print $3}')
    if [ -n "$HOST_GATEWAY" ]; then
        echo "[Entrypoint] Mapping host.docker.internal to gateway $HOST_GATEWAY"
        echo "$HOST_GATEWAY host.docker.internal" >> /etc/hosts 2>/dev/null || true
    fi
fi

# Detect effective DITTO_NGINX_IP from config / env
EFFECTIVE_IP=$(python3 -c 'from pytest_dt_mt import config; print(config.DITTO_NGINX_IP)' 2>/dev/null || echo "${DITTO_NGINX_IP}")
echo "[Entrypoint] Effective DITTO_NGINX_IP: ${EFFECTIVE_IP}"

# If target is localhost / 127.0.0.1 and we are not using host network, setup socat forwarders to host
if [ "$EFFECTIVE_IP" = "127.0.0.1" ] || [ "$EFFECTIVE_IP" = "localhost" ]; then
    TARGET_HOST="host.docker.internal"
    if getent hosts "$TARGET_HOST" >/dev/null 2>&1; then
        # HTTP Ditto API (Port 8083)
        if ! nc -z 127.0.0.1 8083 >/dev/null 2>&1; then
            echo "[Entrypoint] Bridging container 127.0.0.1:8083 -> host ${TARGET_HOST}:8083 (HTTP)..."
            socat TCP-LISTEN:8083,fork,bind=127.0.0.1 TCP:${TARGET_HOST}:8083 &
        fi
        # WebSocket Ditto API (Port 8082)
        if ! nc -z 127.0.0.1 8082 >/dev/null 2>&1; then
            echo "[Entrypoint] Bridging container 127.0.0.1:8082 -> host ${TARGET_HOST}:8082 (WebSocket)..."
            socat TCP-LISTEN:8082,fork,bind=127.0.0.1 TCP:${TARGET_HOST}:8082 &
        fi
    fi
fi

echo "============================================================"

# Terminate background background proxies when the container stops
cleanup() {
    kill $(jobs -p) 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# If no arguments are passed, run standard test runner
if [ "$#" -eq 0 ]; then
    set -- pytest tests/test_dsl_runner.py -v --capture=tee-sys
fi

exec "$@"
