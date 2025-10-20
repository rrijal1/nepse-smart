#!/usr/bin/env python3
"""
Check and remove duplicates from historical JSON files
"""
import json
from collections import Counter
from pathlib import Path

def check_floorsheet_duplicates():
    """Check floorsheet duplicates using transaction_no + quantity + time"""
    file_path = Path('data/historical/historical_floorsheet.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"📊 Floorsheet: {len(data)} total records")
    
    # Create composite keys: (transaction_no, quantity, time/date)
    keys = []
    for item in data:
        key = (
            item.get('transaction_no'),
            item.get('quantity'), 
            item.get('date'),  # using date since we might not have exact time
            item.get('rate')   # adding rate for extra uniqueness
        )
        keys.append(key)
    
    # Find duplicates
    counter = Counter(keys)
    duplicates = [k for k, v in counter.items() if v > 1]
    
    print(f"🔍 Found {len(duplicates)} duplicate keys")
    if duplicates:
        total_duplicates = sum(counter[k] - 1 for k in duplicates)
        print(f"📈 Total duplicate records to remove: {total_duplicates}")
        print(f"📝 Sample duplicates: {duplicates[:5]}")
        
        # Remove duplicates - keep first occurrence
        seen = set()
        unique_data = []
        
        for item in data:
            key = (
                item.get('transaction_no'),
                item.get('quantity'), 
                item.get('date'),
                item.get('rate')
            )
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        print(f"✅ After deduplication: {len(unique_data)} unique records")
        
        # Save deduplicated data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved deduplicated floorsheet data")
        return len(data) - len(unique_data)
    
    return 0

def check_prices_duplicates():
    """Check prices duplicates using date + stock_symbol"""
    file_path = Path('data/historical/historical_prices.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📊 Prices: {len(data)} total records")
    
    # Create composite keys: (date, stock_symbol)
    keys = [(item.get('date'), item.get('stock_symbol')) for item in data]
    
    counter = Counter(keys)
    duplicates = [k for k, v in counter.items() if v > 1]
    
    print(f"🔍 Found {len(duplicates)} duplicate keys")
    if duplicates:
        total_duplicates = sum(counter[k] - 1 for k in duplicates)
        print(f"📈 Total duplicate records to remove: {total_duplicates}")
        
        # Remove duplicates - keep first occurrence  
        seen = set()
        unique_data = []
        
        for item in data:
            key = (item.get('date'), item.get('stock_symbol'))
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        print(f"✅ After deduplication: {len(unique_data)} unique records")
        
        # Save deduplicated data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved deduplicated prices data")
        return len(data) - len(unique_data)
    
    return 0

def check_indices_duplicates():
    """Check indices duplicates using date + index_name"""
    file_path = Path('data/historical/historical_indices.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📊 Indices: {len(data)} total records")
    
    # Create composite keys: (date, index_name)
    keys = [(item.get('date'), item.get('index_name')) for item in data]
    
    counter = Counter(keys)
    duplicates = [k for k, v in counter.items() if v > 1]
    
    print(f"🔍 Found {len(duplicates)} duplicate keys")
    if duplicates:
        total_duplicates = sum(counter[k] - 1 for k in duplicates)
        print(f"📈 Total duplicate records to remove: {total_duplicates}")
        
        # Remove duplicates - keep first occurrence
        seen = set()
        unique_data = []
        
        for item in data:
            key = (item.get('date'), item.get('index_name'))
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        print(f"✅ After deduplication: {len(unique_data)} unique records")
        
        # Save deduplicated data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved deduplicated indices data")
        return len(data) - len(unique_data)
    
    return 0

def check_macro_duplicates():
    """Check macro duplicates using date"""
    file_path = Path('data/historical/historical_macro.json')
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\n📊 Macro: {len(data)} total records")
    
    # Create keys: date
    keys = [item.get('date') for item in data]
    
    counter = Counter(keys)
    duplicates = [k for k, v in counter.items() if v > 1]
    
    print(f"🔍 Found {len(duplicates)} duplicate keys")
    if duplicates:
        total_duplicates = sum(counter[k] - 1 for k in duplicates)
        print(f"📈 Total duplicate records to remove: {total_duplicates}")
        
        # Remove duplicates - keep first occurrence
        seen = set()
        unique_data = []
        
        for item in data:
            key = item.get('date')
            
            if key not in seen:
                seen.add(key)
                unique_data.append(item)
        
        print(f"✅ After deduplication: {len(unique_data)} unique records")
        
        # Save deduplicated data
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(unique_data, f, ensure_ascii=False, indent=2)
        
        print(f"💾 Saved deduplicated macro data")
        return len(data) - len(unique_data)
    
    return 0

if __name__ == '__main__':
    print("🔍 Checking for duplicates in historical files...")
    print("="*60)
    
    total_removed = 0
    total_removed += check_floorsheet_duplicates()
    total_removed += check_prices_duplicates()
    total_removed += check_indices_duplicates()
    total_removed += check_macro_duplicates()
    
    print("\n" + "="*60)
    print(f"🎯 DEDUPLICATION COMPLETE")
    print(f"📊 Total duplicate records removed: {total_removed}")
    print("✅ All historical files have been deduplicated")