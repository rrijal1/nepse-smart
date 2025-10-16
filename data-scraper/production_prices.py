#!/usr/bin/env python3
"""
Production ShareSansar Stock Prices Scraper
- Scrapes 318+ stock prices with OHLC data
- Real-time market indices and statistics
- Optimized for reliability and speed
"""

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

from shared_utils import ScraperBase, clean_numeric_value, create_data_filepath

class ProductionPricesScraper(ScraperBase):
    """Production scraper for ShareSansar stock prices"""
    
    def __init__(self):
        super().__init__("ShareSansar-Prices")
        self.base_url = "https://www.sharesansar.com"
    
    def scrape_stock_prices(self) -> Optional[List[Dict]]:
        """Scrape stock prices from ShareSansar"""
        self.logger.info("🔍 Starting stock prices scraping...")
        
        url = f"{self.base_url}/today-share-price"
        
        try:
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract stock data
            stock_data = self._extract_stock_table(soup)
            
            if not stock_data:
                self.log_error("No stock data found")
                return None
            
            # Validate data
            validation = self.validate_data(stock_data, ['symbol', 'ltp'], min_records=300)
            if not validation['valid']:
                self.log_error(f"Data validation failed: {validation['errors']}")
                return None
            
            self.log_success(f"Scraped {len(stock_data)} stock prices")
            return stock_data
            
        except Exception as e:
            self.log_error(f"Stock prices scraping failed: {e}")
            return None
    
    def _extract_stock_table(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract stock data from HTML table"""
        stock_data = []
        
        # Find the main stock table
        table = soup.find('table', {'id': 'myTableCopy'})
        if not table:
            # Fallback: look for any table with stock-like headers
            tables = soup.find_all('table')
            for t in tables:
                headers = [th.get_text(strip=True).lower() for th in t.find_all('th')]
                if any(h in headers for h in ['symbol', 'ltp', 'high', 'low']):
                    table = t
                    break
        
        if not table:
            self.log_error("Could not find stock prices table")
            return []
        
        # Extract table rows
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            if len(cols) >= 7:  # Minimum columns expected
                try:
                    stock_info = {
                        'symbol': cols[1].get_text(strip=True),
                        'ltp': clean_numeric_value(cols[2].get_text(strip=True)),
                        'high': clean_numeric_value(cols[3].get_text(strip=True)),
                        'low': clean_numeric_value(cols[4].get_text(strip=True)),
                        'open': clean_numeric_value(cols[5].get_text(strip=True)),
                        'qty': clean_numeric_value(cols[6].get_text(strip=True)),
                        'turnover': clean_numeric_value(cols[7].get_text(strip=True)) if len(cols) > 7 else None,
                        'trans': clean_numeric_value(cols[8].get_text(strip=True)) if len(cols) > 8 else None,
                        'diff': clean_numeric_value(cols[9].get_text(strip=True)) if len(cols) > 9 else None,
                        'range': cols[10].get_text(strip=True) if len(cols) > 10 else None,
                        'diff_percent': clean_numeric_value(cols[11].get_text(strip=True)) if len(cols) > 11 else None,
                        'last_trade_time': cols[12].get_text(strip=True) if len(cols) > 12 else None,
                        'prev_close': clean_numeric_value(cols[13].get_text(strip=True)) if len(cols) > 13 else None,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'sharesansar'
                    }
                    
                    # Only add if symbol is valid
                    if stock_info['symbol'] and len(stock_info['symbol']) > 0:
                        stock_data.append(stock_info)
                
                except Exception as e:
                    self.log_warning(f"Error parsing stock row: {e}")
                    continue
        
        return stock_data
    
    def save_prices_data(self, data: List[Dict], date: Optional[str] = None) -> Dict[str, bool]:
        """Save stock prices data to daily and historical files"""
        if not data:
            self.log_error("No data to save")
            return {'daily_saved': False, 'historical_updated': False}
        
        return self.save_with_history(data, "prices", date)
    
    def run_daily_collection(self) -> Dict:
        """Run complete daily stock prices collection"""
        self.logger.info("🚀 Starting daily stock prices collection")
        
        result = {
            'scraper': 'prices',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'failed',
            'records': 0,
            'file_path': None,
            'errors': []
        }
        
        try:
            # Scrape stock prices
            stock_data = self.scrape_stock_prices()
            
            if stock_data:
                # Save data
                save_results = self.save_prices_data(stock_data)
                if save_results['daily_saved']:
                    result.update({
                        'status': 'success',
                        'records': len(stock_data),
                        'file_path': create_data_filepath("prices"),
                        'historical_updated': save_results['historical_updated']
                    })
                    self.log_success(f"Daily collection completed: {len(stock_data)} records")
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
    """Test the prices scraper"""
    scraper = ProductionPricesScraper()
    result = scraper.run_daily_collection()
    
    print(f"\n📊 PRICES SCRAPER RESULTS")
    print("=" * 30)
    print(f"Status: {result['status']}")
    print(f"Records: {result['records']}")
    if result['file_path']:
        print(f"File: {result['file_path']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()