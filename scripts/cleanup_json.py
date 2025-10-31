#!/usr/bin/env python3
"""
Safe JSON File Cleanup Script for NEPSE Smart
Only removes old JSON files from data/daily/ directory
PostgreSQL data is NEVER touched
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "data-scraper"))

try:
    from backend.data_manager import DataManager
except ImportError:
    try:
        from backend.data_manager import DataManager
    except ImportError:
        print("❌ Could not import DataManager. Make sure you're running from the project root.")
        sys.exit(1)

def main():
    """Main cleanup function"""
    print("🧹 NEPSE Smart - Safe JSON File Cleanup")
    print("=" * 50)

    # Default to 30 days, but allow override
    keep_days = 30
    if len(sys.argv) > 1:
        try:
            keep_days = int(sys.argv[1])
        except ValueError:
            print(f"❌ Invalid number of days: {sys.argv[1]}")
            print("Usage: python cleanup_json.py [days_to_keep]")
            sys.exit(1)

    print(f"📅 Keeping JSON files from last {keep_days} days")
    print("💾 PostgreSQL data will NOT be touched")
    print()

    # Confirm before proceeding
    confirm = input(f"Are you sure you want to delete JSON files older than {keep_days} days? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Cleanup cancelled")
        sys.exit(0)

    try:
        # Initialize data manager
        dm = DataManager()

        # Get summary before cleanup
        before_summary = dm.get_data_summary()
        print("📊 Before cleanup:")
        print(f"   JSON files: {before_summary['json_files_count']}")
        print(f"   Database records: {before_summary['database_records_count']}")
        print()

        # Perform cleanup
        print(f"🗑️  Cleaning up files older than {keep_days} days...")
        result = dm.cleanup_old_data(keep_days)

        print("✅ Cleanup completed!")
        print(f"   Files removed: {result['files_removed']}")
        print(f"   Files kept: {result['files_kept']}")
        print(f"   Cutoff date: {result['cutoff_date']}")

        if result['removed_files']:
            print("   Removed files:")
            for file in result['removed_files'][:5]:  # Show first 5
                print(f"     - {file}")
            if len(result['removed_files']) > 5:
                print(f"     ... and {len(result['removed_files']) - 5} more")

        # Get summary after cleanup
        after_summary = dm.get_data_summary()
        print()
        print("📊 After cleanup:")
        print(f"   JSON files: {after_summary['json_files_count']}")
        print(f"   Database records: {after_summary['database_records_count']} (unchanged)")

    except Exception as e:
        print(f"❌ Error during cleanup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()