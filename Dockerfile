# Use a minimal base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    TMPDIR=/app/tmp

# Install system dependencies
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements first (for efficient Docker layer caching)
COPY requirements.txt .

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Ensure entrypoint script has execution permissions
RUN chmod +x /app/entrypoint.sh

# Create non-root user
RUN groupadd -g 1000 appgroup && useradd -m -u 1000 -g appgroup appuser

# Create required directories and set ownership
RUN mkdir -p /app/instance /app/tmp && chmod 1777 /app/tmp
RUN chown -R 1000:1000 /app  # Change ownership of /app to appuser

# Change ownership of all files to appuser
RUN chown -R appuser:appgroup /app

# Use non-root user
USER appuser

# Expose application port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD curl -f http://localhost:5000/ || exit 1

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

