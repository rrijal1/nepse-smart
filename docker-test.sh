#!/bin/bash

# NEPSE Analytics - Docker Test Script

echo "🐳 Testing Docker Setup for NEPSE Analytics..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose first."
    exit 1
fi

echo "✅ Docker and docker-compose are available"

# Test development environment
echo ""
echo "🚀 Testing development environment..."
echo "This will start the development containers with hot reload."
echo "You can stop with Ctrl+C"
echo ""

read -p "Start development environment? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting development environment..."
    docker-compose -f docker-compose.dev.yml up --build
else
    echo "Skipping development test."
fi

echo ""
echo "📋 Available Docker commands:"
echo ""
echo "Development:"
echo "  docker-compose -f docker-compose.dev.yml up --build"
echo ""
echo "Production:"
echo "  docker-compose -f docker-compose.prod.yml up --build"
echo ""
echo "Single container:"
echo "  docker build -t nepse-analytics . && docker run -p 8000:8000 nepse-analytics"
echo ""
echo "See DOCKER.md for complete documentation."