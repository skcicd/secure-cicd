# Use a minimal base image
FROM python:3.11-slim AS builder

# Install necessary dependencies including curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set environment variables to improve security
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set a work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- Production Image ----
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -g 1000 appgroup && useradd -m -u 1000 -g appgroup appuser

# Set work directory
WORKDIR /app

# Copy dependencies from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application files
COPY . .

# Ensure entrypoint script has execution permissions
RUN chmod +x /app/entrypoint.sh

# Use non-root user AFTER the user is created
USER appuser

# Expose application port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
