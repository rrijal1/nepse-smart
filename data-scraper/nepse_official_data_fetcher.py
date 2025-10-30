#!/usr/bin/env python3
"""
NEPSE Official API Data Fetcher
- Uses the NepseUnofficialApi library for authenticated NEPSE data access
- Integrated with the existing scraper architecture
- Fetches comprehensive market data from official NEPSE API endpoints
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Any

# Import the NepseUnofficialApi library
from nepse import Nepse
from shared_utils import ScraperBase, create_data_filepath


class NEPSEOfficialDataFetcher(ScraperBase):
    """
    Official NEPSE data fetcher using authenticated API access
    """
    
    def __init__(self):
        super().__init__("NEPSE-Official-API")
        
        # Initialize the Nepse client with SSL verification disabled
        self.nepse = Nepse()
        self.nepse.setTLSVerification(False)
        
        # Define core data methods for official API (high-value, authenticated data)
        self.core_methods = {
            "security_list": self.nepse.getSecurityList,
            "market_status": self.nepse.getMarketStatus,
            "floorsheet": self.nepse.getFloorSheet,
            "nepse_index": self.nepse.getNepseIndex,
            "nepse_subindices": self.nepse.getNepseSubIndices,
            "supply_demand": self.nepse.getSupplyDemand,
            "security_id_key_map": self.nepse.getSecurityIDKeyMap,
            "sector_scrips": self.nepse.getSectorScrips,
            # Historical price/volume data for ALL stocks
            "price_volume_history_today": lambda: self.nepse.getPriceVolumeHistory(datetime.now().strftime('%Y-%m-%d')),
        }
        
        # Remove comprehensive methods - keeping only core official data
        self.comprehensive_methods = {}
    
    def fetch_method_data(self, method_name: str, method_func, timeout: int = 30) -> Optional[Dict]:
        """Fetch data from a specific API method with error handling"""
        try:
            self.log_success(f"Fetching {method_name}...")
            start_time = time.time()
            
            data = method_func()
            
            fetch_time = time.time() - start_time
            
            if data:
                result = {
                    "method_name": method_name,
                    "data": data,
                    "timestamp": time.time(),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "fetch_time_seconds": round(fetch_time, 2),
                    "status": "success"
                }
                
                if isinstance(data, list):
                    result["record_count"] = len(data)
                    self.log_success(f"✅ {method_name}: {len(data)} records ({fetch_time:.1f}s)")
                else:
                    data_size = len(str(data))
                    result["data_size"] = data_size
                    self.log_success(f"✅ {method_name}: {data_size} chars ({fetch_time:.1f}s)")
                
                return result
            else:
                self.log_warning(f"⚪ {method_name}: No data returned")
                return {
                    "method_name": method_name,
                    "data": None,
                    "timestamp": time.time(),
                    "date": datetime.now().strftime("%Y-%m-%d"),
                    "fetch_time_seconds": round(fetch_time, 2),
                    "status": "empty"
                }
                
        except Exception as e:
            self.log_error(f"❌ {method_name} failed: {e}")
            return {
                "method_name": method_name,
                "data": None,
                "error": str(e),
                "timestamp": time.time(),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "status": "error"
            }
    

    
    def run_core_collection(self) -> Dict[str, Any]:
        """Run core data collection (company list + market status only)"""
        return self._run_collection(self.core_methods, include_floorsheet=False, collection_type="core")
    
    def run_comprehensive_collection(self) -> Dict[str, Any]:
        """Run comprehensive data collection (all available data)"""
        all_methods = {**self.core_methods, **self.comprehensive_methods}
        return self._run_collection(all_methods, include_floorsheet=False, collection_type="comprehensive")
    
    def run_historical_price_volume_collection(self, days_back: int = 30) -> Dict[str, Any]:
        """Run historical price/volume data collection for all stocks"""
        from datetime import datetime, timedelta
        
        results = {
            "scraper": "nepse_official_api",
            "collection_type": "historical_price_volume",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "successful_methods": [],
            "failed_methods": [],
            "empty_methods": [],
            "total_methods": 0,
            "success_count": 0,
            "failure_count": 0,
            "empty_count": 0,
            "total_records": 0,
            "total_fetch_time": 0,
            "days_back": days_back
        }
        
        self.log_success(f"Starting historical price/volume collection for last {days_back} days...")
        collection_start = time.time()
        
        # Generate business dates (skip weekends)
        business_dates = []
        current_date = datetime.now()
        
        for i in range(days_back + 1):
            check_date = current_date - timedelta(days=i)
            # Skip weekends (Saturday=5, Sunday=6)
            if check_date.weekday() < 5:
                business_dates.append(check_date.strftime('%Y-%m-%d'))
        
        results["total_methods"] = len(business_dates)
        
        # Fetch data for each business date
        for business_date in business_dates:
            method_name = f"price_volume_history_{business_date.replace('-', '_')}"
            
            try:
                self.log_success(f"Fetching price/volume data for {business_date}...")
                start_time = time.time()
                
                data = self.nepse.getPriceVolumeHistory(business_date)
                fetch_time = time.time() - start_time
                
                if data and isinstance(data, dict) and 'content' in data:
                    content = data['content']
                    if content:
                        result = {
                            "method_name": method_name,
                            "business_date": business_date,
                            "data": data,
                            "timestamp": time.time(),
                            "date": datetime.now().strftime("%Y-%m-%d"),
                            "fetch_time_seconds": round(fetch_time, 2),
                            "record_count": len(content),
                            "status": "success"
                        }
                        
                        results["successful_methods"].append(result)
                        results["success_count"] += 1
                        results["total_records"] += len(content)
                        results["total_fetch_time"] += fetch_time
                        
                        # Save individual date data
                        from pathlib import Path
                        import json
                        
                        date_str = datetime.now().strftime('%Y-%m-%d')
                        data_dir = Path(__file__).parent.parent / 'data' / 'daily'
                        data_dir.mkdir(parents=True, exist_ok=True)
                        
                        filename = data_dir / f"{date_str}_price_volume_history_{business_date.replace('-', '_')}.json"
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                        
                        self.logger.info(f"✅ {method_name}: {len(content)} stocks → {filename}")
                    else:
                        results["empty_methods"].append({
                            "method_name": method_name,
                            "business_date": business_date,
                            "status": "empty"
                        })
                        results["empty_count"] += 1
                else:
                    results["failed_methods"].append({
                        "method_name": method_name,
                        "business_date": business_date,
                        "error": "Invalid response format",
                        "status": "error"
                    })
                    results["failure_count"] += 1
                    
            except Exception as e:
                results["failed_methods"].append({
                    "method_name": method_name,
                    "business_date": business_date,
                    "error": str(e),
                    "status": "error"
                })
                results["failure_count"] += 1
            
            time.sleep(0.5)  # Brief pause between requests
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        return results
    
    def run_complete_historical_price_volume_collection(self) -> Dict[str, Any]:
        """Run complete historical price/volume data collection - go back as far as possible"""
        from datetime import datetime, timedelta
        
        results = {
            "scraper": "nepse_official_api",
            "collection_type": "complete_historical_price_volume",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "successful_methods": [],
            "failed_methods": [],
            "empty_methods": [],
            "total_methods": 0,
            "success_count": 0,
            "failure_count": 0,
            "empty_count": 0,
            "total_records": 0,
            "total_fetch_time": 0,
            "date_range": {}
        }
        
        self.log_success("Starting complete historical price/volume collection - downloading all available data...")
        collection_start = time.time()
        
        # Start from today and go back until we can't get data anymore
        business_dates = []
        current_date = datetime.now()
        consecutive_failures = 0
        max_consecutive_failures = 5  # Stop after 5 consecutive failures
        
        # Try up to 5 years back (roughly 1250 business days)
        max_days_back = 1250
        
        for i in range(max_days_back):
            check_date = current_date - timedelta(days=i)
            # Skip weekends (Saturday=5, Sunday=6)
            if check_date.weekday() < 5:
                business_date = check_date.strftime('%Y-%m-%d')
                business_dates.append(business_date)
                
                method_name = f"price_volume_history_{business_date.replace('-', '_')}"
                
                try:
                    self.log_success(f"Fetching price/volume data for {business_date}...")
                    start_time = time.time()
                    
                    data = self.nepse.getPriceVolumeHistory(business_date)
                    fetch_time = time.time() - start_time
                    
                    if data and isinstance(data, dict) and 'content' in data:
                        content = data['content']
                        if content:
                            result = {
                                "method_name": method_name,
                                "business_date": business_date,
                                "data": data,
                                "timestamp": time.time(),
                                "date": datetime.now().strftime("%Y-%m-%d"),
                                "fetch_time_seconds": round(fetch_time, 2),
                                "record_count": len(content),
                                "status": "success"
                            }
                            
                            results["successful_methods"].append(result)
                            results["success_count"] += 1
                            results["total_records"] += len(content)
                            results["total_fetch_time"] += fetch_time
                            consecutive_failures = 0  # Reset consecutive failures
                            
                            # Save individual date data
                            from pathlib import Path
                            import json
                            
                            date_str = datetime.now().strftime('%Y-%m-%d')
                            data_dir = Path(__file__).parent.parent / 'data' / 'historical'
                            data_dir.mkdir(parents=True, exist_ok=True)
                            
                            filename = data_dir / f"{date_str}_price_volume_history_{business_date.replace('-', '_')}.json"
                            with open(filename, 'w', encoding='utf-8') as f:
                                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                            
                            self.logger.info(f"✅ {method_name}: {len(content)} stocks → {filename}")
                        else:
                            results["empty_methods"].append({
                                "method_name": method_name,
                                "business_date": business_date,
                                "status": "empty"
                            })
                            results["empty_count"] += 1
                            consecutive_failures += 1
                    else:
                        results["failed_methods"].append({
                            "method_name": method_name,
                            "business_date": business_date,
                            "error": "Invalid response format",
                            "status": "error"
                        })
                        results["failure_count"] += 1
                        consecutive_failures += 1
                        
                except Exception as e:
                    results["failed_methods"].append({
                        "method_name": method_name,
                        "business_date": business_date,
                        "error": str(e),
                        "status": "error"
                    })
                    results["failure_count"] += 1
                    consecutive_failures += 1
                
                # Stop if we've had too many consecutive failures (likely reached the limit of available data)
                if consecutive_failures >= max_consecutive_failures:
                    self.log_success(f"Stopping collection after {consecutive_failures} consecutive failures - likely reached end of available data")
                    break
                
                time.sleep(0.5)  # Brief pause between requests
        
        results["total_methods"] = len(business_dates)
        
        # Set date range
        if results["successful_methods"]:
            successful_dates = [m["business_date"] for m in results["successful_methods"]]
            results["date_range"] = {
                "start_date": min(successful_dates),
                "end_date": max(successful_dates),
                "business_days": len(successful_dates)
            }
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        return results
    
    def run_complete_historical_company_data_collection(self) -> Dict[str, Any]:
        """Run complete historical data collection for all companies using individual company history"""
        from datetime import datetime
        
        results = {
            "scraper": "nepse_official_api",
            "collection_type": "complete_historical_company_data",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "successful_methods": [],
            "failed_methods": [],
            "empty_methods": [],
            "total_methods": 0,
            "success_count": 0,
            "failure_count": 0,
            "empty_count": 0,
            "total_records": 0,
            "total_fetch_time": 0,
            "companies_processed": []
        }
        
        self.log_success("Starting complete historical company data collection - downloading historical data for ALL companies...")
        collection_start = time.time()
        
        # First get the list of all companies
        try:
            self.log_success("Fetching company list...")
            companies_data = self.nepse.getSecurityList()
            
            if not companies_data:
                self.log_error("Failed to get company list")
                return results
            
            # getSecurityList returns a list directly
            if isinstance(companies_data, list):
                companies = companies_data
            elif isinstance(companies_data, dict) and 'content' in companies_data:
                companies = companies_data['content']
            else:
                self.log_error("Unexpected company list format")
                return results
                
            results["total_methods"] = len(companies)
            
            self.log_success(f"Found {len(companies)} companies to process")
            
        except Exception as e:
            self.log_error(f"Failed to get company list: {e}")
            return results
        
        # Process each company
        for i, company in enumerate(companies, 1):
            symbol = company.get('symbol', '')
            security_id = company.get('id', '')
            
            if not symbol:
                continue
                
            try:
                self.log_success(f"[{i}/{len(companies)}] Fetching historical data for {symbol}...")
                start_time = time.time()
                
                # Get historical data for this company
                data = self.nepse.getCompanyPriceVolumeHistory(symbol)
                fetch_time = time.time() - start_time
                
                if data and 'content' in data and data['content']:
                    content = data['content']
                    
                    result = {
                        "method_name": f"company_history_{symbol}",
                        "symbol": symbol,
                        "security_id": security_id,
                        "data": data,
                        "timestamp": time.time(),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "fetch_time_seconds": round(fetch_time, 2),
                        "record_count": len(content),
                        "status": "success"
                    }
                    
                    results["successful_methods"].append(result)
                    results["success_count"] += 1
                    results["total_records"] += len(content)
                    results["total_fetch_time"] += fetch_time
                    results["companies_processed"].append(symbol)
                    
                    # Save individual company data
                    from pathlib import Path
                    import json
                    
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    data_dir = Path(__file__).parent.parent / 'data' / 'historical' / 'companies'
                    data_dir.mkdir(parents=True, exist_ok=True)
                    
                    filename = data_dir / f"{date_str}_company_history_{symbol}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                    
                    self.logger.info(f"✅ {symbol}: {len(content)} historical records → {filename}")
                    
                else:
                    results["empty_methods"].append({
                        "method_name": f"company_history_{symbol}",
                        "symbol": symbol,
                        "status": "empty"
                    })
                    results["empty_count"] += 1
                    
            except Exception as e:
                results["failed_methods"].append({
                    "method_name": f"company_history_{symbol}",
                    "symbol": symbol,
                    "error": str(e),
                    "status": "error"
                })
                results["failure_count"] += 1
                self.log_error(f"Failed to get historical data for {symbol}: {e}")
            
            # Brief pause between requests
            time.sleep(0.2)
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        return results
    
    def aggregate_historical_price_volume_data(self, days_back: int = 30) -> Dict[str, Any]:
        """Aggregate historical price/volume data into a consolidated format for analysis"""
        from pathlib import Path
        from datetime import datetime, timedelta
        import json
        
        results = {
            "aggregation_date": datetime.now().strftime("%Y-%m-%d"),
            "days_back": days_back,
            "total_stocks": 0,
            "total_records": 0,
            "date_range": {},
            "stocks_data": {},
            "summary_stats": {}
        }
        
        self.log_success(f"Aggregating historical price/volume data for last {days_back} days...")
        
        # Generate business dates
        business_dates = []
        current_date = datetime.now()
        
        for i in range(days_back + 1):
            check_date = current_date - timedelta(days=i)
            if check_date.weekday() < 5:  # Skip weekends
                business_dates.append(check_date.strftime('%Y-%m-%d'))
        
        results["date_range"] = {
            "start_date": min(business_dates),
            "end_date": max(business_dates),
            "business_days": len(business_dates)
        }
        
        data_dir = Path(__file__).parent.parent / 'data' / 'daily'
        stocks_data = {}
        
        # Process each business date
        for business_date in business_dates:
            file_pattern = f"*_price_volume_history_{business_date.replace('-', '_')}.json"
            matching_files = list(data_dir.glob(file_pattern))
            
            if matching_files:
                file_path = matching_files[0]  # Should only be one
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    if isinstance(data, dict) and 'content' in data:
                        day_data = data['content']
                        
                        for stock_record in day_data:
                            symbol = stock_record['symbol']
                            
                            if symbol not in stocks_data:
                                stocks_data[symbol] = {
                                    "symbol": symbol,
                                    "security_name": stock_record.get('securityName', ''),
                                    "security_id": stock_record.get('securityId', ''),
                                    "historical_data": []
                                }
                            
                            # Add this day's data
                            stocks_data[symbol]["historical_data"].append({
                                "date": business_date,
                                "open": stock_record.get('openPrice'),
                                "high": stock_record.get('highPrice'),
                                "low": stock_record.get('lowPrice'),
                                "close": stock_record.get('closePrice'),
                                "volume": stock_record.get('totalTradedQuantity'),
                                "value": stock_record.get('totalTradedValue'),
                                "trades": stock_record.get('totalTrades'),
                                "prev_close": stock_record.get('previousDayClosePrice'),
                                "avg_price": stock_record.get('averageTradedPrice'),
                                "market_cap": stock_record.get('marketCapitalization'),
                                "52w_high": stock_record.get('fiftyTwoWeekHigh'),
                                "52w_low": stock_record.get('fiftyTwoWeekLow')
                            })
                        
                        results["total_records"] += len(day_data)
                        self.log_success(f"Processed {business_date}: {len(day_data)} stocks")
                        
                except Exception as e:
                    self.log_error(f"Failed to process {file_path}: {e}")
        
        results["stocks_data"] = stocks_data
        results["total_stocks"] = len(stocks_data)
        
        # Calculate summary statistics
        if stocks_data:
            total_volume = sum(
                sum(day_data.get('volume', 0) for day_data in stock['historical_data'])
                for stock in stocks_data.values()
            )
            total_value = sum(
                sum(day_data.get('value', 0) for day_data in stock['historical_data'])
                for stock in stocks_data.values()
            )
            
            results["summary_stats"] = {
                "total_volume": total_volume,
                "total_value": total_value,
                "avg_daily_volume": total_volume / len(business_dates) if business_dates else 0,
                "avg_daily_value": total_value / len(business_dates) if business_dates else 0,
                "most_active_stocks": sorted(
                    [(symbol, sum(d.get('volume', 0) for d in data['historical_data'])) 
                     for symbol, data in stocks_data.items()],
                    key=lambda x: x[1], 
                    reverse=True
                )[:10]
            }
        
        # Save aggregated data
        output_file = data_dir / f"{datetime.now().strftime('%Y-%m-%d')}_historical_price_volume_aggregated.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str, ensure_ascii=False)
        
        self.log_success(f"✅ Aggregated data saved: {output_file}")
        self.log_success(f"   Total stocks: {results['total_stocks']:,}")
        self.log_success(f"   Total records: {results['total_records']:,}")
        self.log_success(f"   Date range: {results['date_range']['start_date']} to {results['date_range']['end_date']}")
        
        return results
    
    def run_daily_company_data_update(self) -> Dict[str, Any]:
        """Update existing company historical files with latest trading day's data"""
        from datetime import datetime, timedelta
        from pathlib import Path
        import json
        
        results = {
            "scraper": "nepse_official_api",
            "collection_type": "daily_company_update",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "successful_updates": [],
            "failed_updates": [],
            "skipped_companies": [],
            "total_companies_processed": 0,
            "total_records_added": 0,
            "total_fetch_time": 0
        }
        
        self.log_success("Starting daily company data update - appending latest trading day to existing files...")
        collection_start = time.time()
        
        # Find the most recent trading day (yesterday, skipping weekends)
        current_date = datetime.now()
        yesterday = current_date - timedelta(days=1)
        
        # If yesterday was weekend, go back further
        while yesterday.weekday() >= 5:  # Saturday=5, Sunday=6
            yesterday -= timedelta(days=1)
        
        latest_trading_date = yesterday.strftime('%Y-%m-%d')
        results["latest_trading_date"] = latest_trading_date
        
        self.log_success(f"Target trading date: {latest_trading_date}")
        
        # Get list of existing company files
        companies_dir = Path(__file__).parent.parent / 'data' / 'historical' / 'companies'
        
        if not companies_dir.exists():
            self.log_error("Companies directory not found - run complete_company_historical first")
            return results
        
        company_files = list(companies_dir.glob("*_company_history_*.json"))
        
        if not company_files:
            self.log_error("No existing company files found - run complete_company_historical first")
            return results
        
        self.log_success(f"Found {len(company_files)} existing company files to update")
        
        # Process each company file
        for company_file in company_files:
            filename = company_file.name
            # Extract symbol from filename: YYYY-MM-DD_company_history_SYMBOL.json
            parts = filename.split('_company_history_')
            if len(parts) != 2:
                continue
                
            symbol = parts[1].replace('.json', '')
            results["total_companies_processed"] += 1
            
            try:
                # Read existing company data
                with open(company_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                
                if not isinstance(existing_data, dict) or 'content' not in existing_data:
                    self.log_warning(f"Invalid data format in {filename}, skipping")
                    results["skipped_companies"].append({
                        "symbol": symbol,
                        "reason": "invalid_data_format"
                    })
                    continue
                
                existing_records = existing_data['content']
                if not isinstance(existing_records, list):
                    self.log_warning(f"Invalid records format in {filename}, skipping")
                    results["skipped_companies"].append({
                        "symbol": symbol,
                        "reason": "invalid_records_format"
                    })
                    continue
                
                # Check if we already have data for the latest trading date
                existing_dates = {record.get('businessDate') for record in existing_records}
                
                if latest_trading_date in existing_dates:
                    self.log_success(f"✅ {symbol}: Already has data for {latest_trading_date}, skipping")
                    results["skipped_companies"].append({
                        "symbol": symbol,
                        "reason": "date_already_exists"
                    })
                    continue
                
                # Fetch latest day's data for this company
                self.log_success(f"Fetching latest day data for {symbol}...")
                start_time = time.time()
                
                latest_data = self.nepse.getCompanyPriceVolumeHistory(symbol)
                fetch_time = time.time() - start_time
                
                if latest_data and 'content' in latest_data and latest_data['content']:
                    latest_records = latest_data['content']
                    
                    # Find the record for the latest trading date
                    new_record = None
                    for record in latest_records:
                        if record.get('businessDate') == latest_trading_date:
                            new_record = record
                            break
                    
                    if new_record:
                        # Append the new record to existing data
                        existing_records.append(new_record)
                        
                        # Sort records by business date (newest first)
                        existing_records.sort(key=lambda x: x.get('businessDate', ''), reverse=True)
                        
                        # Update the file
                        with open(company_file, 'w', encoding='utf-8') as f:
                            json.dump(existing_data, f, ensure_ascii=False, indent=2, default=str)
                        
                        results["successful_updates"].append({
                            "symbol": symbol,
                            "date_added": latest_trading_date,
                            "fetch_time_seconds": round(fetch_time, 2),
                            "total_records_now": len(existing_records)
                        })
                        
                        results["total_records_added"] += 1
                        results["total_fetch_time"] += fetch_time
                        
                        self.log_success(f"✅ {symbol}: Added {latest_trading_date} data ({len(existing_records)} total records)")
                        
                    else:
                        self.log_warning(f"⚪ {symbol}: No data found for {latest_trading_date}")
                        results["skipped_companies"].append({
                            "symbol": symbol,
                            "reason": "no_data_for_date"
                        })
                        
                else:
                    results["failed_updates"].append({
                        "symbol": symbol,
                        "error": "failed_to_fetch_latest_data"
                    })
                    self.log_error(f"❌ {symbol}: Failed to fetch latest data")
                
            except Exception as e:
                results["failed_updates"].append({
                    "symbol": symbol,
                    "error": str(e)
                })
                self.log_error(f"❌ {symbol}: Update failed - {e}")
            
            # Brief pause between requests
            time.sleep(0.1)
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        
        # Summary
        successful = len(results["successful_updates"])
        failed = len(results["failed_updates"])
        skipped = len(results["skipped_companies"])
        total_processed = results["total_companies_processed"]
        
        self.log_success(f"Daily company update complete:")
        self.log_success(f"  ✅ Updated: {successful}")
        self.log_success(f"  ❌ Failed: {failed}")
        self.log_success(f"  ⏭️ Skipped: {skipped}")
        self.log_success(f"  📊 Records added: {results['total_records_added']}")
        self.log_success(f"  ⏱️ Total time: {results['total_collection_time']}s")
        
        return results
        """Internal method to run data collection"""
        total_methods = len(methods)
        
        results = {
            "scraper": "nepse_official_api",
            "collection_type": collection_type,
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "successful_methods": [],
            "failed_methods": [],
            "empty_methods": [],
            "total_methods": total_methods,
            "success_count": 0,
            "failure_count": 0,
            "empty_count": 0,
            "total_records": 0,
            "total_fetch_time": 0
        }
        
        self.log_success(f"Starting {collection_type} collection from {total_methods} methods...")
        collection_start = time.time()
        
        # Fetch data from all methods
        for method_name, method_func in methods.items():
            result = self.fetch_method_data(method_name, method_func)
            
            if result:
                if result["status"] == "success":
                    results["successful_methods"].append(result)
                    results["success_count"] += 1
                    results["total_fetch_time"] += result["fetch_time_seconds"]
                    
                    if "record_count" in result:
                        results["total_records"] += result["record_count"]
                    
                    # Save individual method data
                    from pathlib import Path
                    import json
                    
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    
                    # Use lookup directory for reference data
                    if method_name in ["security_id_key_map", "sector_scrips", "security_list"]:
                        data_dir = Path(__file__).parent.parent / 'data' / 'lookup'
                    else:
                        data_dir = Path(__file__).parent.parent / 'data' / 'daily'
                    
                    data_dir.mkdir(parents=True, exist_ok=True)
                    
                    filename = data_dir / f"{date_str}_{method_name}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(result["data"], f, ensure_ascii=False, indent=2, default=str)
                    
                    self.logger.info(f"✅ {method_name}: {len(result['data']) if isinstance(result['data'], list) else 1} records → {filename}")
                    
                elif result["status"] == "empty":
                    results["empty_methods"].append(result)
                    results["empty_count"] += 1
                else:
                    results["failed_methods"].append(result)
                    results["failure_count"] += 1
            
            time.sleep(0.5)  # Brief pause between requests
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        return results


def main():
    """Main execution function"""
    fetcher = NEPSEOfficialDataFetcher()
    
    try:
        # Run core collection by default (change to run_comprehensive_collection() if needed)
        results = fetcher.run_core_collection()
        
        print("\n" + "="*60)
        print("📊 NEPSE OFFICIAL API COLLECTION RESULTS")
        print("="*60)
        print(f"🔄 Collection Type: {results['collection_type'].title()}")
        print(f"📈 Total methods: {results['total_methods']}")
        print(f"✅ Successful: {results['success_count']}")
        print(f"❌ Failed: {results['failure_count']}")
        print(f"⚪ Empty: {results['empty_count']}")
        print(f"📊 Success rate: {(results['success_count']/results['total_methods']*100):.1f}%")
        print(f"📋 Total records: {results['total_records']:,}")
        print(f"⏱️ Total time: {results['total_collection_time']}s")
        
        if results['successful_methods']:
            print(f"\n🎯 SUCCESSFUL DATA FETCHES:")
            for method_result in results['successful_methods']:
                method_name = method_result['method_name']
                if 'record_count' in method_result:
                    print(f"  ✅ {method_name}: {method_result['record_count']:,} records")
                else:
                    data_size = method_result.get('data_size', 0)
                    print(f"  ✅ {method_name}: {data_size:,} chars")
        
        if results['failed_methods']:
            print(f"\n❌ FAILED METHODS:")
            for method_result in results['failed_methods']:
                error = method_result.get('error', 'Unknown error')
                print(f"  ❌ {method_result['method_name']}: {error}")
        
        # Collection complete - no summary file needed
        
    except Exception as e:
        print(f"❌ Collection failed: {e}")
    finally:
        fetcher.close_session()


if __name__ == "__main__":
    main()