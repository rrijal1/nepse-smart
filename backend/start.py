#!/usr/bin/env python3
"""
Production startup script for NEPSE Analytics API
"""
import os
from pathlib import Path
import uvicorn

# Change to backend directory
os.chdir(Path(__file__).parent)

# Import the main application
from main import app

if __name__ == "__main__":
    print("🚀 Starting NEPSE Analytics API...")
    print("📊 Using our own scraped data")
    print("🌐 API Documentation: http://localhost:8000/docs")
    
    # Kill any existing process on port 8000
    os.system("lsof -ti:8000 | xargs kill -9 2>/dev/null || true")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)