#!/usr/bin/env python3
"""
Cleanup and Archive Old Data Files
Moves old data files to archive directory while keeping last 7 business days active
"""

import os
import sys
from pathlib import Path
from datetime import datetime, timedelta
import re
import shutil

def get_business_days(num_days: int = 7) -> list:
    """Get list of last N business days (excluding weekends)"""
    business_days = []
    current_date = datetime.now()
    days_checked = 0
    
    while len(business_days) < num_days and days_checked < num_days * 2:
        if current_date.weekday() < 5:  # Skip Saturday (5) and Sunday (6)
            business_days.append(current_date.strftime('%Y-%m-%d'))
        current_date -= timedelta(days=1)
        days_checked += 1
    
    return business_days

def get_year_month_from_date(date_str: str) -> tuple:
    """Extract year and month from date string"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.year, date_obj.month
    except ValueError:
        return None, None

def archive_old_files(data_dir: Path, keep_days: int = 7, dry_run: bool = False):
    """Archive old data files to archive directory"""
    
    if not data_dir.exists():
        print(f"❌ Data directory not found: {data_dir}")
        return
    
    # Get dates to keep active
    keep_dates = set(get_business_days(keep_days))
    print(f"📅 Keeping active files from: {', '.join(sorted(keep_dates, reverse=True))}")
    
    # Pattern to match data files: YYYY-MM-DD_<name>.json
    pattern = re.compile(r'^(\d{4}-\d{2}-\d{2})_(.+)\.json$')
    
    # Create archive base directory
    archive_base = data_dir.parent / 'archive'
    
    stats = {
        'kept': 0,
        'archived': 0,
        'failed': 0,
        'total_size_archived': 0
    }
    
    # Process daily and lookup directories
    for subdir_name in ['daily', 'lookup']:
        subdir = data_dir / subdir_name
        
        if not subdir.exists():
            print(f"⚠️  Directory not found: {subdir}")
            continue
        
        print(f"\n📂 Processing {subdir_name}/ directory...")
        
        for file_path in subdir.glob('*.json'):
            match = pattern.match(file_path.name)
            
            if not match:
                print(f"  ⚠️  Skipping non-matching file: {file_path.name}")
                continue
            
            file_date = match.group(1)
            file_type = match.group(2)
            
            if file_date in keep_dates:
                # Keep this file active
                stats['kept'] += 1
                file_size = file_path.stat().st_size / 1024  # KB
                print(f"  ✓ Keeping: {file_path.name} ({file_size:.1f} KB)")
            else:
                # Archive this file
                year, month = get_year_month_from_date(file_date)
                
                if year is None or month is None:
                    print(f"  ❌ Invalid date format: {file_path.name}")
                    stats['failed'] += 1
                    continue
                
                # Create archive directory structure: archive/YYYY/MM/daily or lookup
                archive_dir = archive_base / str(year) / f"{month:02d}" / subdir_name
                
                if not dry_run:
                    archive_dir.mkdir(parents=True, exist_ok=True)
                
                archive_path = archive_dir / file_path.name
                file_size = file_path.stat().st_size
                file_size_kb = file_size / 1024
                
                if dry_run:
                    print(f"  [DRY RUN] Would archive: {file_path.name} → {archive_path.relative_to(data_dir.parent)} ({file_size_kb:.1f} KB)")
                else:
                    try:
                        shutil.move(str(file_path), str(archive_path))
                        print(f"  📦 Archived: {file_path.name} → {archive_path.relative_to(data_dir.parent)} ({file_size_kb:.1f} KB)")
                        stats['archived'] += 1
                        stats['total_size_archived'] += file_size
                    except Exception as e:
                        print(f"  ❌ Failed to archive {file_path.name}: {e}")
                        stats['failed'] += 1
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"📊 Archive Summary:")
    print(f"   Active files kept: {stats['kept']}")
    print(f"   Files archived: {stats['archived']}")
    print(f"   Failed: {stats['failed']}")
    
    if stats['archived'] > 0:
        total_mb = stats['total_size_archived'] / (1024 * 1024)
        print(f"   Space moved to archive: {total_mb:.2f} MB")
        print(f"   Archive location: {archive_base}")
    
    if dry_run:
        print(f"\n⚠️  DRY RUN - No files were actually moved")
    else:
        print(f"\n✅ Cleanup complete!")

def list_archive_structure(archive_dir: Path):
    """Show the archive directory structure"""
    if not archive_dir.exists():
        print(f"Archive directory doesn't exist yet: {archive_dir}")
        return
    
    print(f"\n📁 Archive Structure:")
    print(f"   {archive_dir}/")
    
    # List years
    years = sorted([d for d in archive_dir.iterdir() if d.is_dir()], reverse=True)
    
    for year_dir in years:
        print(f"   ├── {year_dir.name}/")
        
        # List months in year
        months = sorted([d for d in year_dir.iterdir() if d.is_dir()], reverse=True)
        
        for month_dir in months:
            month_name = datetime.strptime(month_dir.name, '%m').strftime('%B')
            print(f"   │   ├── {month_dir.name}/ ({month_name})")
            
            # Count files in daily and lookup
            for subdir in ['daily', 'lookup']:
                subdir_path = month_dir / subdir
                if subdir_path.exists():
                    file_count = len(list(subdir_path.glob('*.json')))
                    total_size = sum(f.stat().st_size for f in subdir_path.glob('*.json'))
                    size_mb = total_size / (1024 * 1024)
                    print(f"   │   │   ├── {subdir}/ ({file_count} files, {size_mb:.2f} MB)")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Archive old data files')
    parser.add_argument('--days', type=int, default=7,
                       help='Number of business days to keep active (default: 7)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be archived without actually moving files')
    parser.add_argument('--list-archive', action='store_true',
                       help='Show archive directory structure')
    parser.add_argument('--data-dir', type=str, default=None,
                       help='Path to data directory (default: ../data)')
    
    args = parser.parse_args()
    
    # Determine data directory
    if args.data_dir:
        data_dir = Path(args.data_dir)
    else:
        script_dir = Path(__file__).parent
        data_dir = script_dir.parent / 'data'
    
    archive_dir = data_dir / 'archive'
    
    if args.list_archive:
        list_archive_structure(archive_dir)
        return
    
    print(f"🧹 Archive Old Data Files")
    print(f"   Data Directory: {data_dir}")
    print(f"   Archive Directory: {archive_dir}")
    print(f"   Retention: Last {args.days} business days")
    print(f"   Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()
    
    archive_old_files(data_dir, keep_days=args.days, dry_run=args.dry_run)
    
    if not args.dry_run:
        print(f"\n💡 Tip: Use --list-archive to view the archive structure")

if __name__ == "__main__":
    main()
