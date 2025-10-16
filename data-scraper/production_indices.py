#!/usr/bin/env python3
"""
Production NEPSE Indices Scraper
- Scrapes NEPSE main index and sub-indices
- Market statistics and sector performance
- Optimized for reliability and speed
"""

from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import re

from shared_utils import ScraperBase, clean_numeric_value, create_data_filepath

class ProductionIndicesScraper(ScraperBase):
    """Production scraper for NEPSE indices and sub-indices"""
    
    def __init__(self):
        super().__init__("NEPSE-Indices")
        self.base_url = "https://www.nepalstock.com"
    
    def scrape_indices(self) -> Optional[List[Dict]]:
        """Scrape NEPSE indices and sub-indices"""
        self.logger.info("🔍 Starting indices scraping...")
        
        url = f"{self.base_url}/indices"
        
        try:
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract indices data
            indices_data = self._extract_indices_data(soup)
            
            if not indices_data:
                self.log_error("No indices data found")
                return None
            
            # Validate data
            validation = self.validate_data(indices_data, ['index_name', 'current_value'], min_records=5)
            if not validation['valid']:
                self.log_error(f"Data validation failed: {validation['errors']}")
                return None
            
            self.log_success(f"Scraped {len(indices_data)} indices")
            return indices_data
            
        except Exception as e:
            self.log_error(f"Indices scraping failed: {e}")
            return None
    
    def _extract_indices_data(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract indices data from HTML"""
        indices_data = []
        
        # Try multiple approaches to find indices data
        
        # Method 1: Look for indices table
        table = soup.find('table', class_='table')
        if table:
            indices_data = self._parse_indices_table(table)
        
        # Method 2: Look for indices cards/divs if table not found
        if not indices_data:
            indices_data = self._parse_indices_cards(soup)
        
        # Method 3: Parse from script data if available
        if not indices_data:
            indices_data = self._parse_indices_from_scripts(soup)
        
        return indices_data
    
    def _parse_indices_table(self, table) -> List[Dict]:
        """Parse indices from table format"""
        indices_data = []
        
        try:
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cols = row.find_all(['td', 'th'])
                if len(cols) >= 3:
                    try:
                        index_info = {
                            'index_name': cols[0].get_text(strip=True),
                            'current_value': clean_numeric_value(cols[1].get_text(strip=True)),
                            'change': clean_numeric_value(cols[2].get_text(strip=True)),
                            'change_percent': clean_numeric_value(cols[3].get_text(strip=True)) if len(cols) > 3 else None,
                            'high': clean_numeric_value(cols[4].get_text(strip=True)) if len(cols) > 4 else None,
                            'low': clean_numeric_value(cols[5].get_text(strip=True)) if len(cols) > 5 else None,
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'source': 'nepalstock'
                        }
                        
                        if index_info['index_name'] and index_info['current_value']:
                            indices_data.append(index_info)
                    
                    except Exception as e:
                        self.log_warning(f"Error parsing index row: {e}")
                        continue
        
        except Exception as e:
            self.log_warning(f"Error parsing indices table: {e}")
        
        return indices_data
    
    def _parse_indices_cards(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse indices from card/div format"""
        indices_data = []
        
        try:
            # Look for index cards or similar structures
            index_containers = soup.find_all(['div', 'section'], class_=re.compile(r'index|indices', re.I))
            
            for container in index_containers:
                index_items = container.find_all(['div', 'li'], class_=re.compile(r'item|card|index', re.I))
                
                for item in index_items:
                    try:
                        # Extract index name and value
                        name_elem = item.find(['h3', 'h4', 'span', 'div'], class_=re.compile(r'name|title', re.I))
                        value_elem = item.find(['span', 'div'], class_=re.compile(r'value|price|current', re.I))
                        change_elem = item.find(['span', 'div'], class_=re.compile(r'change|diff', re.I))
                        
                        if name_elem and value_elem:
                            index_info = {
                                'index_name': name_elem.get_text(strip=True),
                                'current_value': clean_numeric_value(value_elem.get_text(strip=True)),
                                'change': clean_numeric_value(change_elem.get_text(strip=True)) if change_elem else None,
                                'date': datetime.now().strftime('%Y-%m-%d'),
                                'source': 'nepalstock'
                            }
                            
                            if index_info['index_name'] and index_info['current_value']:
                                indices_data.append(index_info)
                    
                    except Exception as e:
                        self.log_warning(f"Error parsing index card: {e}")
                        continue
        
        except Exception as e:
            self.log_warning(f"Error parsing indices cards: {e}")
        
        return indices_data
    
    def _parse_indices_from_scripts(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse indices data from JavaScript/JSON in script tags"""
        indices_data = []
        
        try:
            scripts = soup.find_all('script')
            
            for script in scripts:
                if script.string:
                    script_content = script.string
                    
                    # Look for JSON data containing indices
                    if 'index' in script_content.lower() and '{' in script_content:
                        # Try to extract JSON-like data
                        import json
                        
                        # Simple regex to find potential JSON objects
                        json_matches = re.findall(r'\{[^{}]*".*?"[^{}]*\}', script_content)
                        
                        for match in json_matches:
                            try:
                                data = json.loads(match)
                                if isinstance(data, dict) and any(key in str(data).lower() for key in ['index', 'nepse']):
                                    # Extract relevant fields
                                    index_info = {
                                        'index_name': data.get('name', 'NEPSE Index'),
                                        'current_value': clean_numeric_value(str(data.get('value', data.get('current', '')))),
                                        'change': clean_numeric_value(str(data.get('change', ''))),
                                        'date': datetime.now().strftime('%Y-%m-%d'),
                                        'source': 'nepalstock'
                                    }
                                    
                                    if index_info['current_value']:
                                        indices_data.append(index_info)
                            
                            except (json.JSONDecodeError, ValueError):
                                continue
        
        except Exception as e:
            self.log_warning(f"Error parsing indices from scripts: {e}")
        
        return indices_data
    
    def save_indices_data(self, data: List[Dict], date: Optional[str] = None) -> bool:
        """Save indices data to JSON file"""
        if not data:
            self.log_error("No data to save")
            return False
        
        filepath = create_data_filepath("indices", date)
        return self.save_data(data, filepath)
    
    def run_daily_collection(self) -> Dict:
        """Run complete daily indices collection"""
        self.logger.info("🚀 Starting daily indices collection")
        
        result = {
            'scraper': 'indices',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'failed',
            'records': 0,
            'file_path': None,
            'errors': []
        }
        
        try:
            # Scrape indices data
            indices_data = self.scrape_indices()
            
            if indices_data:
                # Save data
                if self.save_indices_data(indices_data):
                    result.update({
                        'status': 'success',
                        'records': len(indices_data),
                        'file_path': create_data_filepath("indices")
                    })
                    self.log_success(f"Daily collection completed: {len(indices_data)} records")
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
    """Test the indices scraper"""
    scraper = ProductionIndicesScraper()
    result = scraper.run_daily_collection()
    
    print(f"\n📊 INDICES SCRAPER RESULTS")
    print("=" * 30)
    print(f"Status: {result['status']}")
    print(f"Records: {result['records']}")
    if result['file_path']:
        print(f"File: {result['file_path']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()