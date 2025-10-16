#!/usr/bin/env python3
"""
NEPSE Data Service
- Serves data from our scraped historical data files
- Replaces unofficial NEPSE API dependency
- Provides comprehensive market data endpoints
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

class NepseDataService:
    """Service to load and serve scraped NEPSE data"""
    
    def __init__(self, data_path: str = "../data"):
        self.data_path = Path(data_path)
        self.daily_path = self.data_path / "daily"
        self.historical_path = self.data_path / "historical"
        self.logger = logging.getLogger(__name__)
        
        # Cache for frequently accessed data
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_duration = 300  # 5 minutes cache
    
    def _get_cache_key(self, data_type: str, date: Optional[str] = None) -> str:
        """Generate cache key"""
        if date:
            return f"{data_type}_{date}"
        return f"{data_type}_latest"
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cache is still valid"""
        if cache_key not in self._cache_timestamps:
            return False
        
        cache_time = self._cache_timestamps[cache_key]
        return (datetime.now() - cache_time).seconds < self._cache_duration
    
    def _load_json_file(self, filepath: Path) -> Optional[List[Dict]]:
        """Load JSON data from file with error handling"""
        try:
            if not filepath.exists():
                self.logger.warning(f"File not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.logger.info(f"Loaded {len(data) if isinstance(data, list) else 1} records from {filepath}")
            return data
            
        except Exception as e:
            self.logger.error(f"Failed to load {filepath}: {e}")
            return None
    
    def _get_latest_daily_file(self, data_type: str) -> Optional[Path]:
        """Get the most recent daily file for a data type"""
        pattern = f"*_{data_type}.json"
        files = list(self.daily_path.glob(pattern))
        
        if not files:
            return None
        
        # Sort by date in filename (most recent first)
        files.sort(key=lambda x: x.name, reverse=True)
        return files[0]
    
    def get_daily_data(self, data_type: str, date: Optional[str] = None) -> Optional[List[Dict]]:
        """Get daily data for specific type and date"""
        cache_key = self._get_cache_key(data_type, date)
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        if date:
            # Specific date requested
            filepath = self.daily_path / f"{date}_{data_type}.json"
        else:
            # Get latest available data
            filepath = self._get_latest_daily_file(data_type)
            if not filepath:
                return None
        
        data = self._load_json_file(filepath)
        
        # Cache the result
        if data is not None:
            self._cache[cache_key] = data
            self._cache_timestamps[cache_key] = datetime.now()
        
        return data
    
    def get_historical_data(self, data_type: str, days: int = 30) -> Optional[List[Dict]]:
        """Get historical data for specified number of days"""
        cache_key = f"historical_{data_type}_{days}"
        
        # Check cache first
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]
        
        filepath = self.historical_path / f"historical_{data_type}.json"
        all_data = self._load_json_file(filepath)
        
        if not all_data:
            return None
        
        # Filter to recent days if requested
        if days > 0:
            cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            filtered_data = [
                record for record in all_data 
                if isinstance(record, dict) and record.get('date', '') >= cutoff_date
            ]
        else:
            filtered_data = all_data
        
        # Cache the result
        self._cache[cache_key] = filtered_data
        self._cache_timestamps[cache_key] = datetime.now()
        
        return filtered_data
    
    # Market Data Methods (compatible with existing backend)
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary data"""
        indices_data = self.get_daily_data('indices')
        prices_data = self.get_daily_data('prices')
        
        if not indices_data or not prices_data:
            return {"error": "Market data not available"}
        
        # Find NEPSE Index
        nepse_index = next((idx for idx in indices_data if idx['index_name'] == 'NEPSE Index'), None)
        
        # Calculate market stats
        total_stocks = len(prices_data)
        gainers = len([stock for stock in prices_data if stock.get('diff', 0) > 0])
        losers = len([stock for stock in prices_data if stock.get('diff', 0) < 0])
        unchanged = total_stocks - gainers - losers
        
        return {
            "nepse_index": {
                "value": nepse_index['current_value'] if nepse_index else 0,
                "change": nepse_index['change'] if nepse_index else 0,
                "change_percent": nepse_index['change_percent'] if nepse_index else 0,
            },
            "market_stats": {
                "total_stocks": total_stocks,
                "gainers": gainers,
                "losers": losers,
                "unchanged": unchanged
            },
            "last_updated": datetime.now().isoformat()
        }
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict]:
        """Get top gaining stocks"""
        prices_data = self.get_daily_data('prices')
        
        if not prices_data:
            return []
        
        # Filter and sort by percentage gain
        gainers = [
            stock for stock in prices_data 
            if stock.get('diff_percent', 0) > 0 and stock.get('symbol')
        ]
        
        # Sort by diff_percent descending
        gainers.sort(key=lambda x: x.get('diff_percent', 0), reverse=True)
        
        return gainers[:limit]
    
    def get_top_losers(self, limit: int = 10) -> List[Dict]:
        """Get top losing stocks"""
        prices_data = self.get_daily_data('prices')
        
        if not prices_data:
            return []
        
        # Filter and sort by percentage loss
        losers = [
            stock for stock in prices_data 
            if stock.get('diff_percent', 0) < 0 and stock.get('symbol')
        ]
        
        # Sort by diff_percent ascending (most negative first)
        losers.sort(key=lambda x: x.get('diff_percent', 0))
        
        return losers[:limit]
    
    def get_nepse_index(self) -> Dict[str, Any]:
        """Get NEPSE index data"""
        indices_data = self.get_daily_data('indices')
        
        if not indices_data:
            return {"error": "Index data not available"}
        
        # Find main indices
        nepse_index = next((idx for idx in indices_data if idx['index_name'] == 'NEPSE Index'), None)
        sensitive_index = next((idx for idx in indices_data if idx['index_name'] == 'Sensitive Index'), None)
        float_index = next((idx for idx in indices_data if idx['index_name'] == 'Float Index'), None)
        
        return {
            "nepse_index": nepse_index,
            "sensitive_index": sensitive_index,
            "float_index": float_index,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_sub_indices(self) -> List[Dict]:
        """Get sub-indices data"""
        indices_data = self.get_daily_data('indices')
        
        if not indices_data:
            return []
        
        # Filter sub-indices (those with 'source': 'sharesansar_subindex')
        sub_indices = [
            idx for idx in indices_data 
            if idx.get('source') == 'sharesansar_subindex'
        ]
        
        return sub_indices
    
    def get_price_volume(self) -> List[Dict]:
        """Get price volume data for all stocks"""
        return self.get_daily_data('prices') or []
    
    def get_company_list(self) -> List[Dict]:
        """Get list of all companies from price data"""
        prices_data = self.get_daily_data('prices')
        
        if not prices_data:
            return []
        
        # Extract unique companies
        companies = []
        for stock in prices_data:
            if stock.get('symbol'):
                companies.append({
                    "symbol": stock['symbol'],
                    "name": stock.get('company_name', stock['symbol']),  # Fallback to symbol if no name
                    "ltp": stock.get('ltp'),
                    "change": stock.get('diff'),
                    "change_percent": stock.get('diff_percent')
                })
        
        return companies
    
    def get_macro_data(self) -> Dict[str, Any]:
        """Get macro economic data"""
        macro_data = self.get_daily_data('macro')
        
        if not macro_data:
            return {"error": "Macro data not available"}
        
        # Organize by data type
        forex_rates = [item for item in macro_data if item.get('data_type') == 'exchange_rates']
        banking_indicators = [item for item in macro_data if item.get('data_type') == 'banking_indicators']
        short_term_rates = [item for item in macro_data if item.get('data_type') == 'short_term_rates']
        
        return {
            "forex_rates": forex_rates,
            "banking_indicators": banking_indicators,
            "short_term_rates": short_term_rates,
            "last_updated": datetime.now().isoformat()
        }
    
    def get_company_price_history(self, symbol: str, days: int = 30) -> List[Dict]:
        """Get price history for a specific company"""
        historical_prices = self.get_historical_data('prices', days)
        
        if not historical_prices:
            return []
        
        # Filter for specific symbol
        company_data = [
            record for record in historical_prices 
            if record.get('symbol') == symbol.upper()
        ]
        
        # Sort by date
        company_data.sort(key=lambda x: x.get('date', ''), reverse=True)
        
        return company_data
    
    def is_market_open(self) -> bool:
        """Check if market is open (basic implementation)"""
        # Simple time-based check - market is open 11 AM to 3 PM Nepal time (Sunday-Thursday)
        now = datetime.now()
        
        # Check if it's a weekday (Sunday = 6, Monday = 0 in Python)
        # Nepal: Sunday-Thursday are trading days
        nepal_weekday = (now.weekday() + 1) % 7  # Convert to Nepal weekday system
        if nepal_weekday > 4:  # Friday-Saturday
            return False
        
        # Check trading hours (rough approximation)
        hour = now.hour
        if 11 <= hour < 15:  # 11 AM to 3 PM
            return True
        
        return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get system status and data freshness"""
        status = {
            "system_status": "operational",
            "data_sources": {},
            "last_updated": datetime.now().isoformat()
        }
        
        # Check each data type
        data_types = ['prices', 'indices', 'macro', 'floorsheet']
        
        for data_type in data_types:
            latest_file = self._get_latest_daily_file(data_type)
            if latest_file:
                # Extract date from filename
                try:
                    date_str = latest_file.name.split('_')[0]
                    status["data_sources"][data_type] = {
                        "available": True,
                        "last_update": date_str,
                        "file_size": latest_file.stat().st_size
                    }
                except:
                    status["data_sources"][data_type] = {
                        "available": True,
                        "last_update": "unknown"
                    }
            else:
                status["data_sources"][data_type] = {
                    "available": False,
                    "last_update": None
                }
        
        return status

def main():
    """Test the data service"""
    print("🧪 Testing NEPSE Data Service...")
    
    service = NepseDataService()
    
    # Test market summary
    print("\n📊 Market Summary:")
    summary = service.get_market_summary()
    print(json.dumps(summary, indent=2, default=str))
    
    # Test top gainers
    print(f"\n📈 Top 5 Gainers:")
    gainers = service.get_top_gainers(5)
    for stock in gainers:
        print(f"  {stock['symbol']}: {stock.get('diff_percent', 0):.2f}%")
    
    # Test top losers
    print(f"\n📉 Top 5 Losers:")
    losers = service.get_top_losers(5)
    for stock in losers:
        print(f"  {stock['symbol']}: {stock.get('diff_percent', 0):.2f}%")
    
    # Test indices
    print(f"\n📊 NEPSE Index:")
    index_data = service.get_nepse_index()
    if 'nepse_index' in index_data and index_data['nepse_index']:
        nepse = index_data['nepse_index']
        print(f"  Value: {nepse['current_value']}")
        print(f"  Change: {nepse['change']} ({nepse['change_percent']:.2f}%)")
    
    # Test system status
    print(f"\n🔧 System Status:")
    status = service.get_system_status()
    for data_type, info in status["data_sources"].items():
        print(f"  {data_type}: {'✅' if info['available'] else '❌'} (Last: {info.get('last_update', 'N/A')})")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    main()