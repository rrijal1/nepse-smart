#!/usr/bin/env python3
"""
NEPSE Data Service - PostgreSQL Primary with JSON Fallback
- Primary data source: PostgreSQL database
- Fallback: JSON files when database unavailable
- Provides comprehensive market data endpoints
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import logging

# Database imports
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import and_, desc, func, text
from backend.database import engine, get_db
from backend.models import HistoricalPriceVolume, Floorsheet, MarketIndex, ExchangeRate, BankingIndicator, ShortTermRate

class NepseDataService:
    """Service to load and serve NEPSE data from PostgreSQL with JSON fallback"""

    def __init__(self, data_path: str = "../data", use_database: bool = True):
        self.data_path = Path(data_path)
        self.daily_path = self.data_path / "daily"
        self.historical_path = self.data_path / "historical"
        self.logger = logging.getLogger(__name__)
        self.use_database = use_database

        # Cache for frequently accessed data
        self._cache = {}
        self._cache_timestamps = {}
        self._cache_duration = 300  # 5 minutes cache

        # Test database connection
        self.db_available = self._test_db_connection()
        if self.db_available:
            self.logger.info("✅ PostgreSQL database available")
        else:
            self.logger.warning("⚠️ PostgreSQL database not available, using JSON fallback")

    def _test_db_connection(self) -> bool:
        """Test if database connection is available"""
        if not self.use_database:
            return False

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            self.logger.error(f"Database connection failed: {e}")
            return False

    def _get_db_session(self) -> Session:
        """Get database session"""
        return next(get_db())

    # Database Query Methods

    def _get_latest_historical_prices(self, limit: Optional[int] = None) -> List[Dict]:
        """Get latest historical price data from database"""
        if not self.db_available:
            self.logger.warning("Database not available, no fallback data")
            return []

        try:
            session = self._get_db_session()
            query = session.query(HistoricalPriceVolume).order_by(
                desc(HistoricalPriceVolume.business_date),
                HistoricalPriceVolume.symbol
            )

            if limit:
                query = query.limit(limit)

            records = query.all()
            session.close()

            return [{
                "symbol": record.symbol,
                "date": record.business_date.isoformat(),
                "open": record.open_price,
                "high": record.high_price,
                "low": record.low_price,
                "close": record.close_price,
                "volume": record.total_traded_quantity,
                "amount": record.total_traded_value
            } for record in records]

        except Exception as e:
            self.logger.error(f"Database query failed for historical prices: {e}")
            return []

    def _get_latest_floorsheet(self, limit: Optional[int] = None) -> List[Dict]:
        """Get latest floorsheet data from database"""
        if not self.db_available:
            self.logger.warning("Database not available, no fallback data")
            return []

        try:
            session = self._get_db_session()
            query = session.query(Floorsheet).order_by(
                desc(Floorsheet.data_date),
                desc(Floorsheet.transaction_no)
            )

            if limit:
                query = query.limit(limit)

            records = query.all()
            session.close()

            return [{
                "transaction_no": record.transaction_no,
                "stock_symbol": record.stock_symbol,
                "buyer_broker": record.buyer_broker,
                "seller_broker": record.seller_broker,
                "quantity": record.quantity,
                "rate": record.rate,
                "amount": record.amount,
                "date": record.data_date.isoformat(),
                "source": record.source
            } for record in records]

        except Exception as e:
            self.logger.error(f"Database query failed for floorsheet: {e}")
            return []

    def _get_latest_indices(self) -> List[Dict]:
        """Get latest market indices from database"""
        if not self.db_available:
            self.logger.warning("Database not available, no fallback data")
            return []

        try:
            session = self._get_db_session()
            # Get the latest date first
            latest_date = session.query(func.max(MarketIndex.data_date)).scalar()

            if not latest_date:
                session.close()
                return []

            records = session.query(MarketIndex).filter(
                MarketIndex.data_date == latest_date
            ).order_by(MarketIndex.index_name).all()

            session.close()

            return [{
                "index_name": record.index_name,
                "open": record.open,
                "high": record.high,
                "low": record.low,
                "current_value": record.current_value,
                "change": record.change,
                "change_percent": record.change_percent,
                "turnover": record.turnover,
                "date": record.data_date.isoformat(),
                "source": record.source
            } for record in records]

        except Exception as e:
            self.logger.error(f"Database query failed for indices: {e}")
            return []

    def _get_macro_data_db(self) -> List[Dict]:
        """Get latest macro data from database"""
        if not self.db_available:
            self.logger.warning("Database not available, no fallback data")
            return []

        try:
            session = self._get_db_session()
            macro_data = []

            # Get latest exchange rates
            latest_fx_date = session.query(func.max(ExchangeRate.data_date)).scalar()
            if latest_fx_date:
                fx_records = session.query(ExchangeRate).filter(
                    ExchangeRate.data_date == latest_fx_date
                ).all()

                for record in fx_records:
                    macro_data.append({
                        "data_type": "exchange_rates",
                        "currency": record.currency,
                        "rates": [record.buy_rate, record.sell_rate],
                        "headers": ["Currency", "Buy", "Sell"],
                        "date": record.data_date.isoformat(),
                        "source": record.source
                    })

            # Get latest banking indicators
            latest_bi_date = session.query(func.max(BankingIndicator.data_date)).scalar()
            if latest_bi_date:
                bi_records = session.query(BankingIndicator).filter(
                    BankingIndicator.data_date == latest_bi_date
                ).all()

                for record in bi_records:
                    macro_data.append({
                        "data_type": "banking_indicators",
                        "indicator": record.indicator,
                        "current_value": record.current_value,
                        "previous_value": record.previous_value,
                        "date": record.data_date.isoformat(),
                        "source": record.source,
                        "unit": record.unit
                    })

            # Get latest short-term rates
            latest_str_date = session.query(func.max(ShortTermRate.data_date)).scalar()
            if latest_str_date:
                str_records = session.query(ShortTermRate).filter(
                    ShortTermRate.data_date == latest_str_date
                ).all()

                for record in str_records:
                    macro_data.append({
                        "data_type": "short_term_rates",
                        "maturity": record.maturity,
                        "rate": record.rate,
                        "date": record.data_date.isoformat(),
                        "source": record.source
                    })

            session.close()
            return macro_data

        except Exception as e:
            self.logger.error(f"Database query failed for macro data: {e}")
            return []
    
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
        
        # Since historical JSON files are removed, return None
        self.logger.warning(f"Historical JSON files removed, no fallback data for {data_type}")
        return None
    
    # Market Data Methods (compatible with existing backend)
    
    def get_market_summary(self) -> Dict[str, Any]:
        """Get market summary data"""
        cache_key = "market_summary"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest indices data
            indices_data = self._get_latest_indices()

            # Get latest price data (limit to recent trading day)
            prices_data = self._get_latest_historical_prices(limit=500)  # Get recent data

            if not indices_data or not prices_data:
                return {"error": "Market data not available"}

            # Find NEPSE Index
            nepse_index = next((idx for idx in indices_data if idx['index_name'] == 'NEPSE Index'), None)

            # Calculate market stats from recent price data
            # Group by symbol to get unique stocks
            unique_symbols = {}
            for stock in prices_data:
                symbol = stock.get('symbol')
                if symbol and symbol not in unique_symbols:
                    unique_symbols[symbol] = stock

            recent_stocks = list(unique_symbols.values())
            total_stocks = len(recent_stocks)

            # Calculate gainers/losers (comparing to previous close if available)
            gainers = 0
            losers = 0

            for stock in recent_stocks:
                # Simple logic: if close > open, consider gainer (this is approximate)
                if stock.get('close') and stock.get('open'):
                    if stock['close'] > stock['open']:
                        gainers += 1
                    elif stock['close'] < stock['open']:
                        losers += 1

            unchanged = total_stocks - gainers - losers

            result = {
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
                "data_source": "postgresql" if self.db_available else "json_fallback",
                "last_updated": datetime.now().isoformat()
            }

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting market summary: {e}")
            return {"error": f"Failed to get market summary: {str(e)}"}
    
    def get_top_gainers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top gaining stocks"""
        cache_key = f"top_gainers_{limit}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest price data
            prices_data = self._get_latest_historical_prices(limit=500)  # Get enough data to find top gainers

            if not prices_data:
                return []

            # Group by symbol to get unique stocks with latest data
            unique_symbols = {}
            for stock in prices_data:
                symbol = stock.get('symbol')
                if symbol and symbol not in unique_symbols:
                    unique_symbols[symbol] = stock

            recent_stocks = list(unique_symbols.values())

            # Calculate gainers based on percentage change
            gainers = []
            for stock in recent_stocks:
                close = stock.get('close')
                previous_close = stock.get('previous_close') or stock.get('open')
                if close and previous_close and previous_close > 0:
                    change_percent = ((close - previous_close) / previous_close) * 100
                    if change_percent > 0:  # Only positive changes
                        gainers.append({
                            "symbol": stock.get('symbol'),
                            "close": close,
                            "change": close - previous_close,
                            "change_percent": change_percent,
                            "volume": stock.get('volume', 0)
                        })

            # Sort by change percent descending and take top limit
            gainers.sort(key=lambda x: x['change_percent'], reverse=True)
            result = gainers[:limit]

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting top gainers: {e}")
            return []
    
    def get_top_losers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top losing stocks"""
        cache_key = f"top_losers_{limit}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest price data
            prices_data = self._get_latest_historical_prices(limit=500)  # Get enough data to find top losers

            if not prices_data:
                return []

            # Group by symbol to get unique stocks with latest data
            unique_symbols = {}
            for stock in prices_data:
                symbol = stock.get('symbol')
                if symbol and symbol not in unique_symbols:
                    unique_symbols[symbol] = stock

            recent_stocks = list(unique_symbols.values())

            # Calculate losers based on percentage change
            losers = []
            for stock in recent_stocks:
                close = stock.get('close')
                previous_close = stock.get('previous_close') or stock.get('open')
                if close and previous_close and previous_close > 0:
                    change_percent = ((close - previous_close) / previous_close) * 100
                    if change_percent < 0:  # Only negative changes
                        losers.append({
                            "symbol": stock.get('symbol'),
                            "close": close,
                            "change": close - previous_close,
                            "change_percent": change_percent,
                            "volume": stock.get('volume', 0)
                        })

            # Sort by change percent ascending (most negative first) and take top limit
            losers.sort(key=lambda x: x['change_percent'])
            result = losers[:limit]

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting top losers: {e}")
            return []
    
    def get_nepse_index(self) -> Dict[str, Any]:
        """Get NEPSE index data"""
        cache_key = "nepse_index"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest indices data
            indices_data = self._get_latest_indices()

            if not indices_data:
                return {"error": "Index data not available"}

            # Find main indices
            nepse_index = next((idx for idx in indices_data if idx['index_name'] == 'NEPSE Index'), None)
            sensitive_index = next((idx for idx in indices_data if idx['index_name'] == 'Sensitive Index'), None)
            float_index = next((idx for idx in indices_data if idx['index_name'] == 'Float Index'), None)

            result = {
                "nepse_index": nepse_index,
                "sensitive_index": sensitive_index,
                "float_index": float_index,
                "data_source": "postgresql" if self.db_available else "json_fallback",
                "last_updated": datetime.now().isoformat()
            }

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting NEPSE index: {e}")
            return {"error": f"Failed to get NEPSE index: {str(e)}"}
    
    def get_sub_indices(self) -> List[Dict[str, Any]]:
        """Get sub-indices data"""
        cache_key = "sub_indices"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest indices data
            indices_data = self._get_latest_indices()

            if not indices_data:
                return []

            # Filter sub-indices (those with 'source': 'sharesansar_subindex')
            sub_indices = [
                idx for idx in indices_data
                if idx.get('source') == 'sharesansar_subindex'
            ]

            self._cache[cache_key] = sub_indices
            self._cache_timestamps[cache_key] = datetime.now()
            return sub_indices

        except Exception as e:
            self.logger.error(f"Error getting sub-indices: {e}")
            return []
    
    def get_price_volume(self) -> List[Dict[str, Any]]:
        """Get price volume data for all stocks"""
        cache_key = "price_volume"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest price data
            prices_data = self._get_latest_historical_prices(limit=1000)  # Get all recent data

            if not prices_data:
                return []

            # Group by symbol to get unique stocks with latest data
            unique_symbols = {}
            for stock in prices_data:
                symbol = stock.get('symbol')
                if symbol and symbol not in unique_symbols:
                    unique_symbols[symbol] = stock

            result = list(unique_symbols.values())

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting price volume: {e}")
            return []
    
    def get_company_list(self) -> List[Dict[str, Any]]:
        """Get list of all companies from price data"""
        cache_key = "company_list"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest price data
            prices_data = self._get_latest_historical_prices(limit=1000)  # Get all recent data

            if not prices_data:
                return []

            # Group by symbol to get unique stocks with latest data
            unique_symbols = {}
            for stock in prices_data:
                symbol = stock.get('symbol')
                if symbol and symbol not in unique_symbols:
                    unique_symbols[symbol] = stock

            recent_stocks = list(unique_symbols.values())

            # Extract unique companies
            companies = []
            for stock in recent_stocks:
                if stock.get('symbol'):
                    close = stock.get('close')
                    previous_close = stock.get('previous_close') or stock.get('open')
                    change = close - previous_close if close and previous_close else 0
                    change_percent = ((change / previous_close) * 100) if previous_close and previous_close > 0 else 0

                    companies.append({
                        "symbol": stock['symbol'],
                        "name": stock.get('company_name', stock['symbol']),  # Fallback to symbol if no name
                        "ltp": close,
                        "change": change,
                        "change_percent": change_percent
                    })

            result = companies

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting company list: {e}")
            return []
    
    def get_macro_data(self) -> Dict[str, Any]:
        """Get macro economic data"""
        cache_key = "macro_data"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Get latest macro data from database
            macro_data = self._get_macro_data_db()

            if not macro_data:
                return {"error": "Macro data not available"}

            # Organize by data type
            forex_rates = [item for item in macro_data if item.get('data_type') == 'exchange_rates']
            banking_indicators = [item for item in macro_data if item.get('data_type') == 'banking_indicators']
            short_term_rates = [item for item in macro_data if item.get('data_type') == 'short_term_rates']

            result = {
                "forex_rates": forex_rates,
                "banking_indicators": banking_indicators,
                "short_term_rates": short_term_rates,
                "data_source": "postgresql" if self.db_available else "json_fallback",
                "last_updated": datetime.now().isoformat()
            }

            self._cache[cache_key] = result
            self._cache_timestamps[cache_key] = datetime.now()
            return result

        except Exception as e:
            self.logger.error(f"Error getting macro data: {e}")
            return {"error": f"Failed to get macro data: {str(e)}"}
    
    def get_company_price_history(self, symbol: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get price history for a specific company"""
        cache_key = f"company_history_{symbol}_{days}"
        if self._is_cache_valid(cache_key):
            return self._cache[cache_key]

        try:
            # Try database first
            if self.db_available:
                session = self._get_db_session()
                if session:
                    try:
                        # Calculate date range
                        end_date = datetime.now().date()
                        start_date = end_date - timedelta(days=days)

                        # Query historical prices for specific symbol
                        records = session.query(HistoricalPriceVolume).filter(
                            HistoricalPriceVolume.symbol == symbol.upper(),
                            HistoricalPriceVolume.business_date >= start_date,
                            HistoricalPriceVolume.business_date <= end_date
                        ).order_by(HistoricalPriceVolume.business_date.asc()).all()

                        company_data = []
                        for record in records:
                            company_data.append({
                                "symbol": record.symbol,
                                "date": record.business_date.isoformat(),
                                "open": record.open_price,
                                "high": record.high_price,
                                "low": record.low_price,
                                "close": record.close_price,
                                "volume": record.total_traded_quantity,
                                "amount": record.total_traded_value,
                                "previous_close": None,  # Not available in this table
                                "diff": None,  # Not available in this table
                                "diff_percent": None  # Not available in this table
                            })

                        session.close()

                        if company_data:
                            self._cache[cache_key] = company_data
                            self._cache_timestamps[cache_key] = datetime.now()
                            return company_data

                    except Exception as e:
                        self.logger.error(f"Database query failed for company history: {e}")
                        session.close()

            # Fallback to JSON historical data
            historical_prices = self.get_historical_data('prices', days)

            if not historical_prices:
                return []

            # Filter for specific symbol
            company_data = [
                record for record in historical_prices
                if record.get('symbol') == symbol.upper()
            ]

            # Sort by date (ascending - oldest first)
            company_data.sort(key=lambda x: x.get('date', ''))

            self._cache[cache_key] = company_data
            self._cache_timestamps[cache_key] = datetime.now()
            return company_data

        except Exception as e:
            self.logger.error(f"Error getting company price history: {e}")
            return []
    
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
            "database_available": self.db_available,
            "data_sources": {},
            "last_updated": datetime.now().isoformat()
        }

        # Check database tables if available
        if self.db_available:
            try:
                session = self._get_db_session()
                if session:
                    # Check each table for latest data
                    try:
                        # Historical prices
                        latest_price_date = session.query(func.max(HistoricalPriceVolume.business_date)).scalar()
                        price_count = session.query(func.count(HistoricalPriceVolume.id)).scalar()
                        status["data_sources"]["prices"] = {
                            "available": True,
                            "source": "postgresql",
                            "last_update": latest_price_date.isoformat() if latest_price_date else None,
                            "record_count": price_count
                        }
                    except:
                        status["data_sources"]["prices"] = {"available": False, "source": "postgresql", "error": "Query failed"}

                    try:
                        # Indices
                        latest_index_date = session.query(func.max(MarketIndex.data_date)).scalar()
                        index_count = session.query(func.count(MarketIndex.id)).scalar()
                        status["data_sources"]["indices"] = {
                            "available": True,
                            "source": "postgresql",
                            "last_update": latest_index_date.isoformat() if latest_index_date else None,
                            "record_count": index_count
                        }
                    except:
                        status["data_sources"]["indices"] = {"available": False, "source": "postgresql", "error": "Query failed"}

                    try:
                        # Macro data
                        latest_macro_date = session.query(func.max(ExchangeRate.data_date)).scalar()
                        macro_count = session.query(func.count(ExchangeRate.id)).scalar()
                        status["data_sources"]["macro"] = {
                            "available": True,
                            "source": "postgresql",
                            "last_update": latest_macro_date.isoformat() if latest_macro_date else None,
                            "record_count": macro_count
                        }
                    except:
                        status["data_sources"]["macro"] = {"available": False, "source": "postgresql", "error": "Query failed"}

                    try:
                        # Floorsheet
                        latest_floorsheet_date = session.query(func.max(Floorsheet.data_date)).scalar()
                        floorsheet_count = session.query(func.count(Floorsheet.id)).scalar()
                        status["data_sources"]["floorsheet"] = {
                            "available": True,
                            "source": "postgresql",
                            "last_update": latest_floorsheet_date.isoformat() if latest_floorsheet_date else None,
                            "record_count": floorsheet_count
                        }
                    except:
                        status["data_sources"]["floorsheet"] = {"available": False, "source": "postgresql", "error": "Query failed"}

                    session.close()
            except Exception as e:
                self.logger.error(f"Database status check failed: {e}")
                status["database_available"] = False

        # Fallback to file-based status check
        data_types = ['prices', 'indices', 'macro', 'floorsheet']
        for data_type in data_types:
            if data_type not in status["data_sources"]:
                latest_file = self._get_latest_daily_file(data_type)
                if latest_file:
                    # Extract date from filename
                    try:
                        date_str = latest_file.name.split('_')[0]
                        status["data_sources"][data_type] = {
                            "available": True,
                            "source": "json_fallback",
                            "last_update": date_str,
                            "file_size": latest_file.stat().st_size
                        }
                    except:
                        status["data_sources"][data_type] = {
                            "available": True,
                            "source": "json_fallback",
                            "last_update": "unknown"
                        }
                else:
                    status["data_sources"][data_type] = {
                        "available": False,
                        "source": "json_fallback",
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