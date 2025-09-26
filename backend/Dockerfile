# Backend Dockerfile for NEPSE Analytics
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements first for better caching
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy the entire project structure
COPY . .

# Install the NEPSE API library in editable mode
WORKDIR /app
RUN cd api && pip install -e .

# Set working directory to backend
WORKDIR /app/backend

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["python", "main.py"]