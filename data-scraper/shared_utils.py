#!/usr/bin/env python3
"""
Shared utilities for NEPSE data scrapers
- Common scraping infrastructure
- HTTP session management and retry logic
- Data validation and file operations
- Logging setup and error handling
"""

import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def setup_logging(scraper_name: str) -> logging.Logger:
    """Set up logging for scrapers"""
    logger = logging.getLogger(scraper_name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler for logs directory
        logs_dir = Path(__file__).parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        log_file = logs_dir / f"{scraper_name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

def create_http_session() -> requests.Session:
    """Create configured HTTP session with retry strategy"""
    session = requests.Session()
    
    # Set up retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    # Set headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    })
    return session

def clean_numeric_value(value: Any) -> Optional[float]:
    """Clean and convert numeric values"""
    if not value or value in ['', '-', 'N/A', 'null', 'None']:
        return None
    
    try:
        # Remove commas, spaces, and percentage signs
        cleaned = re.sub(r'[,\s%]', '', str(value))
        return float(cleaned)
    except (ValueError, TypeError):
        return None

def save_json_data(data: Any, filepath: str, logger: Optional[logging.Logger] = None) -> bool:
    """Save data to JSON file with error handling"""
    try:
        # Ensure directory exists
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
        
        if logger:
            logger.info(f"✅ Saved data to {filepath}")
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"❌ Failed to save data to {filepath}: {e}")
        print(f"❌ Failed to save data to {filepath}: {e}")
        return False

def validate_data_structure(data: Any, expected_keys: List[str], min_records: int = 1) -> Dict[str, Any]:
    """Validate data structure and return validation results"""
    validation = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'record_count': 0
    }
    
    if not data:
        validation['valid'] = False
        validation['errors'].append("No data provided")
        return validation
    
    if not isinstance(data, list):
        validation['valid'] = False
        validation['errors'].append("Data must be a list of records")
        return validation
    
    validation['record_count'] = len(data)
    
    if len(data) < min_records:
        validation['valid'] = False
        validation['errors'].append(f"Insufficient records: {len(data)} < {min_records}")
    
    # Check first few records for expected keys
    for i, record in enumerate(data[:5]):
        if not isinstance(record, dict):
            validation['warnings'].append(f"Record {i} is not a dictionary")
            continue
        
        missing_keys = [key for key in expected_keys if key not in record]
        if missing_keys:
            validation['warnings'].append(f"Record {i} missing keys: {missing_keys}")
    
    return validation

def create_data_filepath(data_type: str, date: Optional[str] = None) -> str:
    """Create standardized data file path"""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    data_dir = Path(__file__).parent.parent / "data" / "daily"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{date}_{data_type}.json"
    return str(data_dir / filename)

def create_historical_filepath(data_type: str) -> str:
    """Create standardized historical data file path"""
    historical_dir = Path(__file__).parent.parent / "data" / "historical"
    historical_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"historical_{data_type}.json"
    return str(historical_dir / filename)

def append_to_historical_data(daily_filepath: str, historical_filepath: str, logger: Optional[logging.Logger] = None) -> bool:
    """Append daily data to historical data file"""
    try:
        # Check if daily file exists
        if not Path(daily_filepath).exists():
            if logger:
                logger.warning(f"Daily file not found: {daily_filepath}")
            return False
        
        # Load daily data
        with open(daily_filepath, 'r', encoding='utf-8') as f:
            daily_data = json.load(f)
        
        if not daily_data:
            if logger:
                logger.warning(f"No data in daily file: {daily_filepath}")
            return False
        
        # Load existing historical data or create empty list
        historical_data = []
        if Path(historical_filepath).exists():
            try:
                with open(historical_filepath, 'r', encoding='utf-8') as f:
                    historical_data = json.load(f)
            except json.JSONDecodeError:
                if logger:
                    logger.warning(f"Invalid JSON in historical file, starting fresh: {historical_filepath}")
                historical_data = []
        
        # Get the date from daily data to check for duplicates
        daily_date = None
        if isinstance(daily_data, list) and daily_data:
            daily_date = daily_data[0].get('date')
        
        # Remove any existing data for the same date (to handle re-runs)
        if daily_date and isinstance(historical_data, list):
            historical_data = [record for record in historical_data 
                             if isinstance(record, dict) and record.get('date') != daily_date]
        
        # Append new data
        if isinstance(daily_data, list):
            historical_data.extend(daily_data)
        else:
            historical_data.append(daily_data)
        
        # Sort by date (most recent first)
        if isinstance(historical_data, list) and historical_data:
            historical_data.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        # Save updated historical data
        with open(historical_filepath, 'w', encoding='utf-8') as f:
            json.dump(historical_data, f, indent=2, default=str, ensure_ascii=False)
        
        if logger:
            logger.info(f"✅ Updated historical data: {historical_filepath} ({len(daily_data)} new records)")
        return True
        
    except Exception as e:
        if logger:
            logger.error(f"❌ Failed to update historical data: {e}")
        print(f"❌ Failed to update historical data: {e}")
        return False

def manage_historical_data(data_type: str, daily_data: Any, date: Optional[str] = None, logger: Optional[logging.Logger] = None) -> Dict[str, bool]:
    """Complete historical data management - save daily and update historical"""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    results = {
        'daily_saved': False,
        'historical_updated': False
    }
    
    # Save daily data
    daily_filepath = create_data_filepath(data_type, date)
    results['daily_saved'] = save_json_data(daily_data, daily_filepath, logger)
    
    # Update historical data
    if results['daily_saved']:
        historical_filepath = create_historical_filepath(data_type)
        results['historical_updated'] = append_to_historical_data(daily_filepath, historical_filepath, logger)
    
    return results

class ScraperBase:
    """Base class for all NEPSE scrapers with common functionality"""
    
    def __init__(self, scraper_name: str):
        self.scraper_name = scraper_name
        self.logger = setup_logging(scraper_name)
        self.session = create_http_session()
        self.start_time = datetime.now()
    
    def make_request_with_retry(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                self.logger.info(f"✅ Request successful: {url}")
                return response
            
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"⚠️ Request attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    self.log_error(f"All {max_retries} attempts failed for {url}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
        return None
    
    def make_request(self, url: str, max_retries: int = 3) -> Optional[requests.Response]:
        """Make HTTP request with retry logic - wrapper method"""
        return self.make_request_with_retry(url, max_retries)
    
    def log_success(self, message: str):
        """Log success message"""
        self.logger.info(f"✅ {message}")
    
    def log_error(self, message: str):
        """Log error message"""
        self.logger.error(f"❌ {message}")
    
    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(f"⚠️ {message}")
    
    def save_data(self, data: Any, filepath: str) -> bool:
        """Save data using shared utility"""
        return save_json_data(data, filepath, self.logger)
    
    def save_with_history(self, data: Any, data_type: str, date: Optional[str] = None) -> Dict[str, bool]:
        """Save data with historical management"""
        return manage_historical_data(data_type, data, date, self.logger)
    
    def validate_data(self, data: Any, expected_keys: List[str], min_records: int = 1) -> Dict[str, Any]:
        """Validate data using shared utility"""
        return validate_data_structure(data, expected_keys, min_records)
    
    def get_runtime(self) -> str:
        """Get elapsed runtime"""
        elapsed = datetime.now() - self.start_time
        return str(elapsed)
    
    def close_session(self):
        """Close HTTP session"""
        if self.session:
            self.session.close()

def main():
    """Test shared utilities"""
    print("🧪 Testing shared utilities...")
    
    # Test logging
    logger = setup_logging("test-scraper")
    logger.info("Logging test successful")
    
    # Test session
    session = create_http_session()
    print(f"Session created with headers: {session.headers}")
    
    # Test data validation
    test_data = [
        {"symbol": "NABIL", "price": 1200.50},
        {"symbol": "SCBL", "price": 890.25}
    ]
    
    validation = validate_data_structure(test_data, ["symbol", "price"], min_records=2)
    print(f"Validation result: {validation}")
    
    # Test file path creation
    filepath = create_data_filepath("test_data")
    print(f"Created filepath: {filepath}")
    
    print("✅ All utilities tested successfully!")

if __name__ == "__main__":
    main()