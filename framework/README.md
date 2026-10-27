# Digital Twin Metamorphic Testing Framework (Docker)

This directory contains the testing framework for metamorphic testing of digital twins (Eclipse Ditto / Living Lab).

The framework is fully containerized and runs on any platform (macOS, Linux, Raspberry Pi, Windows).

---

## 1. Network & IP Architecture (`DITTO_NGINX_IP`)

The target IP is centrally configured via the `.env` file (fallback defined in [`pytest_dt_mt/config.py`](pytest_dt_mt/config.py)):
```python
DITTO_NGINX_IP = os.getenv("DITTO_NGINX_IP", "127.0.0.1")
```

### Seamless Support Across All Environments:
1. **Remote / Living Lab (configured IP via `.env`):**
   - The container connects directly to the specified IP through Docker's bridge network 
2. **Local Host (`127.0.0.1` or `localhost`):**
   - When the digital twin / mock backend runs on the same machine as Docker:
   - The entrypoint script ([`entrypoint.sh`](entrypoint.sh)) detects `127.0.0.1` and automatically establishes a transparent `socat` bridge to `host.docker.internal`.
   - On Linux systems, the Docker gateway is dynamically detected and mapped to `host.docker.internal` if needed.
3. **Host Networking on Linux / Raspberry Pi:**
   - Using `--network host` allows the container to directly access the host's network stack without port mapping.

---

## 2. Quickstart with Docker Compose (Recommended)

### Build the Image & Run Tests
```bash
cd framework

# Run default test suite (uses DITTO_NGINX_IP from .env or config)
docker compose up

# Rebuild image after code modifications:
docker compose build
```

### Configuration via Environment Variables (`.env`)
Copy the template configuration:
```bash
cp .env.example .env
```
Adjust parameters in `.env` as required:
```ini
DITTO_NGINX_IP=uibk_ip
UT_TENANT=at.uibk.ut.tenants
DITTO_USER=ditto
DITTO_PW=ditto
```

### Running Specific Commands with Docker Compose
```bash
# 1. Synchronize device catalog from digital twin:
docker compose run --rm framework python3 discover_catalog.py

# 2. Run specific Living Lab scenarios:
docker compose run --rm framework pytest tests/test_dsl_runner.py -k "s1_living_lab" -v --monitor

# 3. Open an interactive shell inside the container:
docker compose run --rm framework bash
```

---

## 3. Direct Usage with `docker run`

### Build the Image
```bash
docker build -t mt-framework .
```

### Default Execution
```bash
docker run --rm -it mt-framework
```


### With Volume Mounts (Persisting Test Reports & Editing Scenarios)
```bash
docker run --rm -it \
  -e DITTO_NGINX_IP=138.232.15.249 \
  -v "$(pwd)/test_reports:/app/test_reports" \
  -v "$(pwd)/dsl/scenarios:/app/dsl/scenarios" \
  -v "$(pwd)/device_catalog.json:/app/device_catalog.json" \
  mt-framework pytest tests/test_dsl_runner.py -k "s1_monotony" -v --monitor --log
```

---

## 4. Key Files

- [`Dockerfile`](Dockerfile): Multi-stage build combining Python 3.11 and Node.js 22 LTS (required for the Langium MT-DSL compiler).
- [`entrypoint.sh`](entrypoint.sh): Startup script managing dynamic host gateway resolution and port forwarding for `127.0.0.1`.
- [`docker-compose.yml`](docker-compose.yml): Pre-configured Compose setup including volume mounts for reports and test scenarios.
- [`.dockerignore`](.dockerignore): Excludes caches, logs, and `node_modules` from the Docker build context.
- [`requirements.txt`](requirements.txt): Python dependencies (`pytest`, `pytest-asyncio`, `pytest-repeat`, `httpx`, `requests`, `websockets`, `python-dotenv`).
- [`.env.example`](.env.example): Template for local environment variables.
