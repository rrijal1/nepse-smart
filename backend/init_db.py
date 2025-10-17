"""
Database initialization script
Creates all tables and optionally seeds sample data
"""
from backend.database import engine, Base
from backend.models import Watchlist, Portfolio, Transaction
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_database():
    """
    Initialize database by creating all tables
    """
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables created successfully!")
        logger.info(f"Tables created: {', '.join(Base.metadata.tables.keys())}")
    except Exception as e:
        logger.error(f"❌ Error creating database tables: {e}")
        raise

def drop_all_tables():
    """
    Drop all tables (use with caution!)
    """
    try:
        logger.warning("⚠️  Dropping all database tables...")
        Base.metadata.drop_all(bind=engine)
        logger.info("✅ All tables dropped successfully!")
    except Exception as e:
        logger.error(f"❌ Error dropping tables: {e}")
        raise

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        logger.warning("⚠️  RESET MODE: Dropping all tables first...")
        drop_all_tables()
    
    init_database()
    logger.info("🎉 Database initialization complete!")
