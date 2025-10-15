#!/bin/bash
# NEPSE Smart - Environment Setup Script
# This script sets up a unified virtual environment for all components

set -e

echo "🚀 Setting up NEPSE Smart Development Environment"
echo "=================================================="

# Check Python version
python_version=$(python3 --version 2>&1 | cut -d' ' -f2)
echo "Python version: $python_version"

# Create virtual environment
if [ ! -d "nepse-smart" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv nepse-smart
    echo "✅ Virtual environment created"
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source nepse-smart/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the environment: source nepse-smart/bin/activate"
echo "   2. Test data scraper: cd data-scraper && python test_scraper.py"
echo "   3. Start API server: cd data-scraper && python api.py"
echo "   4. Launch dashboard: cd data-scraper && streamlit run dashboard.py"
echo "   5. Start frontend: cd frontend && npm run dev"
echo "   6. Start backend: cd backend && python main.py"
echo ""
echo "🔧 Development commands:"
echo "   - Run scraper: python data-scraper/scraper.py"
echo "   - API docs: http://localhost:8001/docs"
echo "   - Dashboard: http://localhost:8501"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend: http://localhost:8000"