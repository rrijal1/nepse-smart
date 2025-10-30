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
            "company_list": self.nepse.getCompanyList,
            "market_status": self.nepse.getMarketStatus,
            "floorsheet": self.nepse.getFloorSheet,
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
    
    def _run_collection(self, methods: Dict, include_floorsheet: bool = False, collection_type: str = "core") -> Dict[str, Any]:
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