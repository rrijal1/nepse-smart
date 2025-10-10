# Optimized Multi-stage Dockerfile for NEPSE Analytics
# Fast builds with better caching and parallel stages

# Stage 1: Frontend Build (can run in parallel)
FROM node:18-alpine as frontend-build
WORKDIR /app/frontend

# Copy package files first for better caching
COPY frontend/package*.json ./
COPY frontend/tsconfig*.json ./
COPY frontend/vite.config.ts ./

# Install dependencies (cached layer)
RUN npm ci --prefer-offline --no-audit

# Copy source code and build
COPY frontend/src ./src
COPY frontend/index.html ./
RUN npm run build

# Stage 2: Python dependencies (can run in parallel)
FROM python:3.11-slim as python-deps
WORKDIR /app

# Install system dependencies in one layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Install Python packages with better caching
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Stage 3: NEPSE API build
FROM python-deps as nepse-api
COPY api/ ./api/
RUN cd api && pip install -e . --no-deps

# Stage 4: Final production stage
FROM python-deps as production
WORKDIR /app

# Copy Python dependencies from previous stages
COPY --from=nepse-api /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=nepse-api /usr/local/bin /usr/local/bin

# Copy API library
COPY api/ ./api/

# Copy backend code (only what's needed)
COPY backend/main.py ./
COPY backend/start.py ./
COPY backend/agent_routes.py ./
COPY backend/agents/ ./agents/

# Copy frontend build
COPY --from=frontend-build /app/frontend/dist ./static

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash nepse
USER nepse

# Expose port
EXPOSE 8000

# Optimized health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=2 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["python", "main.py"]