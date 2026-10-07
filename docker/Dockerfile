# Minimal pinned base image (Debian-based slim)
FROM python:3.12-slim

# Create dedicated unprivileged user for security compliance (non-root)
RUN useradd -m -u 1000 appuser

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code into the package directory
COPY app/ /app/app/

# Set ownership to appuser so SQLite database can be written
RUN chown -R appuser:appuser /app

# Configure Python environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV HOST=0.0.0.0
ENV PORT=8080

# Switch to non-root user
USER appuser

# Expose target port
EXPOSE 8080

# Container healthcheck probe
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health')" || exit 1

# Launch application
CMD ["python", "-m", "app.app"]
