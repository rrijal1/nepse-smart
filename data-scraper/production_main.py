#!/usr/bin/env python3
"""
Production NEPSE Data Collection Orchestrator
- Coordinates all data scrapers
- Parallel execution support
- Comprehensive error handling and reporting
- Used by GitHub Actions for automated data collection
"""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import argparse

from production_prices import ProductionPricesScraper
from production_floorsheet import ProductionFloorsheetScraper
from production_indices import ProductionIndicesScraper
from production_macro import ProductionMacroScraper
from production_companies import ProductionCompaniesScraper
from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
from shared_utils import setup_logging, create_data_filepath

class ProductionOrchestrator:
    """Main orchestrator for NEPSE data collection"""
    
    def __init__(self):
        self.logger = setup_logging("NEPSE-Orchestrator")
        self.results = {}
        self.start_time = datetime.now()
    
    def run_single_scraper(self, scraper_type: str) -> Dict:
        """Run a single scraper type"""
        self.logger.info(f"🚀 Running {scraper_type} scraper...")
        
        scrapers = {
            'prices': ProductionPricesScraper,
            'floorsheet': ProductionFloorsheetScraper, 
            'indices': ProductionIndicesScraper,
            'macro': ProductionMacroScraper,
            'companies': ProductionCompaniesScraper,
            'official_api': NEPSEOfficialDataFetcher,
        }
        
        if scraper_type not in scrapers:
            error_msg = f"Unknown scraper type: {scraper_type}"
            self.logger.error(error_msg)
            return {
                'scraper': scraper_type,
                'status': 'failed',
                'error': error_msg
            }
        
        try:
            scraper = scrapers[scraper_type]()
            
            # Handle different result formats
            if scraper_type == 'official_api':
                result = scraper.run_core_collection()
                # Convert official API result format to standard format
                date_str = datetime.now().strftime('%Y-%m-%d')
                # Official API saves only company list and market status
                expected_files = [
                    f"data/daily/{date_str}_company_list.json",
                    f"data/daily/{date_str}_market_status.json"
                ]
                result = {
                    'scraper': 'official_api',
                    'status': 'success' if result['success_count'] > 0 else 'failed',
                    'records': result.get('total_records', 0),
                    'file_path': expected_files[0],  # Use first file for compatibility
                    'file_paths': expected_files,    # List all expected files
                    'errors': [r.get('error', '') for r in result.get('failed_methods', [])],
                    'method_results': result
                }
            else:
                result = scraper.run_daily_collection()
            
            scraper.close_session()
            
            self.logger.info(f"✅ {scraper_type} completed: {result['status']} ({result.get('records', 0)} records)")
            
            # Debug: Check if files were actually created
            if result['status'] == 'success':
                import os
                if scraper_type == 'official_api' and result.get('file_paths'):
                    # Check multiple files for official API
                    files_found = 0
                    total_size = 0
                    for file_path in result['file_paths']:
                        if os.path.exists(file_path):
                            file_size = os.path.getsize(file_path)
                            total_size += file_size
                            files_found += 1
                            self.logger.info(f"📁 File created: {file_path} ({file_size} bytes)")
                        else:
                            self.logger.warning(f"⚠️ Expected file not found: {file_path}")
                    self.logger.info(f"📊 Official API: {files_found}/{len(result['file_paths'])} files created ({total_size} total bytes)")
                elif result.get('file_path'):
                    # Check single file for other scrapers
                    if os.path.exists(result['file_path']):
                        file_size = os.path.getsize(result['file_path'])
                        self.logger.info(f"📁 File created: {result['file_path']} ({file_size} bytes)")
                    else:
                        self.logger.error(f"❌ Expected file not found: {result['file_path']}")
            
            return result
            
        except Exception as e:
            error_msg = f"Failed to run {scraper_type} scraper: {e}"
            self.logger.error(error_msg)
            return {
                'scraper': scraper_type,
                'status': 'failed',
                'error': error_msg
            }
    
    def run_all_scrapers(self) -> Dict[str, Dict]:
        """Run all scrapers sequentially"""
        self.logger.info("🔄 Starting complete NEPSE data collection...")
        
        # Official API for authenticated data (company_list, market_status only)
        official_scrapers = ['official_api']
        # Traditional scrapers for other data types (including floorsheet from MeroLagani)
        traditional_scrapers = ['floorsheet', 'indices', 'macro']
        
        results = {}
        
        # Run official API first for core data
        for scraper_type in official_scrapers:
            result = self.run_single_scraper(scraper_type)
            results[scraper_type] = result
            
            if result['status'] == 'success':
                self.logger.info(f"✅ {scraper_type}: {result.get('records', 0)} records")
            else:
                self.logger.error(f"❌ {scraper_type}: {result.get('error', 'Unknown error')}")
        
        # Run traditional scrapers for remaining data
        for scraper_type in traditional_scrapers:
            result = self.run_single_scraper(scraper_type)
            results[scraper_type] = result
            
            # Log progress
            if result['status'] == 'success':
                self.logger.info(f"✅ {scraper_type}: {result.get('records', 0)} records")
            else:
                self.logger.error(f"❌ {scraper_type}: {result.get('error', 'Unknown error')}")
        
        return results
    
    def generate_summary_report(self, results: Dict[str, Dict]) -> Dict:
        """Generate comprehensive summary report"""
        total_records = sum(r.get('records', 0) for r in results.values())
        successful_scrapers = [k for k, v in results.items() if v['status'] == 'success']
        failed_scrapers = [k for k, v in results.items() if v['status'] == 'failed']
        
        runtime = datetime.now() - self.start_time
        
        summary = {
            'collection_date': datetime.now().strftime('%Y-%m-%d'),
            'collection_time': datetime.now().isoformat(),
            'runtime_seconds': runtime.total_seconds(),
            'total_records': total_records,
            'scrapers': {
                'total': len(results),
                'successful': len(successful_scrapers),
                'failed': len(failed_scrapers)
            },
            'successful_scrapers': successful_scrapers,
            'failed_scrapers': failed_scrapers,
            'detailed_results': results
        }
        
        # Log summary
        self.logger.info(f"📊 COLLECTION SUMMARY")
        self.logger.info(f"   Total Records: {total_records}")
        self.logger.info(f"   Successful: {len(successful_scrapers)}/{len(results)}")
        self.logger.info(f"   Runtime: {runtime}")
        
        if failed_scrapers:
            self.logger.warning(f"   Failed scrapers: {failed_scrapers}")
        
        return summary
    
    def save_summary_report(self, summary: Dict) -> bool:
        """Save summary report to file"""
        try:
            # Save to data directory
            filepath = create_data_filepath("collection_summary")
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(summary, f, indent=2, default=str, ensure_ascii=False)
            
            self.logger.info(f"✅ Summary report saved: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to save summary report: {e}")
            return False
    
    def run_complete_collection(self) -> Dict:
        """Run complete data collection with reporting"""
        self.logger.info("🎯 Starting complete NEPSE data collection...")
        
        # Run all scrapers
        results = self.run_all_scrapers()
        
        # Generate and save summary
        summary = self.generate_summary_report(results)
        self.save_summary_report(summary)
        
        # Exit with appropriate code for CI/CD
        if summary['scrapers']['failed'] > 0:
            self.logger.warning("⚠️ Some scrapers failed - check logs for details")
            return summary
        else:
            self.logger.info("🎉 All scrapers completed successfully!")
            return summary

def main():
    """Main entry point for the production orchestrator"""
    parser = argparse.ArgumentParser(description='NEPSE Production Data Scraper')
    parser.add_argument('--scraper', 
                       choices=['floorsheet', 'indices', 'macro', 'official_api', 'all'],
                       default='all',
                       help='Specific scraper to run (official_api=company/status, floorsheet=transaction data, indices=market indices, macro=economic data)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    
    args = parser.parse_args()
    
    orchestrator = ProductionOrchestrator()
    
    if args.scraper == 'all':
        summary = orchestrator.run_complete_collection()
        
        # Print final status for GitHub Actions
        print(f"\n{'='*50}")
        print(f"NEPSE DATA COLLECTION COMPLETED")
        print(f"{'='*50}")
        print(f"Date: {summary['collection_date']}")
        print(f"Total Records: {summary['total_records']}")
        print(f"Successful: {summary['scrapers']['successful']}/{summary['scrapers']['total']}")
        print(f"Runtime: {summary['runtime_seconds']:.1f}s")
        
        if summary['failed_scrapers']:
            print(f"Failed: {summary['failed_scrapers']}")
            sys.exit(1)  # Exit with error for CI/CD
        else:
            print("Status: ✅ SUCCESS")
            sys.exit(0)
    
    else:
        # Run single scraper
        result = orchestrator.run_single_scraper(args.scraper)
        
        print(f"\n{'='*40}")
        print(f"{args.scraper.upper()} SCRAPER RESULT")
        print(f"{'='*40}")
        print(f"Status: {result['status']}")
        print(f"Records: {result.get('records', 0)}")
        if result.get('file_path'):
            print(f"File: {result['file_path']}")
        if result.get('error'):
            print(f"Error: {result['error']}")
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    main()