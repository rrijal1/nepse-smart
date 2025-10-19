#!/usr/bin/env python3
"""
Production MeroLagani Floorsheet Scraper
- Scrapes daily floorsheet transactions from all pages.
- Handles ASP.NET pagination by simulating 'Next' button clicks.
- Real-time trade data with buyer/seller details.
- Optimized for reliability and speed.
"""

from bs4 import BeautifulSoup, Tag
from datetime import datetime
from typing import List, Dict, Optional, cast

from shared_utils import ScraperBase, clean_numeric_value, create_data_filepath

class ProductionFloorsheetScraper(ScraperBase):
    """Production scraper for MeroLagani floorsheet data with pagination."""
    
    def __init__(self):
        super().__init__("MeroLagani-Floorsheet")
        self.base_url = "https://merolagani.com"
        self.floorsheet_path = "/Floorsheet.aspx"
    
    def scrape_floorsheet(self, date: Optional[str] = None) -> Optional[List[Dict]]:
        """Scrape all pages of floorsheet data from MeroLagani for a given date."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        self.logger.info(f"🔍 Starting full floorsheet scrape for {date}...")
        url = f"{self.base_url}{self.floorsheet_path}"
        all_floorsheet_data = []

        try:
            # Initial GET request for the first page and form state
            response = self.make_request(url)
            if not response:
                self.log_error("Failed to fetch initial floorsheet page.")
                return None
            
            soup = BeautifulSoup(response.content, 'lxml')
            page_count = 1

            while True:
                self.log_success(f"Scraping page {page_count}...")
                
                # Extract data from the current page's table
                page_data = self._extract_floorsheet_table(soup, date)
                if page_data:
                    all_floorsheet_data.extend(page_data)
                else:
                    self.log_warning(f"No data found on page {page_count}. It might be the end.")

                # Find the 'Next' button to check for more pages
                next_button = soup.select_one('a.btn.btn-default[href*="lbtnNext"]')
                if not next_button:
                    self.log_success("Reached the last page. No 'Next' button found.")
                    break

                # Get hidden form fields required for the POST request (pagination)
                viewstate = soup.find('input', {'name': '__VIEWSTATE'})
                viewstategenerator = soup.find('input', {'name': '__VIEWSTATEGENERATOR'})
                eventvalidation = soup.find('input', {'name': '__EVENTVALIDATION'})

                if not all([viewstate, eventvalidation]):
                    self.log_error("Could not find __VIEWSTATE or __EVENTVALIDATION form fields to paginate.")
                    break

                payload = {
                    '__EVENTTARGET': 'ctl00$ContentPlaceHolder1$lbtnNext',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': viewstate['value'],
                    '__VIEWSTATEGENERATOR': viewstategenerator['value'] if viewstategenerator else '',
                    '__EVENTVALIDATION': eventvalidation['value'],
                    'ctl00$ContentPlaceHolder1$txtSharePrice': '500', # Default value seems required
                    'ctl00$ContentPlaceHolder1$txtQuantity': '1000' # Default value seems required
                }

                # Make POST request to get the next page
                try:
                    next_page_response = self.session.post(url, data=payload, timeout=30)
                    next_page_response.raise_for_status()
                    soup = BeautifulSoup(next_page_response.content, 'lxml')
                    page_count += 1
                except Exception as e:
                    self.log_error(f"Failed to fetch next page: {e}")
                    break

            if not all_floorsheet_data:
                self.log_error("No floorsheet data could be extracted from any page.")
                return None

            # Final validation on the complete dataset
            validation = self.validate_data(all_floorsheet_data, ['stock_symbol', 'quantity', 'rate'], min_records=100)
            if not validation['valid']:
                self.log_warning(f"Data validation failed: {validation['errors']} {validation['warnings']}")
            
            self.log_success(f"Scraped a total of {len(all_floorsheet_data)} records from {page_count} pages.")
            return all_floorsheet_data
            
        except Exception as e:
            self.log_error(f"An unexpected error occurred during floorsheet scraping: {e}")
            return None

    def _extract_floorsheet_table(self, soup: BeautifulSoup, date: str) -> List[Dict]:
        """Extracts floorsheet data from a single HTML table soup."""
        table = soup.select_one('table.table-striped')
        if not table:
            self.log_warning("Could not find the floorsheet table (table.table-striped) on the current page.")
            return []

        floorsheet_data = []
        table_tag = cast(Tag, table)
        rows = table_tag.find('tbody').find_all('tr') if table_tag.find('tbody') else []

        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 7:
                continue
            
            try:
                rate = clean_numeric_value(cols[5].get_text(strip=True))
                quantity = clean_numeric_value(cols[4].get_text(strip=True))
                amount = clean_numeric_value(cols[6].get_text(strip=True))
                
                # Calculate amount if missing, which is common
                if not amount and quantity and rate:
                    amount = quantity * rate

                # Safely clean and convert values that should be integers
                transaction_no_val = clean_numeric_value(cols[0].get_text(strip=True))
                buyer_broker_val = clean_numeric_value(cols[2].get_text(strip=True))
                seller_broker_val = clean_numeric_value(cols[3].get_text(strip=True))

                # Skip row if essential integer identifiers are missing
                if transaction_no_val is None or buyer_broker_val is None or seller_broker_val is None:
                    self.log_warning(f"Skipping row with missing transaction/broker ID: {[c.get_text(strip=True) for c in cols]}")
                    continue

                floorsheet_info = {
                    'transaction_no': int(transaction_no_val),
                    'stock_symbol': cols[1].get_text(strip=True),
                    'buyer_broker': int(buyer_broker_val),
                    'seller_broker': int(seller_broker_val),
                    'quantity': quantity,
                    'rate': rate,
                    'amount': amount,
                    'date': date,
                    'source': 'merolagani'
                }
                floorsheet_data.append(floorsheet_info)
            except (ValueError, TypeError, IndexError) as e:
                self.log_warning(f"Skipping a row due to parsing error: {e} | Row: {cols}")
                continue
        
        return floorsheet_data
    
    def save_floorsheet_data(self, data: List[Dict], date: Optional[str] = None) -> Dict[str, bool]:
        """Save floorsheet data to daily and historical files."""
        if not data:
            self.log_error("No data provided to save.")
            return {'daily_saved': False, 'historical_updated': False}
        return self.save_with_history(data, "floorsheet", date)
    
    def run_daily_collection(self) -> Dict:
        """Runs the complete daily floorsheet collection process."""
        self.logger.info("🚀 Starting daily floorsheet collection run.")
        result = {
            'scraper': 'floorsheet',
            'date': datetime.now().strftime('%Y-%m-%d'),
            'status': 'failed',
            'records': 0,
            'file_path': None,
            'errors': []
        }
        
        try:
            floorsheet_data = self.scrape_floorsheet()
            if floorsheet_data:
                save_results = self.save_floorsheet_data(floorsheet_data)
                if save_results['daily_saved']:
                    result.update({
                        'status': 'success',
                        'records': len(floorsheet_data),
                        'file_path': create_data_filepath("floorsheet"),
                    })
                    self.log_success(f"Collection complete: {result['records']} records saved.")
                    if save_results['historical_updated']:
                        self.log_success("Historical data was also updated.")
                else:
                    result['errors'].append("Failed to save daily data.")
            else:
                result['errors'].append("Scraping returned no data.")
        
        except Exception as e:
            error_msg = f"Daily collection run failed unexpectedly: {e}"
            self.log_error(error_msg)
            result['errors'].append(error_msg)
        
        self.close_session()
        return result

def main():
    """Main execution function to test the scraper."""
    scraper = ProductionFloorsheetScraper()
    result = scraper.run_daily_collection()
    
    print("\n📊 FLOORSHEET SCRAPER RESULTS")
    print("=" * 35)
    print(f"Status: {result['status']}")
    print(f"Records: {result['records']}")
    if result.get('file_path'):
        print(f"File: {result['file_path']}")
    if result.get('errors'):
        print(f"Errors: {result['errors']}")

if __name__ == "__main__":
    main()

