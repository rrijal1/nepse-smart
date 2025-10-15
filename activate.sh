#!/bin/bash
# NEPSE Smart - Quick Activation Script
# Use: source activate.sh (or . activate.sh)

if [ -d "nepse-smart" ]; then
    source nepse-smart/bin/activate
    echo "✅ NEPSE Smart virtual environment activated!"
    echo "📍 Current environment: $VIRTUAL_ENV"
    echo ""
    echo "🛠️  Available commands:"
    echo "   python data-scraper/scraper.py    - Run data scraper"
    echo "   python data-scraper/api.py        - Start API server"
    echo "   streamlit run data-scraper/dashboard.py - Start dashboard"
    echo ""
else
    echo "❌ Virtual environment 'nepse-smart' not found!"
    echo "💡 Run './setup.sh' first to create the environment"
fi