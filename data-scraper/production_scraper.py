#!/usr/bin/env python3
"""
Production NEPSE Data Scraper
- ShareSansar for stock prices (318+ stocks)
- MeroLagani for floorsheet data (35,750+ transactions with pagination)
- JSON output only for storage efficiency
- Comprehensive error handling for GitHub Actions
- Retry logic and fallback mechanisms
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup
import json
from datetime import datetime, timedelta
import time
import os
import sys
from pathlib import Path
import logging
from typing import Dict, List, Optional, Tuple
import re

# Setup comprehensive logging
def setup_logging():
    """Setup logging for both file and console output"""
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    
    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(log_dir / f"scraper_{datetime.now().strftime('%Y%m%d')}.log"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

class ProductionNepseScraper:
    """Production-ready NEPSE data scraper with comprehensive error handling"""
    
    def __init__(self, max_retries: int = 3, timeout: int = 30):
        self.max_retries = max_retries
        self.timeout = timeout
        
        # Initialize session with robust headers
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
        })
        
        # URLs
        self.sharesansar_prices_url = "https://www.sharesansar.com/today-share-price"
        self.sharesansar_indices_url = "https://www.sharesansar.com/indices-sub-indices"
        self.merolagani_floorsheet_url = "https://merolagani.com/Floorsheet.aspx"
        
        # Data directories
        self.data_dir = Path(__file__).parent.parent / "data"
        self.daily_dir = self.data_dir / "daily"
        self.historical_dir = self.data_dir / "historical"
        
        # Create directories
        for dir_path in [self.data_dir, self.daily_dir, self.historical_dir]:
            dir_path.mkdir(exist_ok=True)
        
        # Form state for MeroLagani pagination
        self.viewstate = None
        self.viewstate_generator = None
        self.eventvalidation = None
        
        logger.info("Production NEPSE Scraper initialized")

    def _make_request_with_retry(self, method: str, url: str, **kwargs) -> Optional[requests.Response]:
        """Make HTTP request with retry logic"""
        for attempt in range(self.max_retries):
            try:
                if method.upper() == 'GET':
                    response = self.session.get(url, timeout=self.timeout, **kwargs)
                else:
                    response = self.session.post(url, timeout=self.timeout, **kwargs)
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                logger.warning(f"Request attempt {attempt + 1} failed for {url}: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    logger.error(f"All {self.max_retries} attempts failed for {url}")
        
        return None

    def scrape_sharesansar_prices(self) -> List[Dict]:
        """
        Scrape stock prices from ShareSansar with error handling
        Returns list of stock price dictionaries
        """
        logger.info("Scraping stock prices from ShareSansar")
        
        response = self._make_request_with_retry('GET', self.sharesansar_prices_url)
        if not response:
            logger.error("Failed to fetch ShareSansar prices page")
            return []
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try multiple table identifiers
            table = None
            for table_id in ['myTableCurrency', 'headFixed']:
                table = soup.find('table', {'id': table_id})
                if table:
                    break
            
            if not table:
                table = soup.find('table', {'class': 'table'})
            
            if not table:
                logger.error("Could not find price data table on ShareSansar")
                return []
            
            # Extract headers
            headers = []
            header_row = table.find('thead')
            if header_row:
                for th in header_row.find_all('th'):
                    headers.append(th.get_text().strip())
            
            # Extract data
            stocks_data = []
            tbody = table.find('tbody')
            if tbody:
                for row in tbody.find_all('tr'):
                    cells = row.find_all(['td', 'th'])
                    if len(cells) >= len(headers) and len(headers) > 0:
                        stock_data = {}
                        for i, cell in enumerate(cells[:len(headers)]):
                            if i < len(headers):
                                cell_text = cell.get_text().strip()
                                # Try to convert numeric values
                                cleaned = cell_text.replace(',', '')
                                try:
                                    if '.' in cleaned and cleaned.replace('.', '').replace('-', '').isdigit():
                                        stock_data[headers[i]] = float(cleaned)
                                    elif cleaned.replace('-', '').isdigit():
                                        stock_data[headers[i]] = int(cleaned)
                                    else:
                                        stock_data[headers[i]] = cell_text
                                except ValueError:
                                    stock_data[headers[i]] = cell_text
                        
                        if stock_data:
                            stock_data['date'] = datetime.now().strftime('%Y-%m-%d')
                            stock_data['scraped_at'] = datetime.now().isoformat()
                            stock_data['source'] = 'sharesansar'
                            stocks_data.append(stock_data)
            
            logger.info(f"Successfully scraped {len(stocks_data)} stock prices from ShareSansar")
            return stocks_data
            
        except Exception as e:
            logger.error(f"Error processing ShareSansar prices: {e}")
            return []

    def scrape_sharesansar_indices(self) -> Dict:
        """
        Scrape market indices from ShareSansar
        Returns indices data dictionary
        """
        logger.info("Scraping market indices from ShareSansar")
        
        response = self._make_request_with_retry('GET', self.sharesansar_indices_url)
        if not response:
            logger.error("Failed to fetch ShareSansar indices page")
            return {}
        
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            indices_data = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'scraped_at': datetime.now().isoformat(),
                'source': 'sharesansar',
                'indices': []
            }
            
            # Find indices table
            table = soup.find('table')
            if table:
                tbody = table.find('tbody')
                if tbody:
                    for row in tbody.find_all('tr'):
                        cells = row.find_all(['td', 'th'])
                        if len(cells) >= 8:
                            try:
                                index_data = {
                                    'name': cells[0].get_text().strip(),
                                    'current': self._parse_numeric(cells[1].get_text()),
                                    'high': self._parse_numeric(cells[2].get_text()),
                                    'low': self._parse_numeric(cells[3].get_text()),
                                    'close': self._parse_numeric(cells[4].get_text()),
                                    'turnover': self._parse_numeric(cells[5].get_text()),
                                    'change': self._parse_numeric(cells[6].get_text()),
                                    'change_percent': self._parse_numeric(cells[7].get_text()),
                                }
                                indices_data['indices'].append(index_data)
                            except Exception as e:
                                logger.debug(f"Error parsing index row: {e}")
                                continue
            
            logger.info(f"Successfully scraped {len(indices_data['indices'])} indices from ShareSansar")
            return indices_data
            
        except Exception as e:
            logger.error(f"Error processing ShareSansar indices: {e}")
            return {}

    def _extract_merolagani_form_state(self, soup: BeautifulSoup):
        """Extract ASP.NET form state from MeroLagani page"""
        try:
            viewstate_input = soup.find('input', {'name': '__VIEWSTATE'})
            self.viewstate = viewstate_input.get('value') if viewstate_input else ''
            
            viewstate_gen_input = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
            self.viewstate_generator = viewstate_gen_input.get('value') if viewstate_gen_input else ''
            
            eventval_input = soup.find('input', {'name': '__EVENTVALIDATION'})
            self.eventvalidation = eventval_input.get('value') if eventval_input else ''
            
            logger.debug("Extracted MeroLagani form state")
            
        except Exception as e:
            logger.error(f"Error extracting MeroLagani form state: {e}")

    def _get_merolagani_pagination_info(self, soup: BeautifulSoup) -> Tuple[int, int, int]:
        """Extract pagination info from MeroLagani page"""
        try:
            pagging_div = soup.find('div', class_='pagging')
            if pagging_div:
                text = pagging_div.get_text()
                
                # Extract total pages
                total_pages_match = re.search(r'Total pages:\s*(\d+)', text)
                total_pages = int(total_pages_match.group(1)) if total_pages_match else 1
                
                # Extract total records
                total_records_match = re.search(r'of\s+(\d+)\s+records', text)
                total_records = int(total_records_match.group(1)) if total_records_match else 0
                
                # Extract current page
                showing_match = re.search(r'Showing\s+(\d+)\s*-\s*(\d+)', text)
                if showing_match:
                    start_record = int(showing_match.group(1))
                    current_page = ((start_record - 1) // 500) + 1
                else:
                    current_page = 1
                
                return current_page, total_pages, total_records
                
        except Exception as e:
            logger.debug(f"Error extracting pagination info: {e}")
        
        return 1, 1, 0

    def _extract_merolagani_floorsheet_page(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract floorsheet data from a single MeroLagani page"""
        floorsheet_data = []
        
        try:
            table = soup.find('table', {'class': 'table'})
            if not table:
                logger.warning("Could not find floorsheet table on MeroLagani")
                return []
            
            rows = table.find_all('tr')
            if len(rows) < 2:
                logger.warning("No data rows found in floorsheet table")
                return []
            
            date_str = datetime.now().strftime('%Y-%m-%d')
            
            for row in rows[1:]:  # Skip header
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 8:
                    try:
                        transaction_data = {
                            'sn': cells[0].get_text().strip(),
                            'transaction_no': cells[1].get_text().strip(),
                            'symbol': cells[2].get_text().strip(),
                            'buyer_broker': cells[3].get_text().strip(),
                            'seller_broker': cells[4].get_text().strip(),
                            'share_quantity': self._parse_numeric(cells[5].get_text()),
                            'rate': self._parse_numeric(cells[6].get_text()),
                            'amount': self._parse_numeric(cells[7].get_text()),
                            'traded_date': date_str,
                            'date': date_str,
                            'scraped_at': datetime.now().isoformat(),
                            'source': 'merolagani'
                        }
                        
                        floorsheet_data.append(transaction_data)
                        
                    except Exception as e:
                        logger.debug(f"Error parsing floorsheet row: {e}")
                        continue
            
            return floorsheet_data
            
        except Exception as e:
            logger.error(f"Error extracting floorsheet data: {e}")
            return []

    def _navigate_merolagani_page(self, target_page: int) -> Optional[BeautifulSoup]:
        """Navigate to specific page on MeroLagani"""
        try:
            form_data = {
                '__EVENTTARGET': '',
                '__EVENTARGUMENT': '',
                '__VIEWSTATE': self.viewstate,
                '__VIEWSTATEGENERATOR': self.viewstate_generator,
                '__EVENTVALIDATION': self.eventvalidation,
                'ctl00$ASCompany$hdnAutoSuggest': '0',
                'ctl00$ASCompany$txtAutoSuggest': '',
                'ctl00$txtNews': '',
                'ctl00$AutoSuggest1$hdnAutoSuggest': '0',
                'ctl00$AutoSuggest1$txtAutoSuggest': '',
                'ctl00$ContentPlaceHolder1$ASCompanyFilter$hdnAutoSuggest': '0',
                'ctl00$ContentPlaceHolder1$ASCompanyFilter$txtAutoSuggest': '',
                'ctl00$ContentPlaceHolder1$txtBuyerBrokerCodeFilter': '',
                'ctl00$ContentPlaceHolder1$txtSellerBrokerCodeFilter': '',
                'ctl00$ContentPlaceHolder1$txtFloorsheetDateFilter': '',
                'ctl00$ContentPlaceHolder1$PagerControl1$hdnPCID': 'PC1',
                'ctl00$ContentPlaceHolder1$PagerControl1$hdnCurrentPage': str(target_page - 1),
                'ctl00$ContentPlaceHolder1$PagerControl1$btnPaging': '',
                'ctl00$ContentPlaceHolder1$PagerControl2$hdnPCID': 'PC2',
                'ctl00$ContentPlaceHolder1$PagerControl2$hdnCurrentPage': str(target_page - 1),
                'ctl00$ContentPlaceHolder1$PagerControl2$btnPaging': '',
            }
            
            response = self._make_request_with_retry(
                'POST', 
                self.merolagani_floorsheet_url,
                data=form_data,
                headers={
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'Referer': self.merolagani_floorsheet_url
                }
            )
            
            if response:
                soup = BeautifulSoup(response.content, 'html.parser')
                self._extract_merolagani_form_state(soup)
                return soup
            
            return None
            
        except Exception as e:
            logger.error(f"Error navigating to MeroLagani page {target_page}: {e}")
            return None

    def scrape_merolagani_floorsheet(self, max_pages: int = 0) -> List[Dict]:
        """
        Scrape floorsheet data from MeroLagani with pagination
        Args:
            max_pages: Maximum number of pages to scrape (0 = all pages, default: 0)
        """
        logger.info(f"Scraping floorsheet data from MeroLagani (max {max_pages} pages)")
        
        all_floorsheet_data = []
        
        try:
            # Get initial page
            response = self._make_request_with_retry('GET', self.merolagani_floorsheet_url)
            if not response:
                logger.error("Failed to fetch MeroLagani floorsheet page")
                return []
            
            soup = BeautifulSoup(response.content, 'html.parser')
            self._extract_merolagani_form_state(soup)
            
            # Get pagination info
            current_page, total_pages, total_records = self._get_merolagani_pagination_info(soup)
            logger.info(f"Found {total_pages} total pages with {total_records} records")
            
            # Limit pages (0 means all pages)
            if max_pages == 0:
                pages_to_scrape = total_pages
                logger.info(f"Will scrape ALL {pages_to_scrape} pages (full floorsheet)")
            else:
                pages_to_scrape = min(total_pages, max_pages)
                logger.info(f"Will scrape {pages_to_scrape} of {total_pages} pages")
            
            # Process each page
            for page_num in range(1, pages_to_scrape + 1):
                logger.info(f"Scraping page {page_num}/{pages_to_scrape}")
                
                # Use initial soup for first page, navigate for others
                if page_num == 1:
                    page_soup = soup
                else:
                    page_soup = self._navigate_merolagani_page(page_num)
                    if not page_soup:
                        logger.warning(f"Failed to navigate to page {page_num}, continuing...")
                        continue
                
                # Extract data from current page
                page_data = self._extract_merolagani_floorsheet_page(page_soup)
                all_floorsheet_data.extend(page_data)
                
                logger.info(f"Page {page_num}: {len(page_data)} transactions. Total: {len(all_floorsheet_data)}")
                
                # Respectful delay
                if page_num < pages_to_scrape:
                    time.sleep(1)
            
            logger.info(f"Successfully scraped {len(all_floorsheet_data)} floorsheet transactions from MeroLagani")
            return all_floorsheet_data
            
        except Exception as e:
            logger.error(f"Error scraping MeroLagani floorsheet: {e}")
            return all_floorsheet_data  # Return partial data if available

    def _parse_numeric(self, text: str) -> Optional[float]:
        """Parse numeric values from text"""
        try:
            cleaned = text.replace(',', '').replace('Rs.', '').strip()
            return float(cleaned) if cleaned else None
        except (ValueError, AttributeError):
            return None

    def save_data_to_json(self, data: List[Dict], data_type: str, date_str: str):
        """Save data to JSON file only (no CSV for storage efficiency)"""
        if not data:
            logger.warning(f"No {data_type} data to save for {date_str}")
            return False
        
        try:
            # Save to daily directory
            json_file = self.daily_dir / f"{date_str}_{data_type}.json"
            
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Saved {len(data)} {data_type} records to {json_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving {data_type} data: {e}")
            return False

    def update_historical_data(self, new_data: List[Dict], data_type: str):
        """Update historical JSON database"""
        if not new_data:
            return False
        
        try:
            historical_file = self.historical_dir / f"historical_{data_type}.json"
            
            # Load existing data
            historical_data = []
            if historical_file.exists():
                with open(historical_file, 'r', encoding='utf-8') as f:
                    historical_data = json.load(f)
            
            # Append new data
            historical_data.extend(new_data)
            
            # Remove duplicates for prices (keep latest)
            if data_type == 'prices':
                seen = set()
                unique_data = []
                for item in reversed(historical_data):  # Reverse to keep latest
                    key = (item.get('date', ''), item.get('Symbol', '').strip())
                    if key not in seen and key[1]:  # Ensure symbol exists
                        seen.add(key)
                        unique_data.append(item)
                historical_data = list(reversed(unique_data))
            
            # Save updated data
            with open(historical_file, 'w', encoding='utf-8') as f:
                json.dump(historical_data, f, indent=2, ensure_ascii=False, default=str)
            
            logger.info(f"Updated historical {data_type}: {len(historical_data)} total records")
            return True
            
        except Exception as e:
            logger.error(f"Error updating historical {data_type} data: {e}")
            return False

    def run_daily_collection(self, floorsheet_pages: int = 0) -> Dict[str, bool]:
        """
        Run complete daily data collection with error handling
        Args:
            floorsheet_pages: Number of pages to scrape (0 = all pages, default: 0)
        Returns:
            status dictionary for each data type
        """
        logger.info("Starting daily NEPSE data collection")
        
        date_str = datetime.now().strftime("%Y-%m-%d")
        results = {
            'prices': False,
            'floorsheet': False,
            'indices': False,
            'overall_success': False
        }
        
        try:
            # 1. ShareSansar Stock Prices
            logger.info("=== Collecting Stock Prices from ShareSansar ===")
            prices_data = self.scrape_sharesansar_prices()
            
            if prices_data and len(prices_data) > 0:
                if self.save_data_to_json(prices_data, 'prices', date_str):
                    self.update_historical_data(prices_data, 'prices')
                    results['prices'] = True
                    logger.info(f"✅ Stock prices: {len(prices_data)} records")
                else:
                    logger.error("❌ Failed to save stock prices")
            else:
                logger.error("❌ No stock prices data obtained")
            
            time.sleep(2)  # Respectful delay
            
            # 2. MeroLagani Floorsheet Data
            pages_desc = "ALL pages" if floorsheet_pages == 0 else f"{floorsheet_pages} pages"
            logger.info(f"=== Collecting Floorsheet Data from MeroLagani ({pages_desc}) ===")
            floorsheet_data = self.scrape_merolagani_floorsheet(max_pages=floorsheet_pages)
            
            if floorsheet_data and len(floorsheet_data) > 0:
                if self.save_data_to_json(floorsheet_data, 'floorsheet', date_str):
                    self.update_historical_data(floorsheet_data, 'floorsheet')
                    results['floorsheet'] = True
                    
                    # Log summary statistics
                    symbols = set(t['symbol'] for t in floorsheet_data)
                    total_volume = sum([t['share_quantity'] for t in floorsheet_data if t['share_quantity']])
                    total_amount = sum([t['amount'] for t in floorsheet_data if t['amount']])
                    
                    logger.info(f"✅ Floorsheet: {len(floorsheet_data)} transactions")
                    logger.info(f"   📈 {len(symbols)} symbols, {total_volume:,.0f} shares, Rs.{total_amount:,.2f}")
                else:
                    logger.error("❌ Failed to save floorsheet data")
            else:
                logger.error("❌ No floorsheet data obtained")
            
            time.sleep(2)  # Respectful delay
            
            # 3. ShareSansar Market Indices
            logger.info("=== Collecting Market Indices from ShareSansar ===")
            indices_data = self.scrape_sharesansar_indices()
            
            if indices_data and indices_data.get('indices'):
                indices_list = [indices_data]  # Wrap in list for consistency
                if self.save_data_to_json(indices_list, 'indices', date_str):
                    self.update_historical_data(indices_list, 'indices')
                    results['indices'] = True
                    logger.info(f"✅ Market indices: {len(indices_data['indices'])} indices")
                else:
                    logger.error("❌ Failed to save indices data")
            else:
                logger.error("❌ No indices data obtained")
            
            # Overall success check
            success_count = sum(results[key] for key in ['prices', 'floorsheet', 'indices'])
            results['overall_success'] = success_count >= 2  # At least 2 out of 3 must succeed
            
            if results['overall_success']:
                logger.info(f"🎉 Daily collection completed successfully ({success_count}/3 data sources)")
            else:
                logger.error(f"❌ Daily collection failed ({success_count}/3 data sources)")
            
            return results
            
        except Exception as e:
            logger.error(f"Unexpected error during daily collection: {e}")
            return results

def main():
    """Main entry point for production scraper"""
    scraper = ProductionNepseScraper(max_retries=3, timeout=30)
    
    # Get pages from environment or default to all pages (0)
    max_pages = int(os.environ.get('FLOORSHEET_PAGES', '0'))
    
    try:
        results = scraper.run_daily_collection(floorsheet_pages=max_pages)
        
        # Exit with appropriate code for GitHub Actions
        if results['overall_success']:
            logger.info("SUCCESS: Data collection completed")
            sys.exit(0)
        else:
            logger.error("FAILURE: Data collection failed")
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"CRITICAL ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()