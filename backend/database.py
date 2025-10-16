"""
Database configuration and session management for PostgreSQL
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL from environment variable or default to local PostgreSQL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://nepse_user:nepse_password@localhost:5432/nepse_db"
)

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for declarative models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Dependency function to get database session
    Yields a database session and ensures it's closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
