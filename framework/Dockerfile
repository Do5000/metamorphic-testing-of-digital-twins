FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    IS_DOCKER=1 \
    PYTHONPATH=/app

# Install system dependencies:
# - socat & netcat: transparent proxying of localhost (127.0.0.1) to host machine
# - iproute2: dynamic default gateway discovery on Linux
# - curl & ca-certificates: network verification and SSL support
# - nodejs 22 LTS (via NodeSource): required by Langium DSL compiler (requires Node 21+ for Object.groupBy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    socat \
    netcat-openbsd \
    iproute2 \
    curl \
    ca-certificates \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first for optimal Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies for DSL
COPY dsl/package.json dsl/package-lock.json ./dsl/
RUN cd dsl && npm ci

# Copy the rest of the framework codebase
COPY . .

# Generate Langium parser and compile TypeScript DSL CLI
RUN cd dsl && \
    npm run langium:generate && \
    npm run build

# Ensure entrypoint is executable and report directory exists
RUN chmod +x /app/entrypoint.sh && mkdir -p /app/test_reports

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["pytest", "tests/test_dsl_runner.py", "-v", "--capture=tee-sys"]
