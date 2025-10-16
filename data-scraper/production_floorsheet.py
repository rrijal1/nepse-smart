#!/usr/bin/env python3
"""
Production MeroLagani Floorsheet Scraper
- Scrapes daily floorsheet transactions
- Real-time trade data with buyer/seller details
- Optimized for reliability and speed
"""

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

from shared_utils import ScraperBase, clean_numeric_value, create_data_filepath

class ProductionFloorsheetScraper(ScraperBase):
    """Production scraper for MeroLagani floorsheet data"""
    
    def __init__(self):
        super().__init__("MeroLagani-Floorsheet")
        self.base_url = "https://merolagani.com"
    
    def scrape_floorsheet(self, date: Optional[str] = None) -> Optional[List[Dict]]:
        """Scrape floorsheet data from MeroLagani"""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        self.logger.info(f"🔍 Starting floorsheet scraping for {date}...")
        
        url = f"{self.base_url}/floorsheet/"
        
        try:
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract floorsheet data
            floorsheet_data = self._extract_floorsheet_table(soup, date)
            
            if not floorsheet_data:
                self.log_error("No floorsheet data found")
                return None
            
            # Validate data
            validation = self.validate_data(floorsheet_data, ['stock_symbol', 'transaction_no'], min_records=100)
            if not validation['valid']:
                self.log_error(f"Data validation failed: {validation['errors']}")
                return None
            
            self.log_success(f"Scraped {len(floorsheet_data)} floorsheet records")
            return floorsheet_data
            
        except Exception as e:
            self.log_error(f"Floorsheet scraping failed: {e}")
            return None
    
    def _extract_floorsheet_table(self, soup: BeautifulSoup, date: str) -> List[Dict]:
        """Extract floorsheet data from HTML table"""
        floorsheet_data = []
        
        # Find the floorsheet table - try multiple selectors
        table = None
        
        # Try specific floorsheet table selectors
        selectors = [
            'table.table-responsive',
            'table.floorsheet-table',
            '#floorsheet-table',
            '.table-striped',
            'table'
        ]
        
        for selector in selectors:
            table = soup.select_one(selector)
            if table:
                # Check if this looks like a floorsheet table
                headers = [th.get_text(strip=True).lower() for th in table.find_all('th')]
                if any(h in headers for h in ['stock symbol', 'buyer', 'seller', 'quantity']):
                    break
        
        if not table:
            self.log_error("Could not find floorsheet table")
            return []
        
        # Extract table rows
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 6:  # Minimum columns expected
                try:
                    floorsheet_info = {
                        'transaction_no': clean_numeric_value(cols[0].get_text(strip=True)) if cols[0].get_text(strip=True) else None,
                        'stock_symbol': cols[1].get_text(strip=True),
                        'buyer_broker': clean_numeric_value(cols[2].get_text(strip=True)) if cols[2].get_text(strip=True).isdigit() else cols[2].get_text(strip=True),
                        'seller_broker': clean_numeric_value(cols[3].get_text(strip=True)) if cols[3].get_text(strip=True).isdigit() else cols[3].get_text(strip=True),
                        'quantity': clean_numeric_value(cols[4].get_text(strip=True)),
                        'rate': clean_numeric_value(cols[5].get_text(strip=True)),
                        'amount': clean_numeric_value(cols[6].get_text(strip=True)) if len(cols) > 6 else None,
                        'date': date,
                        'source': 'merolagani'
                    }
                    
                    # Calculate amount if not provided
                    if not floorsheet_info['amount'] and floorsheet_info['quantity'] and floorsheet_info['rate']:
                        floorsheet_info['amount'] = floorsheet_info['quantity'] * floorsheet_info['rate']
                    
                    # Only add if essential fields are present
                    if (floorsheet_info['stock_symbol'] and 
                        floorsheet_info['quantity'] and 
                        floorsheet_info['rate']):
                        floorsheet_data.append(floorsheet_info)
                
                except Exception as e:
                    self.log_warning(f"Error parsing floorsheet row: {e}")
                    continue
        
        return floorsheet_data
    
    def save_floorsheet_data(self, data: List[Dict], date: Optional[str] = None) -> Dict[str, bool]:
        """Save floorsheet data to daily and historical files"""
        if not data:
            self.log_error("No data to save")
            return {'daily_saved': False, 'historical_updated': False}
        
        return self.save_with_history(data, "floorsheet", date)
    
    def run_daily_collection(self) -> Dict:
        """Run complete daily floorsheet collection"""
        self.logger.info("🚀 Starting daily floorsheet collection")
        
        result = {
            'scraper': 'floorsheet',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'failed',
            'records': 0,
            'file_path': None,
            'errors': []
        }
        
        try:
            # Scrape floorsheet data
            floorsheet_data = self.scrape_floorsheet()
            
            if floorsheet_data:
                # Save data
                save_results = self.save_floorsheet_data(floorsheet_data)
                if save_results['daily_saved']:
                    result.update({
                        'status': 'success',
                        'records': len(floorsheet_data),
                        'file_path': create_data_filepath("floorsheet"),
                        'historical_updated': save_results['historical_updated']
                    })
                    self.log_success(f"Daily collection completed: {len(floorsheet_data)} records")
                    if save_results['historical_updated']:
                        self.log_success("Historical data updated successfully")
                else:
                    result['errors'].append("Failed to save data")
            else:
                result['errors'].append("Failed to scrape data")
        
        except Exception as e:
            error_msg = f"Daily collection failed: {e}"
            self.log_error(error_msg)
            result['errors'].append(error_msg)
        
        return result

def main():
    """Test the floorsheet scraper"""
    scraper = ProductionFloorsheetScraper()
    result = scraper.run_daily_collection()
    
    print(f"\n📊 FLOORSHEET SCRAPER RESULTS")
    print("=" * 35)
    print(f"Status: {result['status']}")
    print(f"Records: {result['records']}")
    if result['file_path']:
        print(f"File: {result['file_path']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()