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
from typing import Dict, List, Optional, Any, Callable

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
        
        # Configure HTTP client with longer timeout and HTTP/1.1 for stability
        # HTTP/2 connections can be unstable for long-running requests
        import httpx
        self.nepse.client = httpx.Client(
            verify=False,
            http2=False,  # Disable HTTP/2 to avoid connection state issues
            timeout=300.0,  # 5 minute timeout for long-running requests
            follow_redirects=True
        )
        
        # Define core data methods for official API (high-value, authenticated data)
        self.core_methods = {
            "security_list": self.nepse.getSecurityList,
            "market_status": self.nepse.getMarketStatus,
            "floorsheet": lambda: self.fetch_floorsheet_with_retry(),
            "nepse_index": self.nepse.getNepseIndex,
            "nepse_subindices": self.nepse.getNepseSubIndices,
            "supply_demand": self.nepse.getSupplyDemand,
            "security_id_key_map": self.nepse.getSecurityIDKeyMap,
            "sector_scrips": self.nepse.getSectorScrips,
            # Historical price/volume data for ALL stocks
            "price_volume_history_today": lambda: self.fetch_price_volume_with_retry(),
        }
        
        # Remove comprehensive methods - keeping only core official data
        self.comprehensive_methods = {}
    
    def fetch_floorsheet_with_retry(self, max_retries: int = 3) -> List:
        """Fetch floorsheet with retry logic and error handling
        
        The getFloorSheet() method can fail due to API response format changes.
        This wrapper provides proper error handling and retry logic.
        """
        for attempt in range(max_retries):
            try:
                self.log_success(f"Fetching floorsheet (attempt {attempt + 1}/{max_retries})...")
                # getFloorSheet() returns a list directly, not a dict
                floorsheet = self.nepse.getFloorSheet(show_progress=False)
                
                # Validate that we got a list
                if not isinstance(floorsheet, list):
                    raise ValueError(f"Expected list, got {type(floorsheet)}")
                
                self.log_success(f"✅ Floorsheet fetched: {len(floorsheet)} records")
                return floorsheet
                
            except Exception as e:
                self.log_error(f"❌ Floorsheet fetch attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 2  # Exponential backoff: 2s, 4s, 6s
                    self.log_warning(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    self.log_error(f"❌ All {max_retries} floorsheet fetch attempts failed")
                    raise
    
    def fetch_price_volume_with_retry(self, max_retries: int = 3) -> Dict:
        """Fetch price/volume history with retry logic and timeout handling
        
        The getPriceVolumeHistory() method can timeout for long requests.
        This wrapper provides retry logic and better error handling.
        """
        for attempt in range(max_retries):
            try:
                today = datetime.now().strftime('%Y-%m-%d')
                self.log_success(f"Fetching price/volume history for {today} (attempt {attempt + 1}/{max_retries})...")
                
                # getPriceVolumeHistory returns a dict with pagination info
                price_volume = self.nepse.getPriceVolumeHistory(today)
                
                # Validate response
                if not isinstance(price_volume, dict):
                    raise ValueError(f"Expected dict, got {type(price_volume)}")
                
                # Extract content if available
                if 'content' in price_volume:
                    records = price_volume['content']
                    self.log_success(f"✅ Price/volume history fetched: {len(records)} records")
                else:
                    self.log_warning(f"⚠️ Price/volume response has no 'content' key, returning full response")
                
                return price_volume
                
            except Exception as e:
                error_msg = str(e)
                self.log_error(f"❌ Price/volume fetch attempt {attempt + 1} failed: {error_msg}")
                
                # Check if it's a timeout/connection error
                if "timeout" in error_msg.lower() or "connection" in error_msg.lower():
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 5  # Longer backoff for timeouts: 5s, 10s, 15s
                        self.log_warning(f"Connection issue detected, retrying in {wait_time}s...")
                        time.sleep(wait_time)
                        
                        # Reinitialize the Nepse client to reset connection
                        self.log_success("Reinitializing Nepse client...")
                        self.nepse = Nepse()
                        self.nepse.setTLSVerification(False)
                    else:
                        self.log_error(f"❌ All {max_retries} price/volume fetch attempts failed")
                        raise
                else:
                    # Non-connection errors, fail fast
                    raise
    
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
        """Run historical price/volume data collection for all stocks
        
        ⚠️ DEPRECATED: Historical data scraping is disabled. 
        Data is now sourced from PostgreSQL database.
        """
        self.logger.warning("⚠️ Historical data scraping is disabled. Data is now sourced from PostgreSQL database.")
        return {
            "scraper": "nepse_official_api",
            "collection_type": "historical_price_volume",
            "status": "disabled",
            "message": "Historical data scraping is disabled. Data is now sourced from PostgreSQL database.",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def run_complete_historical_price_volume_collection(self) -> Dict[str, Any]:
        """Run complete historical price/volume data collection - go back as far as possible
        
        ⚠️ DEPRECATED: Historical data scraping is disabled. 
        Data is now sourced from PostgreSQL database.
        """
        self.logger.warning("⚠️ Historical data scraping is disabled. Data is now sourced from PostgreSQL database.")
        return {
            "scraper": "nepse_official_api",
            "collection_type": "complete_historical_price_volume",
            "status": "disabled",
            "message": "Historical data scraping is disabled. Data is now sourced from PostgreSQL database.",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def run_complete_historical_company_data_collection(self) -> Dict[str, Any]:
        """Run complete historical data collection for all companies using individual company history
        
        ⚠️ DEPRECATED: Historical data scraping is disabled. 
        Data is now sourced from PostgreSQL database.
        """
        self.logger.warning("⚠️ Historical data scraping is disabled. Data is now sourced from PostgreSQL database.")
        return {
            "scraper": "nepse_official_api",
            "collection_type": "complete_historical_company_data",
            "status": "disabled",
            "message": "Historical data scraping is disabled. Data is now sourced from PostgreSQL database.",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
    
    def aggregate_historical_price_volume_data(self, days_back: int = 30) -> Dict[str, Any]:
        """Aggregate historical price/volume data into a consolidated format for analysis
        
        ⚠️ DEPRECATED: Historical data scraping is disabled. 
        Data is now sourced from PostgreSQL database.
        """
        self.logger.warning("⚠️ Historical data scraping is disabled. Data is now sourced from PostgreSQL database.")
        return {
            "aggregation_date": datetime.now().strftime("%Y-%m-%d"),
            "days_back": days_back,
            "status": "disabled",
            "message": "Historical data scraping is disabled. Data is now sourced from PostgreSQL database.",
            "timestamp": time.time()
        }
    
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
    def _run_collection(self, methods: Dict[str, Callable], include_floorsheet: bool = True, collection_type: str = "core") -> Dict[str, Any]:
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