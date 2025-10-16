#!/usr/bin/env python3
"""
Production NRB Banking & Macro Economic Data Scraper
- Scrapes deposit and lending rates from NRB
- Key macro economic indicators
- Optimized for reliability and speed
"""

from bs4 import BeautifulSoup, Tag
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional, cast
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
            # Try specific deposit/lending rates page first
            url = f"{self.base_url}/cmfm_rates/lending_rates"
            response = self.make_request(url)
            
            if not response:
                # Fallback to general interest rates page
                url = f"{self.base_url}/category/interest-rate-structure/"
                response = self.make_request(url)
            
            if not response:
                self.log_warning("No response from deposit rates pages")
                return None
                
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
            # Try specific lending rates page first
            url = f"{self.base_url}/cmfm_rates/lending_rates"
            response = self.make_request(url)
            
            if not response:
                # Fallback to policy rates
                url = f"{self.base_url}/cmfm_rates/policy_rates"
                response = self.make_request(url)
            
            if not response:
                # Final fallback to general interest rates page
                url = f"{self.base_url}/category/interest-rate-structure/"
                response = self.make_request(url)
            
            if not response:
                self.log_warning("No response from lending rates pages")
                return None
                
            soup = BeautifulSoup(response.content, 'lxml')
            
            lending_data = []
            
            # Look for lending rates table
            tables = soup.find_all('table')
            for table in tables:
                # Check if this looks like a lending rates table
                text_content = table.get_text().lower()
                if 'lending' in text_content or 'loan' in text_content or 'credit' in text_content or 'policy' in text_content:
                    lending_data = self._parse_banking_table(table, 'lending_rates')
                    break
            
            return lending_data
            
        except Exception as e:
            self.log_warning(f"Failed to scrape lending rates: {e}")
            return None
    
    def _parse_api_forex_data(self, forex_data: List[Dict]) -> List[Dict]:
        """Parse forex data from NRB API"""
        exchange_data = []
        
        try:
            for item in forex_data:
                if isinstance(item, dict):
                    # Extract relevant fields from API response
                    exchange_info = {
                        'data_type': 'exchange_rates',
                        'currency': item.get('title', {}).get('rendered', ''),
                        'content': item.get('content', {}).get('rendered', ''),
                        'date_published': item.get('date', ''),
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'source': 'nrb_api'
                    }
                    
                    # Try to extract rates from content if available
                    if exchange_info['content']:
                        # Parse HTML content for rates
                        from bs4 import BeautifulSoup
                        soup = BeautifulSoup(exchange_info['content'], 'lxml')
                        text = soup.get_text()
                        
                        # Look for numeric values that might be rates
                        import re
                        rates = re.findall(r'\d+\.?\d*', text)
                        if rates:
                            exchange_info['rates'] = [float(r) for r in rates[:2]]  # Usually buy/sell rates
                    
                    if exchange_info['currency']:
                        exchange_data.append(exchange_info)
        
        except Exception as e:
            self.log_warning(f"Error parsing API forex data: {e}")
        
        return exchange_data
    
    def _parse_banking_table(self, table, data_type: str) -> List[Dict]:
        """Parse banking data from table"""
        banking_data = []
        
        try:
            table_tag = cast(Tag, table)
            all_rows = table_tag.find_all('tr')
            if not all_rows or len(all_rows) <= 1:
                return []
            rows = all_rows[1:]  # Skip header row
            
            for i, row in enumerate(rows):
                cols = cast(Tag, row).find_all(['td', 'th'])
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
    
    def _parse_forex_table(self, table) -> List[Dict]:
        """Parse forex exchange rates table"""
        forex_data = []
        
        try:
            table_tag = cast(Tag, table)
            rows = table_tag.find_all('tr')
            headers = []
            
            # Find headers
            if rows:
                header_row = cast(Tag, rows[0])
                headers = [th.get_text().strip() for th in header_row.find_all(['th', 'td'])]
            
            # Process data rows
            for row in rows[1:]:
                cells = cast(Tag, row).find_all(['td', 'th'])
                if len(cells) >= 2:
                    row_data = [cell.get_text().strip() for cell in cells]
                    
                    # Look for currency data
                    if any(currency in ' '.join(row_data).upper() for currency in ['USD', 'EUR', 'GBP', 'JPY', 'INR', 'CNY']):
                        forex_info = {
                            'data_type': 'exchange_rates',
                            'currency': row_data[0] if row_data else 'Unknown',
                            'rates': row_data[1:] if len(row_data) > 1 else [],
                            'headers': headers,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'nrb'
                        }
                        forex_data.append(forex_info)
                        
        except Exception as e:
            self.log_warning(f"Error parsing forex table: {e}")
        
        return forex_data
    
    def _extract_rates_from_element(self, element) -> List[Dict]:
        """Extract rate information from any HTML element"""
        rates_data = []
        
        try:
            text_content = element.get_text()
            
            # Look for numeric values that might be rates
            import re
            numbers = re.findall(r'\d+\.?\d*', text_content)
            
            if numbers and any(keyword in text_content.lower() for keyword in ['rate', 'exchange', 'forex', 'currency']):
                rate_info = {
                    'data_type': 'exchange_rates',
                    'content': text_content.strip(),
                    'numbers': [float(n) for n in numbers if n],
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'source': 'nrb'
                }
                rates_data.append(rate_info)
                
        except Exception as e:
            self.log_warning(f"Error extracting rates from element: {e}")
        
        return rates_data
    
    def _scrape_forex_from_homepage(self, soup) -> List[Dict]:
        """Scrape foreign exchange rates from homepage"""
        forex_data = []
        
        try:
            # Look for tables that contain forex data by checking for currency codes
            tables = soup.find_all('table')
            for table in tables:
                text_content = table.get_text()
                if any(currency in text_content.upper() for currency in ['USD', 'EUR', 'GBP', 'JPY']):
                    forex_data = self._parse_forex_table(table)
                    if forex_data:
                        self.log_success(f"Found forex table with {len(forex_data)} currencies")
                        break
                    
        except Exception as e:
            self.log_warning(f"Error scraping forex from homepage: {e}")
        
        return forex_data
    
    def _scrape_indicators_from_homepage(self, soup) -> List[Dict]:
        """Scrape banking indicators from homepage"""
        indicators_data = []
        
        try:
            # Look for tables that contain banking indicators
            tables = soup.find_all('table')
            for table in tables:
                table_tag = cast(Tag, table)
                text_content = table_tag.get_text()
                # Check if this table contains banking indicators
                if any(indicator in text_content for indicator in ['Total Deposits', 'Total Lending', 'CD Ratio', 'Interbank']):
                    rows = table_tag.find_all('tr')
                    
                    for row in rows:
                        cells = cast(Tag, row).find_all(['td', 'th'])
                        if len(cells) >= 3:
                            cell_texts = [cell.get_text().strip() for cell in cells]
                            
                            # Skip header rows
                            if 'Last Updated' in cell_texts[0] or not cell_texts[0]:
                                continue
                                
                            # Extract indicator name and values
                            indicator_name = cell_texts[0]
                            if len(cell_texts) >= 3 and indicator_name:
                                indicator_info = {
                                    'data_type': 'banking_indicators',
                                    'indicator': indicator_name,
                                    'current_value': cell_texts[1],
                                    'previous_value': cell_texts[2] if len(cell_texts) > 2 else None,
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'nrb_homepage'
                                }
                                
                                # Extract unit from indicator name if present
                                if '(' in indicator_name and ')' in indicator_name:
                                    parts = indicator_name.split('(')
                                    indicator_info['indicator'] = parts[0].strip()
                                    indicator_info['unit'] = parts[1].split(')')[0].strip()
                                
                                indicators_data.append(indicator_info)
                    
                    if indicators_data:
                        self.log_success(f"Found indicators table with {len(indicators_data)} indicators")
                        break
                    
        except Exception as e:
            self.log_warning(f"Error scraping indicators from homepage: {e}")
        
        return indicators_data
    
    def _scrape_short_term_rates_from_homepage(self, soup) -> List[Dict]:
        """Scrape short term interest rates from homepage"""
        rates_data = []
        
        try:
            # Look for elements that contain short term rates patterns
            # First try to find by text content
            for element in soup.find_all(['div', 'section']):
                element_tag = cast(Tag, element)
                text_content = element_tag.get_text()
                if 'Short Term Interest Rates' in text_content:
                    # Look for the rate values in divs within this section
                    rate_divs = element_tag.find_all('div', class_='col-3')
                    
                    for div in rate_divs:
                        div_tag = cast(Tag, div)
                        rate_value_div = div_tag.find('div', class_='text-secondary')
                        rate_label_div = div_tag.find('div', class_='font-size-xs')
                        
                        if rate_value_div and rate_label_div:
                            rate_info = {
                                'data_type': 'short_term_rates',
                                'maturity': rate_label_div.get_text().strip(),
                                'rate': rate_value_div.get_text().strip(),
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'source': 'nrb_homepage'
                            }
                            rates_data.append(rate_info)
                    
                    if rates_data:
                        self.log_success(f"Found short term rates with {len(rates_data)} maturities")
                        break
                    
        except Exception as e:
            self.log_warning(f"Error scraping short term rates from homepage: {e}")
        
        return rates_data
    
    def scrape_nrb_homepage_data(self) -> Optional[List[Dict]]:
        """Scrape all data from NRB homepage - forex, indicators, and interest rates"""
        self.logger.info("🔍 Starting NRB homepage data scraping...")
        
        try:
            # Use the main homepage which has all the tables
            url = f"{self.base_url}/"
            response = self.make_request(url)
            
            if not response:
                self.log_warning("No response from NRB homepage")
                return None
            
            soup = BeautifulSoup(response.content, 'lxml')
            all_data = []
            
            # 1. Scrape Foreign Exchange Rates
            forex_data = self._scrape_forex_from_homepage(soup)
            if forex_data:
                all_data.extend(forex_data)
            
            # 2. Scrape Banking Indicators
            indicators_data = self._scrape_indicators_from_homepage(soup)
            if indicators_data:
                all_data.extend(indicators_data)
            
            # 3. Scrape Short Term Interest Rates
            interest_rates_data = self._scrape_short_term_rates_from_homepage(soup)
            if interest_rates_data:
                all_data.extend(interest_rates_data)
            
            return all_data if all_data else None
            
        except Exception as e:
            self.log_error(f"NRB homepage scraping failed: {e}")
            return None
    
    def save_macro_data(self, data: List[Dict], date: Optional[str] = None) -> Dict[str, bool]:
        """Save macro economic data to daily and historical files"""
        if not data:
            self.log_error("No data to save")
            return {'daily_saved': False, 'historical_updated': False}
        
        return self.save_with_history(data, "macro", date)
    
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
            # Scrape all NRB data from homepage (forex, indicators, rates)
            nrb_data = self.scrape_nrb_homepage_data()
            
            # If homepage fails, try individual methods
            if not nrb_data:
                nrb_data = self.scrape_nrb_data()
            
            if nrb_data:
                # Save data
                save_results = self.save_macro_data(nrb_data)
                if save_results['daily_saved']:
                    result.update({
                        'status': 'success',
                        'records': len(nrb_data),
                        'file_path': create_data_filepath("macro"),
                        'historical_updated': save_results['historical_updated']
                    })
                    self.log_success(f"Daily collection completed: {len(nrb_data)} records")
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