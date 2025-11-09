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
from typing import Dict, List, Optional, Any, Callable, NoReturn

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
        
        # Log floorsheet timing requirement
        self.log_success("✅ Floorsheet collection ENABLED: Available during trading hours (until midnight Nepal time)")
        self.log_success("✅ Using comprehensive transaction data: floorsheet + top traded/turnover/transaction scrips + live market data")
        
        # Define core data methods for official API (high-value, authenticated data)
        self.core_methods = {
            "security_list": self.nepse.getSecurityList,
            "market_status": self.nepse.getMarketStatus,
            "floorsheet": lambda: self.fetch_floorsheet_with_retry(),  # RE-ENABLED: Available during trading hours until midnight Nepal time
            "top_traded_scrips": self.nepse.getTopTenTradeScrips,        # Additional transaction data
            "top_transaction_scrips": self.nepse.getTopTenTransactionScrips,  # Additional transaction data
            "top_turnover_scrips": self.nepse.getTopTenTurnoverScrips,   # Additional transaction data
            "live_market": self.nepse.getLiveMarket,                    # Live market data
            "nepse_index": self.nepse.getNepseIndex,
            "nepse_subindices": self.nepse.getNepseSubIndices,
            "supply_demand": self.nepse.getSupplyDemand,
            "security_id_key_map": self.nepse.getSecurityIDKeyMap,
            "sector_scrips": self.nepse.getSectorScrips,
            # Historical price/volume data for ALL stocks
            "price_volume_history_today": lambda: self.fetch_price_volume_with_retry(),
        }
    
    def fetch_floorsheet_with_retry(self, max_retries: int = 1) -> List[Dict[str, Any]]:
        """Fetch floorsheet with retry logic and error handling

        The getFloorSheet() method returns data during trading hours until midnight Nepal time
        on trading days (Sun-Thu, excluding holidays). Returns empty list after midnight or on holidays.

        Returns:
            List of floorsheet records (dicts) - empty if called after midnight or on holidays

        Raises:
            Exception: If all retry attempts fail
        """
        for attempt in range(max_retries):
            try:
                self.log_success(f"Fetching floorsheet (attempt {attempt + 1}/{max_retries}) - available during trading hours until midnight Nepal time...")

                # Get floorsheet data
                floorsheet = self.nepse.getFloorSheet(show_progress=False)

                # Validate that we got a list
                if not isinstance(floorsheet, list):
                    raise ValueError(f"Expected list, got {type(floorsheet)}")

                if len(floorsheet) == 0:
                    self.log_warning("⚠️ Floorsheet returned empty list - normal after midnight or on holidays")
                    return floorsheet  # Return empty list
                else:
                    self.log_success(f"✅ Floorsheet fetched: {len(floorsheet)} records")
                    return floorsheet

            except Exception as e:
                error_msg = str(e)
                self.log_error(f"❌ Floorsheet fetch attempt {attempt + 1} failed: {error_msg}")

                # If it's the last attempt, return empty (could be holiday/festival)
                if attempt == max_retries - 1:
                    self.log_warning("⚠️ All attempts failed - returning empty (may be holiday or festival)")
                    return []
                else:
                    # Wait before retry
                    wait_time = (attempt + 1) * 2
                    self.log_warning(f"Retrying in {wait_time}s...")
                    time.sleep(wait_time)

        # This line should never be reached due to return above, but satisfies type checker
        raise RuntimeError("Unexpected code path in fetch_floorsheet_with_retry")
    
    def fetch_price_volume_with_retry(self, max_retries: int = 3) -> Dict[str, Any]:
        """Fetch price/volume history with retry logic and timeout handling
        
        The getPriceVolumeHistory() method can timeout for long requests.
        This wrapper provides retry logic and better error handling.
        
        Returns:
            Dict containing price/volume history data with 'content' key
            
        Raises:
            Exception: If all retry attempts fail
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
        
        # This line should never be reached due to raise above, but satisfies type checker
        raise RuntimeError("Unexpected code path in fetch_price_volume_with_retry")
    
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
        """Run core data collection (all methods including floorsheet during trading hours)"""
        self.log_success("Starting core collection (floorsheet available during trading hours until midnight Nepal time)")
        return self._run_collection(self.core_methods, include_floorsheet=True, collection_type="core")
    
    def run_comprehensive_collection(self) -> Dict[str, Any]:
        """Run comprehensive data collection (all available data)"""
        return self._run_collection(self.core_methods, include_floorsheet=False, collection_type="comprehensive")
    
    def fetch_company_details(self, symbols: List[str]) -> Dict[str, Any]:
        """Fetch detailed company information for multiple symbols
        
        Args:
            symbols: List of company symbols (e.g., ['NABIL', 'GLOBAL', 'NMB'])
            
        Returns:
            Dict containing company details for each symbol
        """
        results = {
            "scraper": "nepse_official_api",
            "collection_type": "company_details",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "companies": {},
            "successful_fetches": [],
            "failed_fetches": [],
            "total_companies": len(symbols),
            "success_count": 0,
            "failure_count": 0,
            "total_fetch_time": 0
        }
        
        self.log_success(f"Fetching company details for {len(symbols)} companies...")
        collection_start = time.time()
        
        for symbol in symbols:
            try:
                self.log_success(f"Fetching details for {symbol}...")
                start_time = time.time()
                
                details = self.nepse.getCompanyDetails(symbol)
                fetch_time = time.time() - start_time
                
                if details:
                    results["companies"][symbol] = details
                    
                    # Extract key financials
                    key_financials = self.extract_key_financials(details)
                    results["companies"][symbol]["key_financials"] = key_financials
                    
                    results["successful_fetches"].append({
                        "symbol": symbol,
                        "fetch_time_seconds": round(fetch_time, 2),
                        "data_size": len(str(details)),
                        "key_financials": key_financials
                    })
                    results["success_count"] += 1
                    results["total_fetch_time"] += fetch_time
                    
                    self.log_success(f"✅ {symbol}: Company details fetched ({fetch_time:.1f}s)")
                    
                    # Display key financials
                    if key_financials.get("financial_information"):
                        fi = key_financials["financial_information"]
                        self.log_success(f"💰 {symbol} Financials: Face Value {fi.get('face_value', 'N/A')}, Market Cap {fi.get('market_capitalization', 'N/A')}")
                    
                    if key_financials.get("shareholding_structure"):
                        ss = key_financials["shareholding_structure"]
                        self.log_success(f"👥 {symbol} Shareholding: Public {ss.get('public_percentage', 'N/A')}, Promoter {ss.get('promoter_percentage', 'N/A')}")
                    
                    # Save individual company details
                    from pathlib import Path
                    import json
                    
                    date_str = datetime.now().strftime('%Y-%m-%d')
                    data_dir = Path(__file__).parent.parent / 'data' / 'daily'
                    data_dir.mkdir(parents=True, exist_ok=True)
                    
                    filename = data_dir / f"{date_str}_company_details_{symbol}.json"
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(details, f, ensure_ascii=False, indent=2, default=str)
                    
                    self.logger.info(f"💾 {symbol}: Company details saved → {filename}")
                else:
                    results["failed_fetches"].append({
                        "symbol": symbol,
                        "error": "No data returned"
                    })
                    results["failure_count"] += 1
                    self.log_error(f"❌ {symbol}: No data returned")
                    
            except Exception as e:
                results["failed_fetches"].append({
                    "symbol": symbol,
                    "error": str(e)
                })
                results["failure_count"] += 1
                self.log_error(f"❌ {symbol}: {e}")
            
            # Brief pause between requests
            time.sleep(0.2)
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        
        # Summary
        self.log_success(f"Company details collection complete:")
        self.log_success(f"  ✅ Successful: {results['success_count']}")
        self.log_success(f"  ❌ Failed: {results['failure_count']}")
        self.log_success(f"  ⏱️ Total time: {results['total_collection_time']}s")
        
        return results
    
    def extract_key_financials(self, company_details: Dict[str, Any]) -> Dict[str, Any]:
        """Extract key financial information and shareholding structure from company details
        
        Args:
            company_details: Raw company details from getCompanyDetails API
            
        Returns:
            Dict with formatted financial information and shareholding structure
        """
        if not company_details:
            return {}
        
        # Extract financial information
        security = company_details.get("security", {})
        security_daily_trade = company_details.get("securityDailyTradeDto", {})
        
        financials = {
            "face_value": security.get("faceValue"),
            "paid_up_capital": company_details.get("paidUpCapital"),
            "issued_capital": company_details.get("issuedCapital"),
            "market_capitalization": company_details.get("marketCapitalization"),
            "stock_listed_shares": company_details.get("stockListedShares")
        }
        
        # Extract shareholding structure
        shareholding = {
            "public_shares": company_details.get("publicShares"),
            "public_percentage": company_details.get("publicPercentage"),
            "promoter_shares": company_details.get("promoterShares"),
            "promoter_percentage": company_details.get("promoterPercentage")
        }
        
        # Extract additional requested fields
        additional_data = {
            "last_updated_date_time": security_daily_trade.get("lastUpdatedDateTime"),
            "fifty_two_week_high": security_daily_trade.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": security_daily_trade.get("fiftyTwoWeekLow"),
            "stock_listed_shares": company_details.get("stockListedShares"),
            "market_capitalization": company_details.get("marketCapitalization"),
            "public_shares": company_details.get("publicShares"),
            "promoter_shares": company_details.get("promoterShares"),
            "public_percentage": company_details.get("publicPercentage"),
            "promoter_percentage": company_details.get("promoterPercentage")
        }
        
        # Format the data for better readability
        formatted = {
            "symbol": company_details.get("security", {}).get("symbol"),
            "company_name": company_details.get("security", {}).get("securityName"),
            "financial_information": {
                "face_value": f"{financials['face_value']} (per share)" if financials['face_value'] else None,
                "paid_up_capital": f"{financials['paid_up_capital']:,.0f} ({financials['paid_up_capital']/1000000000:.1f} billion NPR)" if financials['paid_up_capital'] else None,
                "issued_capital": f"{financials['issued_capital']:,.0f}" if financials['issued_capital'] else None,
                "market_capitalization": f"{financials['market_capitalization']:,.1f} ({financials['market_capitalization']/1000000000:.1f} billion NPR)" if financials['market_capitalization'] else None,
                "stock_listed_shares": f"{financials['stock_listed_shares']:,.0f} shares" if financials['stock_listed_shares'] else None
            },
            "shareholding_structure": {
                "public_shares": f"{shareholding['public_shares']:,} ({shareholding['public_percentage']}%)" if shareholding['public_shares'] and shareholding['public_percentage'] else None,
                "promoter_shares": f"{shareholding['promoter_shares']:,} ({shareholding['promoter_percentage']}%)" if shareholding['promoter_shares'] and shareholding['promoter_percentage'] else None,
                "public_percentage": f"{shareholding['public_percentage']}%" if shareholding['public_percentage'] else None,
                "promoter_percentage": f"{shareholding['promoter_percentage']}%" if shareholding['promoter_percentage'] else None
            },
            "additional_data": {
                "last_updated_date_time": additional_data["last_updated_date_time"],
                "fifty_two_week_high": f"{additional_data['fifty_two_week_high']:.2f}" if additional_data['fifty_two_week_high'] else None,
                "fifty_two_week_low": f"{additional_data['fifty_two_week_low']:.2f}" if additional_data['fifty_two_week_low'] else None,
                "stock_listed_shares": f"{additional_data['stock_listed_shares']:,.0f}" if additional_data['stock_listed_shares'] else None,
                "market_capitalization": f"{additional_data['market_capitalization']:,.0f}" if additional_data['market_capitalization'] else None,
                "public_shares": f"{additional_data['public_shares']:,}" if additional_data['public_shares'] else None,
                "promoter_shares": f"{additional_data['promoter_shares']:,}" if additional_data['promoter_shares'] else None,
                "public_percentage": f"{additional_data['public_percentage']:.2f}%" if additional_data['public_percentage'] else None,
                "promoter_percentage": f"{additional_data['promoter_percentage']:.2f}%" if additional_data['promoter_percentage'] else None
            }
        }
        
        return formatted
    
    def get_company_financials(self, symbol: str) -> Dict[str, Any]:
        """Get key financial information and shareholding structure for a company
        
        Args:
            symbol: Company trading symbol (e.g., 'NABIL')
            
        Returns:
            Dict with formatted financial information and shareholding structure
        """
        try:
            self.log_success(f"Fetching financials for {symbol}...")
            details = self.nepse.getCompanyDetails(symbol)
            
            if details:
                return self.extract_key_financials(details)
            else:
                self.log_error(f"No data returned for {symbol}")
                return {}
                
        except Exception as e:
            self.log_error(f"Failed to get financials for {symbol}: {e}")
            return {}
    
    def load_lookup_data(self, data_type: str, date: Optional[str] = None) -> Optional[Dict]:
        """Load lookup data from JSON files
        
        Args:
            data_type: Type of data ('security_list', 'security_id_key_map', 'sector_scrips')
            date: Date string (YYYY-MM-DD), if None uses latest available
            
        Returns:
            Dict containing the lookup data
        """
        import os
        from pathlib import Path
        
        lookup_dir = Path(__file__).parent.parent / 'data' / 'lookup'
        
        if not lookup_dir.exists():
            self.log_error("Lookup directory not found")
            return None
        
        # Find the latest file if date not specified
        if not date:
            files = list(lookup_dir.glob(f"*_{data_type}.json"))
            if not files:
                self.log_error(f"No {data_type} files found")
                return None
            # Sort by date and get the latest
            files.sort(key=lambda x: x.name, reverse=True)
            latest_file = files[0]
        else:
            latest_file = lookup_dir / f"{date}_{data_type}.json"
            if not latest_file.exists():
                self.log_error(f"File {latest_file} not found")
                return None
        
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.log_success(f"Loaded {data_type} from {latest_file.name}")
            return data
        except Exception as e:
            self.log_error(f"Failed to load {data_type}: {e}")
            return None
    
    def get_all_stocks(self, date: Optional[str] = None) -> List[Dict]:
        """Get list of all available stocks
        
        Args:
            date: Date string (YYYY-MM-DD), if None uses latest available
            
        Returns:
            List of stock dictionaries with symbol, name, id, etc.
        """
        security_list = self.load_lookup_data('security_list', date)
        if not security_list:
            return []
        
        # Filter only active stocks (exclude debentures, etc. if needed)
        active_stocks = [stock for stock in security_list if stock.get('activeStatus') == 'A']
        
        self.log_success(f"Found {len(active_stocks)} active stocks")
        return active_stocks
    
    def find_stock_by_symbol(self, symbol: str, date: Optional[str] = None) -> Optional[Dict]:
        """Find stock information by symbol
        
        Args:
            symbol: Stock trading symbol (e.g., 'NABIL')
            date: Date string (YYYY-MM-DD), if None uses latest available
            
        Returns:
            Stock information dict or None if not found
        """
        security_list = self.load_lookup_data('security_list', date)
        if not security_list:
            return None
        
        # Search for the symbol (case insensitive)
        for stock in security_list:
            if stock.get('symbol', '').upper() == symbol.upper():
                return stock
        
        self.log_warning(f"Stock symbol '{symbol}' not found")
        return None
    
    def get_stock_id(self, symbol: str, date: Optional[str] = None) -> Optional[int]:
        """Get stock ID by symbol
        
        Args:
            symbol: Stock trading symbol
            date: Date string (YYYY-MM-DD), if None uses latest available
            
        Returns:
            Stock ID (integer) or None if not found
        """
        security_list = self.load_lookup_data('security_list', date)
        if not security_list:
            return None
        
        # Find the stock by symbol
        for stock in security_list:
            if stock.get('symbol', '').upper() == symbol.upper():
                return stock.get('id')
        
        return None
    
    def get_stocks_by_sector(self, sector: str, date: Optional[str] = None) -> List[str]:
        """Get list of stock symbols in a specific sector
        
        Args:
            sector: Sector name (e.g., 'Commercial Banks', 'Hydro Power')
            date: Date string (YYYY-MM-DD), if None uses latest available
            
        Returns:
            List of stock symbols in the sector
        """
        sector_data = self.load_lookup_data('sector_scrips', date)
        if not sector_data:
            return []
        
        # Find sector (case insensitive partial match)
        for sector_name, symbols in sector_data.items():
            if sector.lower() in sector_name.lower():
                self.log_success(f"Found {len(symbols)} stocks in sector '{sector_name}'")
                return symbols
        
        self.log_warning(f"Sector '{sector}' not found")
        return []
    
    def get_available_sectors(self, date: Optional[str] = None) -> List[str]:
        """Get list of all available sectors
        
        Args:
            date: Date string (YYYY-MM-DD), if None uses latest available
            
        Returns:
            List of sector names
        """
        sector_data = self.load_lookup_data('sector_scrips', date)
        if not sector_data:
            return []
        
        sectors = list(sector_data.keys())
        self.log_success(f"Found {len(sectors)} sectors")
        return sectors
    
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
    
    def fetch_all_company_data(self, limit: Optional[int] = None, batch_size: int = 10) -> Dict[str, Any]:
        """Fetch company data for all active stocks from the latest lookup file
        
        Args:
            limit: Maximum number of companies to fetch (None for all)
            batch_size: Number of companies to fetch in each batch
            
        Returns:
            Dict containing company data for all fetched companies
        """
        # Get all active stocks from latest lookup file
        all_stocks = self.get_all_stocks()
        
        if not all_stocks:
            self.log_error("No stocks found in lookup data")
            return {"error": "No stocks found"}
        
        # Apply limit if specified
        if limit:
            stocks_to_process = all_stocks[:limit]
            self.log_success(f"Processing {limit} companies (limited from {len(all_stocks)} total)")
        else:
            stocks_to_process = all_stocks
            self.log_success(f"Processing all {len(all_stocks)} active companies")
        
        results = {
            "scraper": "nepse_official_api",
            "collection_type": "all_company_data",
            "timestamp": time.time(),
            "date": datetime.now().strftime("%Y-%m-%d"),
            "total_stocks_available": len(all_stocks),
            "stocks_processed": len(stocks_to_process),
            "companies": {},
            "successful_fetches": [],
            "failed_fetches": [],
            "success_count": 0,
            "failure_count": 0,
            "total_fetch_time": 0
        }
        
        collection_start = time.time()
        
        # Process in batches to avoid overwhelming the API
        for i in range(0, len(stocks_to_process), batch_size):
            batch = stocks_to_process[i:i + batch_size]
            batch_symbols = [stock['symbol'] for stock in batch]
            
            self.log_success(f"Processing batch {i//batch_size + 1}/{(len(stocks_to_process) + batch_size - 1)//batch_size}: {len(batch)} companies")
            
            # Fetch company details for this batch
            batch_results = self.fetch_company_details_batch(batch_symbols)
            
            # Merge results
            results["companies"].update(batch_results.get("companies", {}))
            results["successful_fetches"].extend(batch_results.get("successful_fetches", []))
            results["failed_fetches"].extend(batch_results.get("failed_fetches", []))
            results["success_count"] += batch_results.get("success_count", 0)
            results["failure_count"] += batch_results.get("failure_count", 0)
            results["total_fetch_time"] += batch_results.get("total_fetch_time", 0)
            
            # Brief pause between batches
            if i + batch_size < len(stocks_to_process):
                self.log_success("Waiting 2 seconds before next batch...")
                time.sleep(2)
        
        results["total_collection_time"] = round(time.time() - collection_start, 2)
        
        # Summary
        self.log_success(f"All company data collection complete:")
        self.log_success(f"  📊 Total stocks available: {results['total_stocks_available']}")
        self.log_success(f"  ✅ Processed: {results['stocks_processed']}")
        self.log_success(f"  ✅ Successful: {results['success_count']}")
        self.log_success(f"  ❌ Failed: {results['failure_count']}")
        self.log_success(f"  ⏱️ Total time: {results['total_collection_time']}s")
        
        return results
    
    def fetch_company_details_batch(self, symbols: List[str]) -> Dict[str, Any]:
        """Fetch company details for a batch of symbols (internal method)"""
        results = {
            "companies": {},
            "successful_fetches": [],
            "failed_fetches": [],
            "success_count": 0,
            "failure_count": 0,
            "total_fetch_time": 0
        }
        
        for symbol in symbols:
            try:
                start_time = time.time()
                details = self.nepse.getCompanyDetails(symbol)
                fetch_time = time.time() - start_time
                
                if details:
                    results["companies"][symbol] = details
                    
                    # Extract key financials
                    key_financials = self.extract_key_financials(details)
                    results["companies"][symbol]["key_financials"] = key_financials
                    
                    results["successful_fetches"].append({
                        "symbol": symbol,
                        "security_id": details.get("security", {}).get("id"),
                        "fetch_time_seconds": round(fetch_time, 2),
                        "key_financials": key_financials
                    })
                    results["success_count"] += 1
                    results["total_fetch_time"] += fetch_time
                    
                    self.log_success(f"✅ {symbol} (ID: {details.get('security', {}).get('id')}): Fetched ({fetch_time:.1f}s)")
                else:
                    results["failed_fetches"].append({
                        "symbol": symbol,
                        "error": "No data returned"
                    })
                    results["failure_count"] += 1
                    self.log_error(f"❌ {symbol}: No data returned")
                    
            except Exception as e:
                results["failed_fetches"].append({
                    "symbol": symbol,
                    "error": str(e)
                })
                results["failure_count"] += 1
                self.log_error(f"❌ {symbol}: {e}")
            
            # Brief pause between requests
            time.sleep(0.1)
        
        return results
def main():
    """Main execution function"""
    import sys
    
    fetcher = NEPSEOfficialDataFetcher()
    
    try:
        # Check command line arguments
        if len(sys.argv) > 1 and sys.argv[1] == "financials":
            # Get financials for a single company
            if len(sys.argv) < 3:
                print("Usage: python3 nepse_official_data_fetcher.py financials <SYMBOL>")
                print("Example: python3 nepse_official_data_fetcher.py financials NABIL")
                return
            
            symbol = sys.argv[2].upper()
            financials = fetcher.get_company_financials(symbol)
            
            if financials:
                print(f"\n🏢 {symbol} - {financials.get('company_name', 'Unknown Company')}")
                print("="*60)
                
                if financials.get('additional_data'):
                    ad = financials['additional_data']
                    print("📊 REQUESTED DATA:")
                    print(f"  Last Updated DateTime: {ad.get('last_updated_date_time', 'N/A')}")
                    print(f"  52 Week High: {ad.get('fifty_two_week_high', 'N/A')}")
                    print(f"  52 Week Low: {ad.get('fifty_two_week_low', 'N/A')}")
                    print(f"  Stock Listed Shares: {ad.get('stock_listed_shares', 'N/A')}")
                    print(f"  Market Capitalization: {ad.get('market_capitalization', 'N/A')}")
                    print(f"  Public Shares: {ad.get('public_shares', 'N/A')}")
                    print(f"  Promoter Shares: {ad.get('promoter_shares', 'N/A')}")
                    print(f"  Public Percentage: {ad.get('public_percentage', 'N/A')}")
                    print(f"  Promoter Percentage: {ad.get('promoter_percentage', 'N/A')}")
                
                if financials.get('financial_information'):
                    print("\n💰 FINANCIAL INFORMATION:")
                    fi = financials['financial_information']
                    print(f"  Face Value: {fi.get('face_value', 'N/A')}")
                    print(f"  Paid-up Capital: {fi.get('paid_up_capital', 'N/A')}")
                    print(f"  Issued Capital: {fi.get('issued_capital', 'N/A')}")
                    print(f"  Market Capitalization: {fi.get('market_capitalization', 'N/A')}")
                    print(f"  Stock Listed Shares: {fi.get('stock_listed_shares', 'N/A')}")
                
                if financials.get('shareholding_structure'):
                    print("\n👥 SHAREHOLDING STRUCTURE:")
                    ss = financials['shareholding_structure']
                    print(f"  Public Shares: {ss.get('public_shares', 'N/A')}")
                    print(f"  Promoter Shares: {ss.get('promoter_shares', 'N/A')}")
                    print(f"  Public Percentage: {ss.get('public_percentage', 'N/A')}")
                    print(f"  Promoter Percentage: {ss.get('promoter_percentage', 'N/A')}")
            else:
                print(f"❌ Failed to get financials for {symbol}")
                
        elif len(sys.argv) > 1 and sys.argv[1] == "companies":
            # Fetch data for all companies from latest lookup file
            if len(sys.argv) >= 3 and sys.argv[2] == "all":
                # Optional limit parameter
                limit = None
                if len(sys.argv) >= 4:
                    try:
                        limit = int(sys.argv[3])
                    except ValueError:
                        print("❌ Invalid limit value. Use: python3 nepse_official_data_fetcher.py companies all [limit]")
                        return
                
                results = fetcher.fetch_all_company_data(limit=limit)
                
                print("\n" + "="*80)
                print("🏢 NEPSE ALL COMPANIES DATA COLLECTION RESULTS")
                print("="*80)
                print(f"📊 Total stocks available: {results['total_stocks_available']}")
                print(f"✅ Stocks processed: {results['stocks_processed']}")
                print(f"✅ Successful: {results['success_count']}")
                print(f"❌ Failed: {results['failure_count']}")
                print(f"⏱️ Total time: {results['total_collection_time']}s")
                
                if results['successful_fetches']:
                    print(f"\n🏢 SUCCESSFUL COMPANY FETCHES (showing first 10):")
                    for i, company in enumerate(results['successful_fetches'][:10], 1):
                        kf = company.get('key_financials', {})
                        print(f"{i:2d}. {company['symbol']} (ID: {company.get('security_id', 'N/A')})")
                        
                        # Show additional requested data
                        if kf.get('additional_data'):
                            ad = kf['additional_data']
                            print(f"    📅 Last Updated: {ad.get('last_updated_date_time', 'N/A')}")
                            print(f"    📈 52W High: {ad.get('fifty_two_week_high', 'N/A')}, 52W Low: {ad.get('fifty_two_week_low', 'N/A')}")
                            print(f"    📊 Listed Shares: {ad.get('stock_listed_shares', 'N/A')}")
                            print(f"    💰 Market Cap: {ad.get('market_capitalization', 'N/A')}")
                            print(f"    👥 Public: {ad.get('public_shares', 'N/A')} ({ad.get('public_percentage', 'N/A')})")
                            print(f"    👥 Promoter: {ad.get('promoter_shares', 'N/A')} ({ad.get('promoter_percentage', 'N/A')})")
                        print()
                    
                    if len(results['successful_fetches']) > 10:
                        print(f"... and {len(results['successful_fetches']) - 10} more companies")
                
                if results['failed_fetches']:
                    print(f"\n❌ FAILED COMPANY FETCHES (showing first 5):")
                    for company in results['failed_fetches'][:5]:
                        print(f"  ❌ {company['symbol']}: {company['error']}")
                    if len(results['failed_fetches']) > 5:
                        print(f"... and {len(results['failed_fetches']) - 5} more failures")
                        
            else:
                print("Usage: python3 nepse_official_data_fetcher.py companies all [limit]")
                print("Examples:")
                print("  python3 nepse_official_data_fetcher.py companies all        # Fetch all companies")
                print("  python3 nepse_official_data_fetcher.py companies all 50     # Fetch first 50 companies")
                    
        else:
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