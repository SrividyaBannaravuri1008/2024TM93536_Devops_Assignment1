# ---------- Build Stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies separately to leverage Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---------- Runtime Stage ----------
FROM python:3.11-slim

# Create a non-root user for security
RUN groupadd -r aceest && useradd -r -g aceest aceest

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application source
COPY app.py .
COPY requirements.txt .

# Copy tests (needed for CI test stage)
COPY tests/ ./tests/

# Use non-root user
USER aceest

# Expose application port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Run Flask application
CMD ["python", "app.py"]
