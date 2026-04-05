# Use Python 3.11 slim for minimal image size
FROM python:3.11-slim

# Metadata
LABEL maintainer="OpenEnv Hackathon"
LABEL org.opencontainers.image.description="Customer Email Triage OpenEnv Environment"

# Working directory
WORKDIR /app

# Install dependencies first (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY server/ ./server/
COPY inference.py .
COPY openenv.yaml .

# Create non-root user for security
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Expose port
EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')" || exit 1

# Start the FastAPI server
# HuggingFace Spaces uses port 7860
CMD ["uvicorn", "server.main:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
