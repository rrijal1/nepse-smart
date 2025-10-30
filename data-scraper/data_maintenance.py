#!/usr/bin/env python3
"""
Data Maintenance Script for NEPSE Smart
Handles data cleanup, migration, and retention policies
"""

import argparse
import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List

from data_manager import DataManager, init_database

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataMaintenance:
    """Handles data maintenance operations"""

    def __init__(self):
        self.data_manager = DataManager()

    def migrate_existing_data_to_db(self) -> Dict[str, Any]:
        """
        Migrate all existing JSON historical data to PostgreSQL

        Returns:
            Migration summary
        """
        logger.info("🔄 Starting migration of existing JSON data to PostgreSQL...")

        daily_dir = Path("data/daily")
        if not daily_dir.exists():
            return {'error': 'Daily data directory not found'}

        migrated_files = []
        total_records = 0
        errors = []

        # Find all historical price volume files
        json_files = list(daily_dir.glob("*_price_volume_history_*.json"))

        for json_file in json_files:
            try:
                logger.info(f"📁 Processing {json_file.name}...")

                with open(json_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if data:
                    # Extract date from filename
                    date_part = json_file.stem.split('_price_volume_history_')[1]
                    date_str = date_part.replace('_', '-')

                    # Save to database
                    saved_count = self.data_manager.save_to_postgres(data)
                    total_records += saved_count
                    migrated_files.append({
                        'file': json_file.name,
                        'date': date_str,
                        'records': len(data),
                        'saved_to_db': saved_count
                    })

                    logger.info(f"✅ Migrated {json_file.name}: {saved_count} records")

            except Exception as e:
                error_msg = f"Failed to migrate {json_file.name}: {e}"
                logger.error(error_msg)
                errors.append(error_msg)

        return {
            'migrated_files': len(migrated_files),
            'total_records': total_records,
            'errors': errors,
            'file_details': migrated_files
        }

    def cleanup_old_json_files(self, keep_days: int = 30, dry_run: bool = False) -> Dict[str, Any]:
        """
        Remove old JSON files, keeping only recent data

        Args:
            keep_days: Number of days of data to keep
            dry_run: If True, only show what would be deleted

        Returns:
            Cleanup summary
        """
        logger.info(f"🧹 {'DRY RUN: ' if dry_run else ''}Cleaning up old JSON files (keeping {keep_days} days)...")

        result = self.data_manager.cleanup_old_data(keep_days)

        if dry_run:
            logger.info("📋 DRY RUN RESULTS:")
            logger.info(f"   Would remove {result['files_removed']} files")
            logger.info(f"   Would keep {result['files_kept']} files")
            logger.info(f"   Cutoff date: {result['cutoff_date']}")
            if result['removed_files']:
                logger.info("   Files to be removed:")
                for file in result['removed_files'][:5]:
                    logger.info(f"     - {file}")
                if len(result['removed_files']) > 5:
                    logger.info(f"     ... and {len(result['removed_files']) - 5} more")
        else:
            logger.info("✅ CLEANUP RESULTS:")
            logger.info(f"   Removed {result['files_removed']} files")
            logger.info(f"   Kept {result['files_kept']} files")
            logger.info(f"   Cutoff date: {result['cutoff_date']}")

        return result

    def verify_data_integrity(self) -> Dict[str, Any]:
        """
        Verify data integrity between JSON files and database

        Returns:
            Integrity check results
        """
        logger.info("🔍 Verifying data integrity...")

        summary = self.data_manager.get_data_summary()

        # Check for any inconsistencies
        issues = []

        if summary['json_files_count'] == 0 and summary['database_records_count'] == 0:
            issues.append("No data found in either JSON files or database")

        # Check date ranges
        date_range = summary.get('date_range', {})
        if date_range.get('oldest') and date_range.get('newest'):
            oldest_date = datetime.strptime(date_range['oldest'], '%Y-%m-%d')
            newest_date = datetime.strptime(date_range['newest'], '%Y-%m-%d')
            days_span = (newest_date - oldest_date).days

            if days_span > 365:  # More than a year of data in JSON
                issues.append(f"Large date range in JSON files: {days_span} days (consider cleanup)")

        return {
            'summary': summary,
            'issues': issues,
            'integrity_status': 'good' if not issues else 'issues_found'
        }

    def run_full_maintenance(self, keep_days: int = 30, dry_run: bool = False) -> Dict[str, Any]:
        """
        Run complete maintenance cycle:
        1. Migrate existing data to DB
        2. Clean up old JSON files
        3. Verify integrity

        Args:
            keep_days: Days of JSON data to keep
            dry_run: Preview changes without executing

        Returns:
            Complete maintenance results
        """
        logger.info("🔧 Starting full data maintenance cycle...")

        results = {
            'timestamp': datetime.now().isoformat(),
            'operations': {}
        }

        # 1. Migrate existing data
        logger.info("Step 1: Migrating existing data to PostgreSQL...")
        migration_result = self.migrate_existing_data_to_db()
        results['operations']['migration'] = migration_result

        # 2. Clean up old files
        logger.info("Step 2: Cleaning up old JSON files...")
        cleanup_result = self.cleanup_old_json_files(keep_days, dry_run)
        results['operations']['cleanup'] = cleanup_result

        # 3. Verify integrity
        logger.info("Step 3: Verifying data integrity...")
        integrity_result = self.verify_data_integrity()
        results['operations']['integrity'] = integrity_result

        # Summary
        total_migrated = migration_result.get('total_records', 0)
        files_cleaned = cleanup_result.get('files_removed', 0)
        issues_found = len(integrity_result.get('issues', []))

        results['summary'] = {
            'records_migrated': total_migrated,
            'files_cleaned': files_cleaned,
            'issues_found': issues_found,
            'status': 'success' if issues_found == 0 else 'completed_with_issues'
        }

        logger.info("🎯 MAINTENANCE COMPLETE")
        logger.info(f"   Records migrated: {total_migrated}")
        logger.info(f"   Files cleaned: {files_cleaned}")
        logger.info(f"   Issues found: {issues_found}")

        return results

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='NEPSE Data Maintenance')
    parser.add_argument('operation',
                       choices=['migrate', 'cleanup', 'verify', 'full'],
                       help='Maintenance operation to perform')
    parser.add_argument('--keep-days', type=int, default=30,
                       help='Days of JSON data to keep during cleanup (default: 30)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Preview changes without executing (for cleanup and full operations)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize database
    init_database()

    # Create maintenance instance
    maintenance = DataMaintenance()

    try:
        if args.operation == 'migrate':
            result = maintenance.migrate_existing_data_to_db()

            print(f"\n{'='*50}")
            print("DATA MIGRATION RESULTS")
            print(f"{'='*50}")
            print(f"Files Migrated: {result['migrated_files']}")
            print(f"Total Records: {result['total_records']:,}")

            if result['errors']:
                print(f"Errors: {len(result['errors'])}")
                for error in result['errors'][:3]:
                    print(f"  - {error}")

            print(f"\nStatus: ✅ SUCCESS")

        elif args.operation == 'cleanup':
            result = maintenance.cleanup_old_json_files(args.keep_days, args.dry_run)

            print(f"\n{'='*50}")
            print(f"{'DRY RUN - ' if args.dry_run else ''}DATA CLEANUP RESULTS")
            print(f"{'='*50}")
            print(f"Files {'to be ' if args.dry_run else ''}Removed: {result['files_removed']}")
            print(f"Files Kept: {result['files_kept']}")
            print(f"Cutoff Date: {result['cutoff_date']}")

            if result['removed_files']:
                print(f"\n{'Would remove' if args.dry_run else 'Removed'} files:")
                for file in result['removed_files'][:10]:
                    print(f"  - {file}")
                if len(result['removed_files']) > 10:
                    print(f"  ... and {len(result['removed_files']) - 10} more")

            print(f"\nStatus: ✅ SUCCESS")

        elif args.operation == 'verify':
            result = maintenance.verify_data_integrity()

            print(f"\n{'='*50}")
            print("DATA INTEGRITY CHECK")
            print(f"{'='*50}")
            print(f"JSON Files: {result['summary']['json_files_count']}")
            print(f"Database Records: {result['summary']['database_records_count']:,}")
            print(f"Total Storage: {result['summary']['total_storage']:,} bytes")

            if result['summary'].get('date_range'):
                dr = result['summary']['date_range']
                print(f"Date Range: {dr.get('oldest', 'N/A')} to {dr.get('newest', 'N/A')}")

            if result['issues']:
                print(f"\n⚠️ ISSUES FOUND:")
                for issue in result['issues']:
                    print(f"  - {issue}")
                print(f"\nStatus: ⚠️ ISSUES DETECTED")
            else:
                print(f"\nStatus: ✅ INTEGRITY GOOD")

        elif args.operation == 'full':
            result = maintenance.run_full_maintenance(args.keep_days, args.dry_run)

            print(f"\n{'='*70}")
            print(f"{'DRY RUN - ' if args.dry_run else ''}FULL MAINTENANCE RESULTS")
            print(f"{'='*70}")
            print(f"Records Migrated: {result['summary']['records_migrated']:,}")
            print(f"Files Cleaned: {result['summary']['files_cleaned']}")
            print(f"Issues Found: {result['summary']['issues_found']}")
            print(f"Status: {result['summary']['status']}")

            # Show operation details
            for op_name, op_result in result['operations'].items():
                print(f"\n{op_name.upper()}:")
                if op_name == 'migration':
                    print(f"  Files: {op_result['migrated_files']}")
                    print(f"  Records: {op_result['total_records']:,}")
                elif op_name == 'cleanup':
                    print(f"  Removed: {op_result['files_removed']}")
                    print(f"  Kept: {op_result['files_kept']}")
                elif op_name == 'integrity':
                    print(f"  Status: {op_result['integrity_status']}")

    except Exception as e:
        logger.error(f"❌ Maintenance failed: {e}")
        print(f"\n❌ ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main()