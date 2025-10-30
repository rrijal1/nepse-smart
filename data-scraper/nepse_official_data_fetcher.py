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