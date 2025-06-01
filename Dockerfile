# Author: Gari Arellano
# Date: 2025
# Description: Dockerfile for the MITRE CALDERA


FROM python:3.11-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application
COPY src/ /app/src/

# Create necessary directories
RUN mkdir -p /app/src/Service/builds
RUN mkdir -p /app/src/repository
RUN mkdir -p /app/logs


# Set environment variables
ENV PYTHONPATH=/app

# Default command
CMD ["python", "src/main.py"]

# You can override the CMD with your custom command when running the container
# Example: docker run -it --rm your-image python src/your_script.py 
# Example2: docker run --env-file .env mitre-caldera-client