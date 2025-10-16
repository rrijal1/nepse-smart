#!/usr/bin/env python3
"""
Production NRB Banking & Macro Economic Data Scraper
- Scrapes deposit and lending rates from NRB
- Key macro economic indicators
- Optimized for reliability and speed
"""

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

from shared_utils import ScraperBase, clean_numeric_value, create_data_filepath

class ProductionMacroScraper(ScraperBase):
    """Production scraper for NRB banking and macro economic data"""
    
    def __init__(self):
        super().__init__("NRB-Macro")
        self.base_url = "https://www.nrb.org.np"
    
    def scrape_nrb_data(self) -> Optional[List[Dict]]:
        """Scrape NRB banking and economic data"""
        self.logger.info("🔍 Starting NRB data scraping...")
        
        all_data = []
        
        # Scrape different types of NRB data
        deposit_data = self._scrape_deposit_rates()
        if deposit_data:
            all_data.extend(deposit_data)
        
        lending_data = self._scrape_lending_rates()
        if lending_data:
            all_data.extend(lending_data)
        
        if not all_data:
            self.log_error("No NRB data found")
            return None
        
        # Validate data
        validation = self.validate_data(all_data, ['data_type'], min_records=5)
        if not validation['valid']:
            self.log_error(f"Data validation failed: {validation['errors']}")
            return None
        
        self.log_success(f"Scraped {len(all_data)} NRB records")
        return all_data
    
    def _scrape_deposit_rates(self) -> Optional[List[Dict]]:
        """Scrape deposit rates from NRB"""
        try:
            url = f"{self.base_url}/fxmexchangerate.php?YY=2024&MM=12&DD=01&B1=Go"
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            deposit_data = []
            
            # Look for deposit rates table
            tables = soup.find_all('table')
            for table in tables:
                # Check if this looks like a deposit rates table
                text_content = table.get_text().lower()
                if 'deposit' in text_content or 'savings' in text_content:
                    deposit_data = self._parse_banking_table(table, 'deposit_rates')
                    break
            
            return deposit_data
            
        except Exception as e:
            self.log_warning(f"Failed to scrape deposit rates: {e}")
            return None
    
    def _scrape_lending_rates(self) -> Optional[List[Dict]]:
        """Scrape lending rates from NRB"""
        try:
            url = f"{self.base_url}/fxmexchangerate.php?YY=2024&MM=12&DD=01&B1=Go"
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            lending_data = []
            
            # Look for lending rates table
            tables = soup.find_all('table')
            for table in tables:
                # Check if this looks like a lending rates table
                text_content = table.get_text().lower()
                if 'lending' in text_content or 'loan' in text_content or 'credit' in text_content:
                    lending_data = self._parse_banking_table(table, 'lending_rates')
                    break
            
            return lending_data
            
        except Exception as e:
            self.log_warning(f"Failed to scrape lending rates: {e}")
            return None
    
    def _parse_banking_table(self, table, data_type: str) -> List[Dict]:
        """Parse banking data from table"""
        banking_data = []
        
        try:
            rows = table.find_all('tr')[1:]  # Skip header row
            
            for i, row in enumerate(rows):
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 2:
                    try:
                        # Extract banking information
                        bank_info = {
                            'data_type': data_type,
                            'bank_name': cols[0].get_text(strip=True) if len(cols) > 0 else f"Bank_{i+1}",
                            'rate': clean_numeric_value(cols[1].get_text(strip=True)) if len(cols) > 1 else None,
                            'minimum_amount': clean_numeric_value(cols[2].get_text(strip=True)) if len(cols) > 2 else None,
                            'maximum_amount': clean_numeric_value(cols[3].get_text(strip=True)) if len(cols) > 3 else None,
                            'currency': cols[4].get_text(strip=True) if len(cols) > 4 else 'NPR',
                            'effective_date': cols[5].get_text(strip=True) if len(cols) > 5 else None,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'nrb'
                        }
                        
                        # Only add if essential fields are present
                        if bank_info['bank_name'] and bank_info['rate'] is not None:
                            banking_data.append(bank_info)
                    
                    except Exception as e:
                        self.log_warning(f"Error parsing banking row: {e}")
                        continue
        
        except Exception as e:
            self.log_warning(f"Error parsing banking table: {e}")
        
        return banking_data
    
    def scrape_exchange_rates(self) -> Optional[List[Dict]]:
        """Scrape foreign exchange rates from NRB"""
        self.logger.info("🔍 Starting exchange rates scraping...")
        
        try:
            url = f"{self.base_url}/fxmexchangerate.php"
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            exchange_data = []
            
            # Look for exchange rates table
            table = soup.find('table')
            if table:
                rows = table.find_all('tr')[1:]  # Skip header
                
                for row in rows:
                    cols = row.find_all(['td', 'th'])
                    if len(cols) >= 4:
                        try:
                            exchange_info = {
                                'data_type': 'exchange_rates',
                                'currency': cols[0].get_text(strip=True),
                                'currency_code': cols[1].get_text(strip=True) if len(cols) > 1 else None,
                                'buying_rate': clean_numeric_value(cols[2].get_text(strip=True)) if len(cols) > 2 else None,
                                'selling_rate': clean_numeric_value(cols[3].get_text(strip=True)) if len(cols) > 3 else None,
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'source': 'nrb'
                            }
                            
                            if exchange_info['currency'] and (exchange_info['buying_rate'] or exchange_info['selling_rate']):
                                exchange_data.append(exchange_info)
                        
                        except Exception as e:
                            self.log_warning(f"Error parsing exchange rate row: {e}")
                            continue
            
            return exchange_data
            
        except Exception as e:
            self.log_error(f"Exchange rates scraping failed: {e}")
            return None
    
    def save_macro_data(self, data: List[Dict], date: Optional[str] = None) -> bool:
        """Save macro economic data to JSON file"""
        if not data:
            self.log_error("No data to save")
            return False
        
        filepath = create_data_filepath("nrb_banking", date)
        return self.save_data(data, filepath)
    
    def run_daily_collection(self) -> Dict:
        """Run complete daily macro data collection"""
        self.logger.info("🚀 Starting daily macro data collection")
        
        result = {
            'scraper': 'macro',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'failed',
            'records': 0,
            'file_path': None,
            'errors': []
        }
        
        try:
            # Scrape NRB data
            nrb_data = self.scrape_nrb_data()
            
            # Also try to get exchange rates
            exchange_data = self.scrape_exchange_rates()
            if exchange_data:
                if nrb_data:
                    nrb_data.extend(exchange_data)
                else:
                    nrb_data = exchange_data
            
            if nrb_data:
                # Save data
                if self.save_macro_data(nrb_data):
                    result.update({
                        'status': 'success',
                        'records': len(nrb_data),
                        'file_path': create_data_filepath("nrb_banking")
                    })
                    self.log_success(f"Daily collection completed: {len(nrb_data)} records")
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
    """Test the macro scraper"""
    scraper = ProductionMacroScraper()
    result = scraper.run_daily_collection()
    
    print(f"\n📊 MACRO SCRAPER RESULTS")
    print("=" * 28)
    print(f"Status: {result['status']}")
    print(f"Records: {result['records']}")
    if result['file_path']:
        print(f"File: {result['file_path']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()