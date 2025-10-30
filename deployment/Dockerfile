# Oracle Production Dockerfile
# Week 11-12: Production Deployment Infrastructure
#
# Multi-stage build for optimized production image

################################################################################
# Stage 1: Base Python Image
################################################################################
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create app user
RUN useradd -m -u 1000 oracle && \
    mkdir -p /app && \
    chown -R oracle:oracle /app

WORKDIR /app

################################################################################
# Stage 2: Dependencies
################################################################################
FROM base as dependencies

# Copy only requirements to leverage Docker cache
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

################################################################################
# Stage 3: Application
################################################################################
FROM dependencies as application

# Build arguments
ARG BUILD_TIME
ARG GIT_COMMIT
ARG ENVIRONMENT=production

# Set labels
LABEL maintainer="Oracle Team"
LABEL version="1.0.0"
LABEL description="Oracle Meta-Agent System for Justice League"
LABEL build.time="${BUILD_TIME}"
LABEL git.commit="${GIT_COMMIT}"
LABEL environment="${ENVIRONMENT}"

# Copy application code
COPY --chown=oracle:oracle . /app/

# Create necessary directories
RUN mkdir -p /app/logs /app/data /app/backups && \
    chown -R oracle:oracle /app/logs /app/data /app/backups

# Switch to non-root user
USER oracle

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python3 /app/deployment/health_check.py || exit 1

# Expose ports (if needed for future API)
EXPOSE 8000

# Set environment
ENV ENVIRONMENT=${ENVIRONMENT}

# Default command
CMD ["python3", "-m", "core.oracle_integration.superman_connector"]
