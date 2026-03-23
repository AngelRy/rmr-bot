FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app


# Install system deps (if needed later for Pillow/fonts)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project
COPY requirements.runtime.txt .
# Install Python deps
RUN pip install --no-cache-dir --default-timeout=100 -r requirements.runtime.txt

COPY rmrbot/ rmrbot/
COPY tests/ tests/
COPY assets/ assets/

# Default command (can override)
CMD ["python", "rmrbot/pipeline.py"]