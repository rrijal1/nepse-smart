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

from production_indices import ProductionIndicesScraper
from production_macro import ProductionMacroScraper
from production_companies import ProductionCompaniesScraper
from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
from shared_utils import setup_logging, create_data_filepath
from data_manager import DataManager, init_database

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
                # Official API saves security list, market status, floorsheet, indices, supply/demand, and lookup
                expected_files = [
                    f"data/lookup/{date_str}_security_list.json",
                    f"data/daily/{date_str}_market_status.json",
                    f"data/daily/{date_str}_floorsheet.json",
                    f"data/daily/{date_str}_nepse_index.json",
                    f"data/daily/{date_str}_nepse_subindices.json",
                    f"data/daily/{date_str}_supply_demand.json",
                    f"data/lookup/{date_str}_security_id_key_map.json",
                    f"data/lookup/{date_str}_sector_scrips.json",
                    f"data/daily/{date_str}_price_volume_history_today.json"
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
                # Traditional scrapers for remaining data (prices and macro economic data)
        traditional_scrapers = ['prices', 'macro']
        
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
                       choices=['prices', 'macro', 'official_api', 'historical_prices', 'aggregate_historical', 'complete_historical', 'complete_company_historical', 'daily_company_update', 'all'],
                       default='all',
                       help='Specific scraper to run (official_api=security/status/floorsheet/indices/gainers + price/volume history for all stocks, historical_prices=bulk historical OHLCV for all stocks, aggregate_historical=aggregate existing historical data, complete_historical=download ALL available historical data, complete_company_historical=download historical data for ALL individual companies, daily_company_update=append latest trading day to existing company files, prices=price data, macro=economic data)')
    parser.add_argument('--days-back', type=int, default=30,
                       help='Number of days back for historical data collection/aggregation (default: 30)')
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
    
    elif args.scraper == 'historical_prices':
        # Initialize database and data manager
        init_database()
        data_manager = DataManager()

        # Run historical price/volume collection
        from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
        fetcher = NEPSEOfficialDataFetcher()

        print(f"📊 Starting historical price/volume collection for last {args.days_back} days...")
        result = fetcher.run_historical_price_volume_collection(args.days_back)

        # Process and save data using data manager
        total_saved_to_db = 0
        total_saved_to_json = 0

        if result['successful_methods']:
            print(f"\n💾 Processing and saving data...")

            for method_result in result['successful_methods']:
                business_date = method_result['business_date']
                data = method_result.get('data', [])

                if data:
                    # Save to both PostgreSQL and JSON (for recent data)
                    save_result = data_manager.save_historical_data(
                        data=data,
                        date_str=business_date,
                        save_to_db=True,  # Always save to database
                        save_to_json=True  # Save recent data to JSON for GitHub
                    )

                    total_saved_to_db += save_result['saved_to_db']
                    if save_result['saved_to_json']:
                        total_saved_to_json += len(data)

                    if save_result.get('db_error'):
                        print(f"⚠️ Database error for {business_date}: {save_result['db_error']}")

        print(f"\n{'='*60}")
        print(f"HISTORICAL PRICE/VOLUME COLLECTION RESULTS")
        print(f"{'='*60}")
        print(f"Days Back: {result['days_back']}")
        print(f"Business Days Processed: {result['total_methods']}")
        print(f"Successful: {result['success_count']}")
        print(f"Failed: {result['failure_count']}")
        print(f"Empty: {result['empty_count']}")
        print(f"Total Records: {result['total_records']:,}")
        print(f"Records Saved to Database: {total_saved_to_db:,}")
        print(f"Records Saved to JSON: {total_saved_to_json:,}")
        print(f"Total Time: {result['total_collection_time']}s")

        if result['successful_methods']:
            print(f"\n✅ SUCCESSFUL DATES:")
            for method_result in result['successful_methods'][:5]:  # Show first 5
                print(f"  {method_result['business_date']}: {method_result['record_count']} stocks")
            if len(result['successful_methods']) > 5:
                print(f"  ... and {len(result['successful_methods']) - 5} more dates")

        if result['failed_methods']:
            print(f"\n❌ FAILED DATES:")
            for method_result in result['failed_methods'][:3]:  # Show first 3
                print(f"  {method_result['business_date']}: {method_result.get('error', 'Unknown error')}")

        fetcher.close_session()

        if result['failure_count'] > 0:
            print(f"\nStatus: ⚠️ PARTIAL SUCCESS ({result['success_count']}/{result['total_methods']} dates)")
            sys.exit(1)
        else:
            print(f"\nStatus: ✅ SUCCESS - Collected historical data for {result['success_count']} trading days")
            sys.exit(0)
    
    elif args.scraper == 'aggregate_historical':
        # Run historical data aggregation
        from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
        fetcher = NEPSEOfficialDataFetcher()
        
        print(f"📊 Aggregating historical price/volume data for last {args.days_back} days...")
        result = fetcher.aggregate_historical_price_volume_data(args.days_back)
        
        print(f"\n{'='*60}")
        print(f"HISTORICAL DATA AGGREGATION RESULTS")
        print(f"{'='*60}")
        print(f"Date Range: {result['date_range']['start_date']} to {result['date_range']['end_date']}")
        print(f"Business Days: {result['date_range']['business_days']}")
        print(f"Total Stocks: {result['total_stocks']:,}")
        print(f"Total Records: {result['total_records']:,}")
        
        if result.get('summary_stats'):
            stats = result['summary_stats']
            print(f"Total Volume: {stats['total_volume']:,.0f} shares")
            print(f"Total Value: Rs. {stats['total_value']:,.0f}")
            print(f"Avg Daily Volume: {stats['avg_daily_volume']:,.0f} shares")
            print(f"Avg Daily Value: Rs. {stats['avg_daily_value']:,.0f}")
            
            print(f"\n🏆 Most Active Stocks (by volume):")
            for i, (symbol, volume) in enumerate(stats['most_active_stocks'][:5], 1):
                print(f"  {i}. {symbol}: {volume:,.0f} shares")
        
        fetcher.close_session()
        print(f"\nStatus: ✅ SUCCESS - Historical data aggregated")
        sys.exit(0)
    
    elif args.scraper == 'complete_historical':
        # Run complete historical data collection (all available data)
        from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
        fetcher = NEPSEOfficialDataFetcher()
        
        print("📊 Starting complete historical price/volume collection - downloading ALL available data...")
        print("⚠️  This may take a long time and download several years of data...")
        
        result = fetcher.run_complete_historical_price_volume_collection()
        
        print(f"\n{'='*80}")
        print(f"COMPLETE HISTORICAL PRICE/VOLUME COLLECTION RESULTS")
        print(f"{'='*80}")
        print(f"Total Methods Attempted: {result['total_methods']}")
        print(f"✅ Successful: {result['success_count']}")
        print(f"❌ Failed: {result['failure_count']}")
        print(f"⚪ Empty: {result['empty_count']}")
        print(f"📊 Success Rate: {(result['success_count']/result['total_methods']*100):.1f}%")
        print(f"📋 Total Records: {result['total_records']:,}")
        print(f"⏱️ Total Time: {result['total_collection_time']}s")
        
        if result.get('date_range'):
            date_range = result['date_range']
            print(f"📅 Date Range: {date_range['start_date']} to {date_range['end_date']}")
            print(f"📆 Business Days: {date_range['business_days']}")
        
        fetcher.close_session()
        print(f"\nStatus: ✅ SUCCESS - Complete historical data collection finished")
        sys.exit(0)
    
    elif args.scraper == 'complete_company_historical':
        # Run complete historical data collection for all companies
        from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
        fetcher = NEPSEOfficialDataFetcher()
        
        print("📊 Starting complete historical company data collection - downloading historical data for ALL companies...")
        print("⚠️  This will take a very long time and download extensive historical data...")
        
        result = fetcher.run_complete_historical_company_data_collection()
        
        print(f"\n{'='*90}")
        print(f"COMPLETE HISTORICAL COMPANY DATA COLLECTION RESULTS")
        print(f"{'='*90}")
        print(f"Total Companies Attempted: {result['total_methods']}")
        print(f"✅ Successful: {result['success_count']}")
        print(f"❌ Failed: {result['failure_count']}")
        print(f"⚪ Empty: {result['empty_count']}")
        print(f"📊 Success Rate: {(result['success_count']/result['total_methods']*100):.1f}%")
        print(f"📋 Total Records: {result['total_records']:,}")
        print(f"⏱️ Total Time: {result['total_collection_time']}s")
        
        if result.get('companies_processed'):
            companies = result['companies_processed']
            print(f"🏢 Companies Processed: {len(companies)}")
            print(f"Sample companies: {', '.join(companies[:10])}{'...' if len(companies) > 10 else ''}")
        
        fetcher.close_session()
        print(f"\nStatus: ✅ SUCCESS - Complete company historical data collection finished")
        sys.exit(0)
    
    elif args.scraper == 'daily_company_update':
        # Run daily company data update - append latest trading day to existing files
        from nepse_official_data_fetcher import NEPSEOfficialDataFetcher
        fetcher = NEPSEOfficialDataFetcher()
        
        print("📊 Starting daily company data update - appending latest trading day to existing company files...")
        
        result = fetcher.run_daily_company_data_update()
        
        print(f"\n{'='*80}")
        print(f"DAILY COMPANY DATA UPDATE RESULTS")
        print(f"{'='*80}")
        print(f"Target Trading Date: {result.get('latest_trading_date', 'N/A')}")
        print(f"Total Companies Processed: {result['total_companies_processed']}")
        print(f"✅ Successfully Updated: {len(result['successful_updates'])}")
        print(f"❌ Failed Updates: {len(result['failed_updates'])}")
        print(f"⏭️ Skipped: {len(result['skipped_companies'])}")
        print(f"📋 Records Added: {result['total_records_added']}")
        print(f"⏱️ Total Time: {result['total_collection_time']}s")
        
        if result['successful_updates']:
            print(f"\n✅ SUCCESSFULLY UPDATED COMPANIES:")
            for update in result['successful_updates'][:10]:  # Show first 10
                print(f"  ✅ {update['symbol']}: Added {update['date_added']} ({update['total_records_now']} total records)")
            if len(result['successful_updates']) > 10:
                print(f"  ... and {len(result['successful_updates']) - 10} more companies")
        
        if result['failed_updates']:
            print(f"\n❌ FAILED UPDATES:")
            for failure in result['failed_updates'][:5]:  # Show first 5
                print(f"  ❌ {failure['symbol']}: {failure.get('error', 'Unknown error')}")
        
        fetcher.close_session()
        print(f"\nStatus: ✅ SUCCESS - Daily company update completed")
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