# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY api/ api/
COPY common/ common/
COPY temporal/ temporal/
COPY workers/ workers/

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TEMPORAL_HOST=temporal:7233

# Expose the API port
EXPOSE 8080

# Command to run the application
CMD ["python", "-m", "api.main"]
