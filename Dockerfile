# Minimal Dockerfile for the ecosystem-builder project
# Uses a slim Python base, installs dependencies, and runs the app module

# Use the AWS Public ECR mirror of the official Python image to avoid Docker Hub rate limits
FROM public.ecr.aws/docker/library/python:3.11-slim

# Set a stable working directory
WORKDIR /app

# Prevent Python from writing .pyc files and enable stdout/stderr flushing
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies needed for common Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install (layered for caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Expose a default port (optional; adjust if your app uses a different one)
EXPOSE 8000

# Default command: run the app module. Adjust if you use gunicorn/uvicorn in production.
CMD ["python", "-m", "app.main"]
