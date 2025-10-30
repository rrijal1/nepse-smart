"""
Data Management Utilities for NEPSE Smart
Handles data storage, cleanup, and retention policies
"""
import os
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from sqlalchemy import text
from backend.database import SessionLocal, engine
from backend.models import HistoricalPriceVolume, Base
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataManager:
    """Manages data storage and cleanup operations"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)

    def save_to_postgres(self, data: List[Dict[str, Any]], table_name: str = "historical_price_volume") -> int:
        """
        Save historical price/volume data to PostgreSQL

        Args:
            data: List of dictionaries containing price/volume data
            table_name: Target table name (default: historical_price_volume)

        Returns:
            Number of records saved (0 if database unavailable)
        """
        saved_count = 0

        try:
            with SessionLocal() as session:
                for record in data:
                    # Create HistoricalPriceVolume record
                    db_record = HistoricalPriceVolume(
                        symbol=record.get('symbol', ''),
                        business_date=datetime.strptime(record['businessDate'], '%Y-%m-%d').date(),
                        open_price=record.get('openPrice'),  # May not be available in some data
                        high_price=record['highPrice'],
                        low_price=record['lowPrice'],
                        close_price=record['closePrice'],
                        total_trades=record['totalTrades'],
                        total_traded_quantity=record['totalTradedQuantity'],
                        total_traded_value=record['totalTradedValue']
                    )

                    # Check if record already exists
                    existing = session.query(HistoricalPriceVolume).filter_by(
                        symbol=db_record.symbol,
                        business_date=db_record.business_date
                    ).first()

                    if not existing:
                        session.add(db_record)
                        saved_count += 1

                session.commit()
                logger.info(f"✅ Saved {saved_count} records to PostgreSQL")

        except Exception as e:
            logger.warning(f"⚠️ Database save failed (continuing with JSON only): {e}")
            return 0

        return saved_count

    def save_to_json(self, data: List[Dict[str, Any]], filename: str) -> None:
        """
        Save data to JSON file (for GitHub storage)

        Args:
            data: List of dictionaries containing data
            filename: Target filename
        """
        filepath = self.data_dir / "daily" / filename
        filepath.parent.mkdir(exist_ok=True)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"✅ Saved {len(data)} records to {filepath}")

    def save_historical_data(self, data: List[Dict[str, Any]], date_str: str,
                           save_to_db: bool = True, save_to_json: bool = True) -> Dict[str, Any]:
        """
        Save historical data to both PostgreSQL and JSON (if enabled)

        Args:
            data: Historical price/volume data
            date_str: Date string for filename
            save_to_db: Whether to save to PostgreSQL
            save_to_json: Whether to save to JSON file

        Returns:
            Summary of save operations
        """
        results = {
            'date': date_str,
            'total_records': len(data),
            'saved_to_db': 0,
            'saved_to_json': save_to_json
        }

        # Save to PostgreSQL
        if save_to_db:
            try:
                results['saved_to_db'] = self.save_to_postgres(data)
            except Exception as e:
                logger.error(f"Failed to save to database: {e}")
                results['db_error'] = str(e)

        # Save to JSON (for recent data only)
        if save_to_json:
            filename = f"{date_str}_price_volume_history_{date_str.replace('-', '_')}.json"
            self.save_to_json(data, filename)

        return results

    def cleanup_old_data(self, keep_days: int = 30) -> Dict[str, Any]:
        """
        Remove old JSON files, keeping only recent data

        Args:
            keep_days: Number of days of data to keep in JSON files

        Returns:
            Cleanup summary
        """
        daily_dir = self.data_dir / "daily"
        if not daily_dir.exists():
            return {'files_removed': 0, 'error': 'Daily directory not found'}

        cutoff_date = datetime.now() - timedelta(days=keep_days)
        removed_files = []

        # Find and remove old files
        for json_file in daily_dir.glob("*_price_volume_history_*.json"):
            try:
                # Extract date from filename (format: YYYY-MM-DD_price_volume_history_YYYY_MM_DD.json)
                date_part = json_file.stem.split('_price_volume_history_')[1]
                file_date = datetime.strptime(date_part.replace('_', '-'), '%Y-%m-%d')

                if file_date < cutoff_date:
                    json_file.unlink()
                    removed_files.append(json_file.name)
                    logger.info(f"🗑️ Removed old file: {json_file.name}")

            except (ValueError, IndexError) as e:
                logger.warning(f"Could not parse date from filename {json_file.name}: {e}")

        return {
            'files_removed': len(removed_files),
            'files_kept': len(list(daily_dir.glob("*_price_volume_history_*.json"))),
            'cutoff_date': cutoff_date.strftime('%Y-%m-%d'),
            'removed_files': removed_files
        }

    def get_data_summary(self) -> Dict[str, Any]:
        """
        Get summary of current data storage

        Returns:
            Data storage summary
        """
        daily_dir = self.data_dir / "daily"

        json_files = list(daily_dir.glob("*_price_volume_history_*.json")) if daily_dir.exists() else []

        # Count records in database
        db_count = 0
        try:
            with SessionLocal() as session:
                db_count = session.query(HistoricalPriceVolume).count()
        except Exception as e:
            logger.warning(f"⚠️ Could not query database: {e}")

        return {
            'json_files_count': len(json_files),
            'database_records_count': db_count,
            'total_storage': sum(f.stat().st_size for f in json_files) if json_files else 0,
            'date_range': self._get_date_range(json_files)
        }

    def _get_date_range(self, files: List[Path]) -> Dict[str, Optional[str]]:
        """Get date range from JSON files"""
        dates = []
        for file in files:
            try:
                date_part = file.stem.split('_price_volume_history_')[1]
                dates.append(datetime.strptime(date_part.replace('_', '-'), '%Y-%m-%d'))
            except:
                continue

        if not dates:
            return {'oldest': None, 'newest': None}

        return {
            'oldest': min(dates).strftime('%Y-%m-%d'),
            'newest': max(dates).strftime('%Y-%m-%d')
        }

def init_database():
    """Initialize database tables"""
    try:
        # Create schema if it doesn't exist
        with engine.connect() as conn:
            conn.execute(text("CREATE SCHEMA IF NOT EXISTS nepse_data"))
            conn.commit()

        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized")

    except Exception as e:
        logger.warning(f"⚠️ Database initialization failed (continuing without DB): {e}")
        logger.info("💡 Data will be saved to JSON files only")
        # Don't raise exception - allow operation without database

if __name__ == "__main__":
    # Initialize database when run directly
    init_database()

    # Example usage
    manager = DataManager()
    summary = manager.get_data_summary()
    print("Data Summary:", json.dumps(summary, indent=2))