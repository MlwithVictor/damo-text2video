# Base image
FROM python:3.10-slim

# Build args (defaults)
ARG MODEL_ID=damo-vilab/modelscope-text-to-video-synthesis
ARG OUTPUT_DIR=/app/videos
ARG HOST=0.0.0.0
ARG PORT=8000
ARG CUDA_DEVICE=cpu
ARG LOG_LEVEL=info
ARG WORKERS=1
ARG HF_HOME=/cache/hf
ARG DISABLE_TELEMETRY=true

# Set environment variables
ENV MODEL_ID=${MODEL_ID}
ENV OUTPUT_DIR=${OUTPUT_DIR}
ENV HOST=${HOST}
ENV PORT=${PORT}
ENV CUDA_DEVICE=${CUDA_DEVICE}
ENV LOG_LEVEL=${LOG_LEVEL}
ENV WORKERS=${WORKERS}
ENV HF_HOME=${HF_HOME}
ENV DISABLE_TELEMETRY=${DISABLE_TELEMETRY}

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y git ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app

# Expose port
EXPOSE ${PORT}

# Run Uvicorn with dynamic settings
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--log-level", "info", \
     "--workers", "1"]
