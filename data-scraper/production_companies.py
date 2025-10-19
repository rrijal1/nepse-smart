#!/usr/bin/env python3
"""
Production NEPSE Listed Companies Scraper
- Scrapes the list of listed companies from NEPSE
- API-first approach with HTML fallback
- Saves a daily snapshot (no historical aggregation)
- Updated to use the new shared_utils.py ScraperBase
"""

from bs4 import BeautifulSoup, Tag
from typing import List, Dict, Optional, cast
import requests

# Import the new base class and file path utility
from shared_utils import ScraperBase, create_data_filepath


class ProductionCompaniesScraper(ScraperBase):
    """
    Scraper for NEPSE listed companies, inheriting from the robust ScraperBase.
    """

    def __init__(self):
        # The __init__ is now much simpler.
        # super().__init__() handles logger and session creation.
        super().__init__("NEPSE-Companies")
        self.site_base = "https://nepalstock.com.np"
        self.api_candidates = [
            "https://newweb.nepalstock.com.np/api/nots/security?nonDelisted=true",
            "https://nepalstock.com.np/api/nots/security?nonDelisted=true",
        ]

    def _normalize_company(self, item: dict) -> Optional[Dict]:
        """Normalizes company data from various possible dictionary keys."""
        symbol = (
            item.get("symbol")
            or item.get("symbolName")
            or item.get("symbol_code")
            or item.get("scrip")
        )
        name = (
            item.get("companyName")
            or item.get("companyname")
            or item.get("fullName")
            or item.get("name")
        )

        if not symbol:
            return None

        result: Dict = {
            "symbol": str(symbol).strip().upper(),
            "name": str(name).strip() if name else str(symbol).strip().upper(),
        }

        # Optional enrichers
        for key in ["isin", "sectorName", "sector", "id", "instrumentType"]:
            if key in item and item[key] is not None:
                result[key] = item[key]
        return result

    def _fetch_api_companies(self) -> Optional[List[Dict]]:
        """Fetches and processes company data from a list of potential API endpoints."""
        self.session.headers.update({
            "Accept": "application/json, text/plain, */*",
            "Referer": f"{self.site_base}/company",
        })

        for url in self.api_candidates:
            # Use the make_request method from ScraperBase which has built-in retries
            resp = self.make_request(url)
            if not resp:
                continue  # Try the next API candidate

            try:
                data = resp.json()
                if isinstance(data, dict) and "content" in data:
                    data = data.get("content")

                if not isinstance(data, list):
                    self.log_warning(f"API response from {url} was not a list.")
                    continue

                out: List[Dict] = []
                for item in data:
                    if isinstance(item, dict):
                        norm = self._normalize_company(item)
                        if norm:
                            out.append(norm)

                if out:
                    self.log_success(f"Fetched {len(out)} companies from API: {url}")
                    return out
            except requests.exceptions.JSONDecodeError as e:
                self.log_warning(f"Failed to decode JSON from {url}: {e}")
                continue

        return None

    def _parse_html_companies(self) -> Optional[List[Dict]]:
        """Parses company data from the HTML table as a fallback."""
        url = f"{self.site_base}/company"
        # Use the robust make_request from the base class
        resp = self.make_request(url)
        if not resp:
            return None

        try:
            soup = BeautifulSoup(resp.content, "lxml")
            target_table = soup.find("table", {"class": "table-responsive"})

            if not target_table:
                # A more generic fallback if the class name changes
                tables = soup.find_all("table")
                for table in tables:
                    headers = [th.get_text(strip=True).lower() for th in table.find_all("th")]
                    if "symbol" in headers and "company name" in headers:
                        target_table = cast(Tag, table)
                        break

            if not target_table:
                self.log_warning("No matching company table found on the page.")
                return None

            out: List[Dict] = []
            tbody = target_table.find("tbody")
            if not tbody:
                 self.log_warning("Table found but it contains no tbody element.")
                 return None

            for row in tbody.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) < 2:
                    continue
                
                symbol = cols[1].get_text(strip=True) # Symbol is often the second column
                name = cols[0].get_text(strip=True) # Company Name is often the first
                
                if symbol:
                    out.append({
                        "symbol": symbol.upper(),
                        "name": name or symbol.upper(),
                        "source": "html",
                    })

            if out:
                self.log_success(f"Parsed {len(out)} companies from HTML table")
                return out
        except Exception as e:
            self.log_error(f"HTML parsing failed: {e}")

        return None

    def scrape_companies(self) -> Optional[List[Dict]]:
        """Main scraping method: tries API first, then falls back to HTML."""
        self.log_success("Starting company scrape. Trying API first...")
        data = self._fetch_api_companies()
        if data:
            return data
        
        self.log_warning("API fetch failed. Falling back to HTML parsing.")
        return self._parse_html_companies()

    def run_daily_collection(self) -> Dict:
        """Orchestrates the daily scraping and saving process."""
        from datetime import datetime
        result = {
            "scraper": "companies",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "status": "failed",
            "records": 0,
            "file_path": None,
            "errors": [],
        }
        try:
            companies = self.scrape_companies()
            if companies:
                # The data_type here should match the intended filename
                daily_path = create_data_filepath("companies")
                if self.save_data(companies, daily_path):
                    result.update({
                        "status": "success",
                        "records": len(companies),
                        "file_path": daily_path,
                    })
                else:
                    result["errors"].append("Failed to save company list")
            else:
                result["errors"].append("Failed to scrape company list")
        except Exception as e:
            self.log_error(f"Companies collection failed: {e}")
            result["errors"].append(str(e))
        
        self.log_success(f"Scraper finished in {self.get_runtime()}.")
        self.close_session()
        return result


def main():
    """Main execution function"""
    scraper = ProductionCompaniesScraper()
    res = scraper.run_daily_collection()
    print("\n📊 COMPANIES SCRAPER RESULTS")
    print("=" * 30)
    print(f"Status: {res['status']}")
    print(f"Records: {res['records']}")
    if res.get("file_path"):
        print(f"File: {res['file_path']}")
    if res.get("errors"):
        print(f"Errors: {', '.join(res['errors'])}")


if __name__ == "__main__":
    main()
