#!/usr/bin/env python3
import sys
import os
from pathlib import Path

# Add the API directory to the Python path
api_path = Path(__file__).parent.parent / "API"
sys.path.insert(0, str(api_path))

# Change to backend directory
os.chdir(Path(__file__).parent)

# Now import and run the main application
from main import app
import uvicorn

if __name__ == "__main__":
    # Kill any existing process on port 8001
    os.system("lsof -ti:8001 | xargs kill -9 2>/dev/null || true")
    uvicorn.run(app, host="0.0.0.0", port=8001)