#!/usr/bin/env python3
"""
Script to create database tables.
"""

import sys
from pathlib import Path

# Add the backend directory to the path so we can import our modules
# This is necessary because the script is in the root directory but needs to import from backend/
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

try:
    from database import engine, Base  # type: ignore
    from models import *  # type: ignore
except ImportError as e:
    print(f"Error importing backend modules: {e}")
    print("Make sure you're running this script from the project root directory.")
    sys.exit(1)

def create_tables():
    """Create all database tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")

if __name__ == "__main__":
    create_tables()