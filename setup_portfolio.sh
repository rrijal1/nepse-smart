#!/bin/bash
# Setup script for NEPSE Smart Portfolio Feature
# Installs database dependencies and initializes the database

set -e  # Exit on error

echo "🚀 NEPSE Smart - Portfolio Feature Setup"
echo "========================================"

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Please run from project root."
    exit 1
fi

echo ""
echo "📦 Step 1: Installing Python dependencies..."
echo "-------------------------------------------"
pip3 install -r requirements.txt

echo ""
echo "✅ Dependencies installed successfully!"

echo ""
echo "🐘 Step 2: Starting PostgreSQL with Docker..."
echo "---------------------------------------------"
docker-compose up -d postgres

echo ""
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Check if PostgreSQL is running
if docker ps --filter "name=nepse-postgres" --format "{{.Names}}" | grep -q "nepse-postgres"; then
    echo "✅ PostgreSQL is running!"
else
    echo "❌ PostgreSQL failed to start. Please check Docker logs."
    exit 1
fi

echo ""
echo "🗄️  Step 3: Initializing database tables..."
echo "-------------------------------------------"

# Set DATABASE_URL for local development
export DATABASE_URL="postgresql://nepse_user:nepse_password@localhost:5432/nepse_db"

# Run database initialization
cd backend
python3 init_db.py
cd ..

echo ""
echo "✅ Database tables created successfully!"

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Your portfolio management system is ready!"
echo ""
echo "Next steps:"
echo "  1. Start the backend:  cd backend && python3 start.py"
echo "  2. Start the frontend: cd frontend && npm run dev"
echo "  3. Visit http://localhost:3000/my-corner"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo "PostgreSQL: localhost:5432 (user: nepse_user, db: nepse_db)"
echo ""
echo "To view database:"
echo "  docker exec -it nepse-postgres psql -U nepse_user -d nepse_db"
echo ""
