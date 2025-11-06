#!/usr/bin/env python3
"""
Cleanup old lookup files
Keeps only the last 7 business days of lookup data (security_list, sector_scrips, security_id_key_map)
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import re

def get_business_days(num_days: int = 7) -> list:
    """Get list of last N business days (excluding weekends)"""
    business_days = []
    current_date = datetime.now()
    days_checked = 0
    
    while len(business_days) < num_days and days_checked < num_days * 2:  # Safety limit
        # Skip Saturday (5) and Sunday (6)
        if current_date.weekday() < 5:
            business_days.append(current_date.strftime('%Y-%m-%d'))
        current_date -= timedelta(days=1)
        days_checked += 1
    
    return business_days

def cleanup_lookup_files(lookup_dir: Path, keep_days: int = 7, dry_run: bool = False):
    """Remove lookup files older than specified business days"""
    if not lookup_dir.exists():
        print(f"Lookup directory not found: {lookup_dir}")
        return
    
    # Get dates to keep
    keep_dates = set(get_business_days(keep_days))
    print(f"📅 Keeping files from these dates: {', '.join(sorted(keep_dates, reverse=True))}")
    
    # Pattern to match lookup files: YYYY-MM-DD_<name>.json
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})_(security_list|sector_scrips|security_id_key_map)\.json$')
    
    files_to_delete = []
    files_to_keep = []
    
    # Scan all files in lookup directory
    for file_path in lookup_dir.glob('*.json'):
        match = pattern.match(file_path.name)
        if match:
            file_date = match.group(1)
            
            if file_date not in keep_dates:
                files_to_delete.append(file_path)
            else:
                files_to_keep.append(file_path)
    
    # Summary
    print(f"\n📊 Cleanup Summary:")
    print(f"   Files to keep: {len(files_to_keep)}")
    print(f"   Files to delete: {len(files_to_delete)}")
    
    if files_to_keep:
        print(f"\n✅ Keeping {len(files_to_keep)} files:")
        for file_path in sorted(files_to_keep):
            file_size = file_path.stat().st_size / 1024  # KB
            print(f"   ✓ {file_path.name} ({file_size:.1f} KB)")
    
    if files_to_delete:
        total_size = sum(f.stat().st_size for f in files_to_delete) / (1024 * 1024)  # MB
        print(f"\n🗑️  Deleting {len(files_to_delete)} old files (freeing {total_size:.2f} MB):")
        
        for file_path in sorted(files_to_delete):
            file_size = file_path.stat().st_size / 1024  # KB
            if dry_run:
                print(f"   [DRY RUN] Would delete: {file_path.name} ({file_size:.1f} KB)")
            else:
                print(f"   ✗ Deleting: {file_path.name} ({file_size:.1f} KB)")
                file_path.unlink()
        
        if not dry_run:
            print(f"\n✅ Cleanup complete! Freed {total_size:.2f} MB")
        else:
            print(f"\n⚠️  DRY RUN - No files were actually deleted")
    else:
        print(f"\n✅ No old files to delete - all files are within the {keep_days} business day retention period")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Cleanup old lookup files')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of business days to keep (default: 7)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be deleted without actually deleting')
    parser.add_argument('--lookup-dir', type=str, default=None,
                       help='Path to lookup directory (default: ../data/lookup)')
    
    args = parser.parse_args()
    
    # Determine lookup directory
    if args.lookup_dir:
        lookup_dir = Path(args.lookup_dir)
    else:
        # Default: relative to script location
        script_dir = Path(__file__).parent
        lookup_dir = script_dir.parent / 'data' / 'lookup'
    
    print(f"🧹 Cleanup Old Lookup Files")
    print(f"   Directory: {lookup_dir}")
    print(f"   Retention: Last {args.days} business days")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()
    
    cleanup_lookup_files(lookup_dir, keep_days=args.days, dry_run=args.dry_run)

if __name__ == "__main__":
    main()
