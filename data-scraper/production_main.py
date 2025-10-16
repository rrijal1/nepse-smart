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
            'macro': ProductionMacroScraper
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
            result = scraper.run_daily_collection()
            scraper.close_session()
            
            self.logger.info(f"✅ {scraper_type} completed: {result['status']} ({result.get('records', 0)} records)")
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
        
        scrapers = ['prices', 'floorsheet', 'indices', 'macro']
        results = {}
        
        for scraper_type in scrapers:
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
                       choices=['prices', 'floorsheet', 'indices', 'macro', 'all'],
                       default='all',
                       help='Specific scraper to run (default: all)')
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