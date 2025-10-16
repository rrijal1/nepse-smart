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
        self.base_url = "https://www.sharesansar.com"
    
    def scrape_indices(self) -> Optional[List[Dict]]:
        """Scrape NEPSE indices and sub-indices from ShareSansar"""
        self.logger.info("🔍 Starting indices scraping...")
        
        url = f"{self.base_url}/market"
        
        try:
            response = self.make_request(url)
            soup = BeautifulSoup(response.content, 'lxml')
            
            # Extract indices data
            indices_data = self._extract_sharesansar_indices(soup)
            
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
    
    def _extract_sharesansar_indices(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract indices data from ShareSansar market page"""
        indices_data = []
        
        try:
            # Method 1: Parse from detailed indices table
            table_indices = self._parse_indices_table_sharesansar(soup)
            if table_indices:
                indices_data.extend(table_indices)
            
            # Method 2: Parse from sub-indices table  
            subindices = self._parse_subindices_table_sharesansar(soup)
            if subindices:
                indices_data.extend(subindices)
            
        except Exception as e:
            self.log_warning(f"Error extracting ShareSansar indices: {e}")
        
        return indices_data
    

    
    def _parse_indices_table_sharesansar(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse main indices table from ShareSansar"""
        indices_data = []
        
        try:
            # Find tables that contain indices data
            tables = soup.find_all('table')
            
            for table in tables:
                # Check if this table contains index data
                table_text = table.get_text()
                if 'NEPSE Index' in table_text and 'Close' in table_text:
                    rows = table.find_all('tr')
                    
                    for row in rows[1:]:  # Skip header
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 7:
                            try:
                                index_info = {
                                    'index_name': cells[0].get_text(strip=True),
                                    'open': clean_numeric_value(cells[1].get_text(strip=True)),
                                    'high': clean_numeric_value(cells[2].get_text(strip=True)),
                                    'low': clean_numeric_value(cells[3].get_text(strip=True)),
                                    'current_value': clean_numeric_value(cells[4].get_text(strip=True)),
                                    'change': clean_numeric_value(cells[5].get_text(strip=True)),
                                    'change_percent': clean_numeric_value(cells[6].get_text(strip=True)),
                                    'turnover': clean_numeric_value(cells[7].get_text(strip=True)) if len(cells) > 7 else None,
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'sharesansar_table'
                                }
                                
                                if index_info['index_name'] and index_info['current_value']:
                                    indices_data.append(index_info)
                                    
                            except Exception as e:
                                self.log_warning(f"Error parsing table row: {e}")
                                continue
                    break
                        
        except Exception as e:
            self.log_warning(f"Error parsing indices table: {e}")
        
        return indices_data
    
    def _parse_subindices_table_sharesansar(self, soup: BeautifulSoup) -> List[Dict]:
        """Parse sub-indices table from ShareSansar"""
        indices_data = []
        
        try:
            # Find tables that contain sub-indices data
            tables = soup.find_all('table')
            
            for table in tables:
                # Check if this table contains sub-index data
                table_text = table.get_text()
                if 'Sub Index' in table_text or ('Banking' in table_text and 'Development Bank' in table_text):
                    rows = table.find_all('tr')
                    
                    for row in rows[1:]:  # Skip header
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 7:
                            try:
                                index_info = {
                                    'index_name': cells[0].get_text(strip=True),
                                    'open': clean_numeric_value(cells[1].get_text(strip=True)),
                                    'high': clean_numeric_value(cells[2].get_text(strip=True)),
                                    'low': clean_numeric_value(cells[3].get_text(strip=True)),
                                    'current_value': clean_numeric_value(cells[4].get_text(strip=True)),
                                    'change': clean_numeric_value(cells[5].get_text(strip=True)),
                                    'change_percent': clean_numeric_value(cells[6].get_text(strip=True)),
                                    'turnover': clean_numeric_value(cells[7].get_text(strip=True)) if len(cells) > 7 else None,
                                    'date': datetime.now().strftime('%Y-%m-%d'),
                                    'source': 'sharesansar_subindex'
                                }
                                
                                if index_info['index_name'] and index_info['current_value']:
                                    indices_data.append(index_info)
                                    
                            except Exception as e:
                                self.log_warning(f"Error parsing subindex row: {e}")
                                continue
                    break
                        
        except Exception as e:
            self.log_warning(f"Error parsing subindices table: {e}")
        
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