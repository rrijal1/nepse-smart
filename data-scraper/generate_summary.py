#!/usr/bin/env python3
"""
Enhanced Collection Summary Generator
- Generates comprehensive daily collection summary
- Includes historical data status and trends
- Monitors data quality and scraper health
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

def analyze_daily_data() -> Dict:
    """Analyze today's data collection"""
    data_dir = Path("../data/daily")
    today = datetime.now().strftime('%Y-%m-%d')
    
    summary = {
        'collection_date': today,
        'generated_at': datetime.now().isoformat(),
        'scrapers': {},
        'totals': {
            'total_records': 0,
            'total_files': 0,
            'total_size_mb': 0.0
        },
        'success': True,
        'quality_checks': {}
    }
    
    # Define expected data types and their minimum record counts
    data_types = {
        'prices': {'min_records': 250, 'max_size_mb': 0.5},
        'floorsheet': {'min_records': 1000, 'max_size_mb': 50.0},
        'indices': {'min_records': 15, 'max_size_mb': 0.1},
        'macro': {'min_records': 10, 'max_size_mb': 0.1}
    }
    
    successful_scrapers = 0
    
    for data_type, expectations in data_types.items():
        file_pattern = f"{today}_{data_type}.json"
        files = list(data_dir.glob(file_pattern))
        
        scraper_info = {
            'status': 'missing',
            'filename': file_pattern,
            'records': 0,
            'size_mb': 0.0,
            'quality': 'unknown',
            'issues': []
        }
        
        if files:
            file_path = files[0]
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                # Count records
                if isinstance(data, list):
                    record_count = len(data)
                elif isinstance(data, dict):
                    record_count = sum(len(v) if isinstance(v, list) else 1 for v in data.values())
                else:
                    record_count = 1
                
                # Calculate file size
                size_mb = round(file_path.stat().st_size / (1024*1024), 2)
                
                # Update scraper info
                scraper_info.update({
                    'status': 'success',
                    'records': record_count,
                    'size_mb': size_mb,
                    'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                })
                
                # Quality checks
                quality_issues = []
                if record_count < expectations['min_records']:
                    quality_issues.append(f"Low record count: {record_count} < {expectations['min_records']}")
                
                if size_mb > expectations['max_size_mb']:
                    quality_issues.append(f"Large file size: {size_mb}MB > {expectations['max_size_mb']}MB")
                
                if not data:
                    quality_issues.append("Empty data file")
                
                scraper_info['quality'] = 'good' if not quality_issues else 'warning'
                scraper_info['issues'] = quality_issues
                
                # Update totals
                summary['totals']['total_records'] += record_count
                summary['totals']['total_size_mb'] += size_mb
                successful_scrapers += 1
                
            except Exception as e:
                scraper_info.update({
                    'status': 'error',
                    'error': str(e),
                    'quality': 'failed'
                })
                
        summary['scrapers'][data_type] = scraper_info
    
    summary['totals']['total_files'] = successful_scrapers
    summary['success'] = successful_scrapers >= 3  # At least 3 out of 4 should succeed
    
    return summary

def analyze_historical_trends() -> Dict:
    """Analyze historical data trends"""
    historical_dir = Path("../data/historical")
    trends = {}
    
    data_types = ['prices', 'floorsheet', 'indices', 'macro']
    
    for data_type in data_types:
        file_path = historical_dir / f"historical_{data_type}.json"
        
        trend_info = {
            'file_exists': file_path.exists(),
            'total_historical_records': 0,
            'unique_dates': 0,
            'date_range': None,
            'last_update': None
        }
        
        if file_path.exists():
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                
                if isinstance(data, list) and data:
                    trend_info['total_historical_records'] = len(data)
                    
                    # Extract dates
                    dates = [record.get('date') for record in data if isinstance(record, dict) and record.get('date')]
                    unique_dates = list(set(date for date in dates if date is not None))
                    
                    trend_info['unique_dates'] = len(unique_dates)
                    
                    if unique_dates:
                        sorted_dates = sorted(unique_dates)
                        trend_info['date_range'] = {
                            'earliest': sorted_dates[0],
                            'latest': sorted_dates[-1]
                        }
                        trend_info['last_update'] = sorted_dates[-1]
                
                # File stats
                trend_info['file_size_mb'] = round(file_path.stat().st_size / (1024*1024), 2)
                trend_info['last_modified'] = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                
            except Exception as e:
                trend_info['error'] = str(e)
        
        trends[data_type] = trend_info
    
    return trends

def generate_enhanced_summary() -> Dict:
    """Generate comprehensive collection summary"""
    print("📊 Generating enhanced collection summary...")
    
    # Analyze daily data
    daily_analysis = analyze_daily_data()
    
    # Analyze historical trends
    historical_trends = analyze_historical_trends()
    
    # Combine into enhanced summary
    enhanced_summary = {
        **daily_analysis,
        'historical_data': historical_trends,
        'system_health': {
            'overall_status': 'healthy' if daily_analysis['success'] else 'degraded',
            'active_scrapers': sum(1 for s in daily_analysis['scrapers'].values() if s['status'] == 'success'),
            'total_scrapers': len(daily_analysis['scrapers']),
            'data_freshness': 'current',  # Could be enhanced to check staleness
        }
    }
    
    # Add recommendations
    recommendations = []
    
    for data_type, info in daily_analysis['scrapers'].items():
        if info['status'] == 'missing':
            recommendations.append(f"Fix {data_type} scraper - no data collected")
        elif info['status'] == 'error':
            recommendations.append(f"Debug {data_type} scraper error: {info.get('error', 'Unknown')}")
        elif info['issues']:
            recommendations.append(f"Review {data_type} data quality: {'; '.join(info['issues'])}")
    
    if not historical_trends:
        recommendations.append("Historical data tracking not working")
    
    enhanced_summary['recommendations'] = recommendations
    
    return enhanced_summary

def save_summary(summary: Dict) -> bool:
    """Save summary to both daily and root locations"""
    try:
        # Ensure directories exist
        os.makedirs("../data/daily", exist_ok=True)
        
        # Save to daily folder
        daily_path = Path("../data/daily/collection_summary.json")
        with open(daily_path, 'w') as f:
            json.dump(summary, f, indent=2, default=str, ensure_ascii=False)
        
        print(f"✅ Summary saved to {daily_path}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to save summary: {e}")
        return False

def print_summary_report(summary: Dict):
    """Print formatted summary report"""
    print("\n" + "="*60)
    print("📊 NEPSE DATA COLLECTION SUMMARY")
    print("="*60)
    print(f"📅 Date: {summary['collection_date']}")
    print(f"🕐 Generated: {summary['generated_at']}")
    print(f"🎯 Success: {'✅ YES' if summary['success'] else '❌ NO'}")
    print(f"📁 Active Scrapers: {summary['system_health']['active_scrapers']}/{summary['system_health']['total_scrapers']}")
    print(f"📈 Total Records: {summary['totals']['total_records']:,}")
    print(f"💾 Total Size: {summary['totals']['total_size_mb']:.1f} MB")
    
    print(f"\n📋 SCRAPER DETAILS:")
    print("-" * 40)
    for data_type, info in summary['scrapers'].items():
        status_icon = "✅" if info['status'] == 'success' else "❌" if info['status'] == 'error' else "⚠️"
        quality_icon = "🟢" if info['quality'] == 'good' else "🟡" if info['quality'] == 'warning' else "🔴"
        
        print(f"{status_icon} {data_type.capitalize()}: {info['records']:,} records ({info['size_mb']:.1f}MB) {quality_icon}")
        
        if info.get('issues'):
            for issue in info['issues']:
                print(f"   ⚠️ {issue}")
    
    if summary.get('historical_data'):
        print(f"\n📚 HISTORICAL DATA:")
        print("-" * 40)
        for data_type, info in summary['historical_data'].items():
            if info['file_exists']:
                print(f"📈 {data_type.capitalize()}: {info['total_historical_records']:,} records ({info['unique_dates']} dates)")
            else:
                print(f"❌ {data_type.capitalize()}: No historical data")
    
    if summary.get('recommendations'):
        print(f"\n💡 RECOMMENDATIONS:")
        print("-" * 40)
        for rec in summary['recommendations']:
            print(f"• {rec}")
    
    print("="*60)

def main():
    """Main entry point"""
    try:
        # Generate enhanced summary
        summary = generate_enhanced_summary()
        
        # Save to file
        save_success = save_summary(summary)
        
        # Print report
        print_summary_report(summary)
        
        # Exit with appropriate code
        if not summary['success']:
            print("\n❌ Collection partially failed - check individual scrapers")
            exit(1)
        elif not save_success:
            print("\n⚠️ Summary generation failed")
            exit(1)
        else:
            print("\n✅ Collection and summary completed successfully")
            exit(0)
            
    except Exception as e:
        print(f"\n❌ Summary generation error: {e}")
        exit(1)

if __name__ == "__main__":
    main()