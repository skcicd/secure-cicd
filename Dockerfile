# Use a minimal base image
FROM python:3.11-slim AS builder

# Set environment variables to improve security
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100

# Set a non-root user for security
RUN groupadd -g 1000 appgroup && useradd -m -u 1000 -g appgroup appuser

# Set work directory
WORKDIR /app

# Copy only required files
COPY requirements.txt ./

# Install dependencies using a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# ---- Production Image ----
FROM python:3.11-slim

# Security configurations
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy app source
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
COPY . .

# Use non-root user
USER appuser

# Expose application port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Make the entrypoint script executable
RUN chmod +x /app/entrypoint.sh

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
