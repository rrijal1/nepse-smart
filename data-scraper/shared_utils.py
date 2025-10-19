#!/usr/bin/env python3
"""
Shared utilities for NEPSE data scrapers
- Common scraping infrastructure, session management, and retry logic.
- Data validation and standardized file/path operations.
- Centralized logging and error handling.

Refactoring Summary:
- Reorganized functions into logical sections for better readability.
- Centralized path creation logic to be more DRY.
- Added type hints and improved docstrings for clarity.
- Ensured all original public functions remain available.
"""

import json
import logging
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import certifi # <-- Added import for SSL certificate handling

# --- Constants & Path Management ---

def get_data_directory() -> Path:
    """Returns the base path for the 'data' directory."""
    return Path(__file__).resolve().parent.parent / "data"

def create_data_filepath(data_type: str, date: Optional[str] = None) -> str:
    """Creates a standardized filepath for daily data."""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    data_dir = get_data_directory() / "daily"
    data_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"{date}_{data_type}.json"
    return str(data_dir / filename)

def create_historical_filepath(data_type: str) -> str:
    """Creates a standardized filepath for historical data."""
    historical_dir = get_data_directory() / "historical"
    historical_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"historical_{data_type}.json"
    return str(historical_dir / filename)

# --- Logging Setup ---

def setup_logging(scraper_name: str) -> logging.Logger:
    """Sets up a logger with both console and file handlers."""
    logger = logging.getLogger(scraper_name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        # File handler
        logs_dir = Path(__file__).resolve().parent / "logs"
        logs_dir.mkdir(exist_ok=True)
        log_file = logs_dir / f"{scraper_name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger

# --- Data Handling & Validation ---

def clean_numeric_value(value: Any) -> Optional[float]:
    """Cleans and converts a value to a float, handling common non-numeric strings."""
    if value is None or isinstance(value, (int, float)):
        return value
    if isinstance(value, str):
        value = value.strip()
        if value in ['', '-', 'N/A', 'null', 'None']:
            return None
        try:
            # Remove commas and percentage signs for robust conversion
            cleaned = re.sub(r'[,\s%]', '', value)
            return float(cleaned)
        except (ValueError, TypeError):
            return None
    return None

def save_json_data(data: Any, filepath: str, logger: Optional[logging.Logger] = None) -> bool:
    """Saves data to a JSON file with proper encoding and error handling."""
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with path.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, default=str, ensure_ascii=False)
        
        if logger:
            logger.info(f"✅ Successfully saved data to {filepath}")
        return True
    except (IOError, TypeError) as e:
        if logger:
            logger.error(f"❌ Failed to save data to {filepath}: {e}")
        return False

def _load_json_safely(filepath: Path, logger: Optional[logging.Logger] = None) -> Optional[Any]:
    """Loads JSON data from a file, returning None on failure."""
    if not filepath.exists():
        return None
    try:
        with filepath.open('r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        if logger:
            logger.warning(f"⚠️ Could not load or parse JSON from {filepath}: {e}. Starting fresh.")
        return None

def validate_data_structure(data: Any, expected_keys: List[str], min_records: int = 1) -> Dict[str, Any]:
    """Validates that the data is a list of dicts with expected keys."""
    validation = {'valid': True, 'errors': [], 'warnings': [], 'record_count': 0}
    
    if not isinstance(data, list):
        validation['valid'] = False
        validation['errors'].append("Data must be a list of records.")
        return validation
    
    validation['record_count'] = len(data)
    
    if len(data) < min_records:
        validation['valid'] = False
        validation['errors'].append(f"Insufficient records: found {len(data)}, expected at least {min_records}.")
    
    # Check first few records for key existence
    for i, record in enumerate(data[:5]):
        if not isinstance(record, dict):
            validation['warnings'].append(f"Record {i} is not a dictionary.")
            continue
        missing_keys = [key for key in expected_keys if key not in record]
        if missing_keys:
            validation['warnings'].append(f"Record {i} is missing keys: {missing_keys}.")
            
    return validation

# --- Historical Data Management ---

def append_to_historical_data(daily_filepath_str: str, historical_filepath_str: str, logger: Optional[logging.Logger] = None) -> bool:
    """Appends data from a daily file to a historical file, handling duplicates."""
    daily_filepath = Path(daily_filepath_str)
    historical_filepath = Path(historical_filepath_str)

    daily_data = _load_json_safely(daily_filepath, logger)
    if not daily_data:
        if logger:
            logger.warning(f"Skipping history update: No data in daily file {daily_filepath}.")
        return False

    historical_data = _load_json_safely(historical_filepath, logger) or []
    if not isinstance(historical_data, list):
        if logger:
             logger.warning(f"Historical data in {historical_filepath} is not a list. Overwriting.")
        historical_data = []

    # Identify date from daily data to prevent duplicates
    daily_date = None
    if isinstance(daily_data, list) and daily_data and isinstance(daily_data[0], dict):
        daily_date = daily_data[0].get('date')
    
    if daily_date:
        # Filter out any records from the same date to allow for re-runs
        historical_data = [rec for rec in historical_data if isinstance(rec, dict) and rec.get('date') != daily_date]

    # Append new data and sort by date (most recent first)
    historical_data.extend(daily_data if isinstance(daily_data, list) else [daily_data])
    historical_data.sort(key=lambda x: x.get('date', '') if isinstance(x, dict) else '', reverse=True)
    
    return save_json_data(historical_data, str(historical_filepath), logger)


def manage_historical_data(data_type: str, daily_data: Any, date: Optional[str] = None, logger: Optional[logging.Logger] = None) -> Dict[str, bool]:
    """Orchestrates saving daily data and appending it to the historical archive."""
    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    
    daily_filepath = create_data_filepath(data_type, date)
    daily_saved = save_json_data(daily_data, daily_filepath, logger)
    
    historical_updated = False
    if daily_saved:
        historical_filepath = create_historical_filepath(data_type)
        historical_updated = append_to_historical_data(daily_filepath, historical_filepath, logger)
    
    return {'daily_saved': daily_saved, 'historical_updated': historical_updated}

# --- Scraper Base Class ---

class ScraperBase:
    """A base class for NEPSE scrapers providing common infrastructure."""
    
    def __init__(self, scraper_name: str):
        self.scraper_name = scraper_name
        self.logger = setup_logging(scraper_name)
        self.session = self._create_http_session()
        self.start_time = datetime.now()

    def _create_http_session(self) -> requests.Session:
        """Creates a requests.Session with a robust retry strategy."""
        session = requests.Session()

        # *** FIX: Use certifi's CA bundle for SSL verification ***
        try:
            session.verify = certifi.where()
            self.logger.info("Attached certifi's CA bundle to session for SSL verification.")
        except Exception as e:
            self.logger.warning(f"Could not attach certifi's CA bundle: {e}")

        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        })
        return session
    
    def make_request(self, url: str, timeout: int = 30) -> Optional[requests.Response]:
        """Makes an HTTP GET request using the configured session with retries."""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            self.logger.info(f"✅ Request successful for {url} (Status: {response.status_code})")
            return response
        except requests.exceptions.RequestException as e:
            self.log_error(f"Request failed for {url} after retries: {e}")
            return None
    
    def log_success(self, message: str):
        self.logger.info(f"✅ {message}")
    
    def log_error(self, message: str):
        self.logger.error(f"❌ {message}")
    
    def log_warning(self, message: str):
        self.logger.warning(f"⚠️ {message}")
    
    def save_data(self, data: Any, filepath: str) -> bool:
        """Saves data using the shared utility and the scraper's logger."""
        return save_json_data(data, filepath, self.logger)
    
    def save_with_history(self, data: Any, data_type: str, date: Optional[str] = None) -> Dict[str, bool]:
        """Saves daily data and updates history using the scraper's logger."""
        return manage_historical_data(data_type, data, date, self.logger)
    
    def validate_data(self, data: Any, expected_keys: List[str], min_records: int = 1) -> Dict[str, Any]:
        """Validates data using the shared utility."""
        return validate_data_structure(data, expected_keys, min_records)
    
    def get_runtime(self) -> str:
        """Returns the elapsed runtime of the scraper as a string."""
        return str(datetime.now() - self.start_time)
    
    def close_session(self):
        """Closes the HTTP session."""
        self.session.close()
        self.log_success("HTTP session closed.")

def main():
    """Provides a simple test run for the shared utilities."""
    print("🧪 Testing shared utilities...")
    logger = setup_logging("test-utility")
    
    logger.info("Testing data validation...")
    test_data = [{"symbol": "NABIL", "price": 1200}, {"symbol": "SCBL"}]
    validation = validate_data_structure(test_data, ["symbol", "price"])
    print(f"Validation result: {validation}")
    assert 'missing keys' in validation['warnings'][0]

    logger.info("Testing file path creation...")
    filepath = create_data_filepath("test_data")
    print(f"Created daily filepath: {filepath}")
    assert "daily" in filepath

    historical_path = create_historical_filepath("test_data")
    print(f"Created historical filepath: {historical_path}")
    assert "historical" in historical_path
    
    print("\n✅ All utilities tested successfully!")

if __name__ == "__main__":
    main()

