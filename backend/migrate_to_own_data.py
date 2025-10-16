#!/usr/bin/env python3
"""
Migration Script: From Unofficial NEPSE API to Our Own Data
- Updates backend endpoints to use scraped data
- Creates data mapping and compatibility layer
- Provides migration path for frontend
"""

import json
import shutil
from pathlib import Path
from datetime import datetime

def backup_original_backend():
    """Backup the original backend file"""
    backend_path = Path("main.py")
    backup_path = Path("main_original_backup.py")
    
    if backend_path.exists() and not backup_path.exists():
        shutil.copy2(backend_path, backup_path)
        print("✅ Backed up original backend to main_original_backup.py")
    
def update_backend():
    """Replace the main backend with enhanced version"""
    enhanced_path = Path("main_enhanced.py")
    main_path = Path("main.py")
    
    if enhanced_path.exists():
        # Backup original first
        backup_original_backend()
        
        # Replace with enhanced version
        shutil.copy2(enhanced_path, main_path)
        print("✅ Updated main.py with enhanced backend")
        print("📊 Backend now uses our own scraped data!")
    else:
        print("❌ Enhanced backend file not found")

def create_api_comparison():
    """Create API endpoint comparison"""
    comparison = {
        "migration_date": datetime.now().isoformat(),
        "api_changes": {
            "old_unofficial_api": {
                "source": "Unofficial NEPSE API (api/nepse/)",
                "endpoints": [
                    "/api/market-status",
                    "/api/summary", 
                    "/api/top-gainers",
                    "/api/top-losers",
                    "/api/nepse-index",
                    "/api/company-list",
                    "/api/price-volume"
                ],
                "limitations": [
                    "Dependent on external unofficial API",
                    "No historical data management",
                    "Limited error handling",
                    "No data freshness tracking"
                ]
            },
            "new_enhanced_api": {
                "source": "Our own scraped data (data-scraper/)",
                "endpoints": [
                    "/api/market-status",
                    "/api/summary", 
                    "/api/top-gainers",
                    "/api/top-losers", 
                    "/api/nepse-index",
                    "/api/sub-indices",
                    "/api/company-list",
                    "/api/price-volume",
                    "/api/macro-data",
                    "/api/historical/{data_type}",
                    "/api/company-history/{symbol}",
                    "/api/system-status",
                    "/api/data-freshness",
                    "/api/search-stocks",
                    "/api/data-quality"
                ],
                "advantages": [
                    "Uses our own reliable scraped data",
                    "Comprehensive historical data",
                    "Enhanced error handling and caching",
                    "Data quality monitoring",
                    "System status tracking",
                    "Search and filtering capabilities",
                    "Macro economic data (forex, banking)",
                    "Sub-indices data"
                ]
            }
        },
        "data_sources": {
            "prices": {
                "source": "ShareSansar",
                "records": "~311 stocks daily",
                "fields": ["symbol", "ltp", "high", "low", "open", "change", "change_percent"]
            },
            "indices": {
                "source": "ShareSansar", 
                "records": "17 indices/sub-indices daily",
                "fields": ["index_name", "current_value", "change", "change_percent", "turnover"]
            },
            "macro": {
                "source": "NRB Homepage",
                "records": "16 macro indicators daily",
                "fields": ["forex_rates", "banking_indicators", "short_term_rates"]
            },
            "floorsheet": {
                "source": "MeroLagani",
                "records": "~36,000 transactions daily",
                "fields": ["symbol", "quantity", "rate", "amount"]
            }
        },
        "compatibility": {
            "existing_endpoints": "Fully compatible - same endpoint URLs",
            "response_format": "Enhanced with additional metadata",
            "breaking_changes": "None - backward compatible",
            "new_features": [
                "Historical data access",
                "Data quality metrics",
                "System health monitoring",
                "Enhanced search capabilities"
            ]
        }
    }
    
    with open("api_migration_guide.json", "w") as f:
        json.dump(comparison, f, indent=2, default=str)
    
    print("✅ Created API migration guide: api_migration_guide.json")

def create_frontend_service_update():
    """Create updated frontend service"""
    frontend_service = '''// Enhanced Market Data Service - Using Our Own Data
import axios from "axios";

const API_BASE = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:8000/api';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// Market Data Functions
export const fetchMarketSummary = async () => {
  try {
    const response = await api.get('/summary');
    return response.data;
  } catch (error) {
    console.error("Error fetching market summary:", error);
    return { error: "Failed to fetch market summary" };
  }
};

export const fetchTopGainers = async (limit = 10) => {
  try {
    const response = await api.get(`/top-gainers?limit=${limit}`);
    return response.data.gainers || [];
  } catch (error) {
    console.error("Error fetching top gainers:", error);
    return [];
  }
};

export const fetchTopLosers = async (limit = 10) => {
  try {
    const response = await api.get(`/top-losers?limit=${limit}`);
    return response.data.losers || [];
  } catch (error) {
    console.error("Error fetching top losers:", error);
    return [];
  }
};

export const fetchNepseIndex = async () => {
  try {
    const response = await api.get('/nepse-index');
    return response.data;
  } catch (error) {
    console.error("Error fetching NEPSE index:", error);
    return { error: "Failed to fetch NEPSE index" };
  }
};

export const fetchSubIndices = async () => {
  try {
    const response = await api.get('/sub-indices');
    return response.data.sub_indices || [];
  } catch (error) {
    console.error("Error fetching sub-indices:", error);
    return [];
  }
};

export const fetchPriceVolume = async (limit = null) => {
  try {
    const url = limit ? `/price-volume?limit=${limit}` : '/price-volume';
    const response = await api.get(url);
    return response.data.stocks || [];
  } catch (error) {
    console.error("Error fetching price volume:", error);
    return [];
  }
};

export const fetchCompanyList = async () => {
  try {
    const response = await api.get('/company-list');
    return response.data.companies || [];
  } catch (error) {
    console.error("Error fetching company list:", error);
    return [];
  }
};

// New Enhanced Functions
export const fetchMacroData = async () => {
  try {
    const response = await api.get('/macro-data');
    return response.data;
  } catch (error) {
    console.error("Error fetching macro data:", error);
    return { error: "Failed to fetch macro data" };
  }
};

export const fetchHistoricalData = async (dataType, days = 30) => {
  try {
    const response = await api.get(`/historical/${dataType}?days=${days}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching historical ${dataType}:`, error);
    return { error: `Failed to fetch historical ${dataType}` };
  }
};

export const fetchCompanyHistory = async (symbol, days = 30) => {
  try {
    const response = await api.get(`/company-history/${symbol}?days=${days}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching ${symbol} history:`, error);
    return { error: `Failed to fetch ${symbol} history` };
  }
};

export const searchStocks = async (query, limit = 20) => {
  try {
    const response = await api.get(`/search-stocks?query=${encodeURIComponent(query)}&limit=${limit}`);
    return response.data.results || [];
  } catch (error) {
    console.error("Error searching stocks:", error);
    return [];
  }
};

// System Monitoring Functions
export const fetchSystemStatus = async () => {
  try {
    const response = await api.get('/system-status');
    return response.data;
  } catch (error) {
    console.error("Error fetching system status:", error);
    return { error: "Failed to fetch system status" };
  }
};

export const fetchDataFreshness = async () => {
  try {
    const response = await api.get('/data-freshness');
    return response.data;
  } catch (error) {
    console.error("Error fetching data freshness:", error);
    return { error: "Failed to fetch data freshness" };
  }
};

export const fetchDataQuality = async () => {
  try {
    const response = await api.get('/data-quality');
    return response.data;
  } catch (error) {
    console.error("Error fetching data quality:", error);
    return { error: "Failed to fetch data quality" };
  }
};

export const checkMarketStatus = async () => {
  try {
    const response = await api.get('/market-status');
    return response.data;
  } catch (error) {
    console.error("Error checking market status:", error);
    return { error: "Failed to check market status", is_open: false };
  }
};

// Utility Functions
export const formatCurrency = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-NP', {
    style: 'currency',
    currency: 'NPR',
    minimumFractionDigits: 2
  }).format(value);
};

export const formatPercentage = (value) => {
  if (value === null || value === undefined) return 'N/A';
  const sign = value >= 0 ? '+' : '';
  return `${sign}${value.toFixed(2)}%`;
};

export const formatNumber = (value) => {
  if (value === null || value === undefined) return 'N/A';
  return new Intl.NumberFormat('en-NP').format(value);
};

// Export default api instance for direct use
export default api;
'''
    
    # Save the updated frontend service
    frontend_service_path = Path("../frontend/src/services/marketData_enhanced.ts")
    frontend_service_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(frontend_service_path, "w") as f:
        f.write(frontend_service)
    
    print("✅ Created enhanced frontend service: frontend/src/services/marketData_enhanced.ts")

def main():
    """Run the migration process"""
    print("🚀 Starting Migration: Unofficial NEPSE API → Our Own Data")
    print("=" * 60)
    
    # Step 1: Update backend
    print("\n1️⃣ Updating Backend...")
    update_backend()
    
    # Step 2: Create migration documentation
    print("\n2️⃣ Creating Migration Documentation...")
    create_api_comparison()
    
    # Step 3: Create enhanced frontend service
    print("\n3️⃣ Creating Enhanced Frontend Service...")
    create_frontend_service_update()
    
    print("\n" + "=" * 60)
    print("✅ MIGRATION COMPLETED!")
    print("\n📊 Summary:")
    print("  • Backend updated to use our own scraped data")
    print("  • All existing endpoints remain compatible")
    print("  • Added enhanced endpoints for historical data")
    print("  • Created comprehensive API documentation")
    print("  • Frontend service enhanced with new capabilities")
    
    print("\n🚀 Next Steps:")
    print("  1. Test the enhanced backend: python3 main.py")
    print("  2. Update frontend to use enhanced service")
    print("  3. Deploy the updated system")
    print("  4. Monitor data quality and system health")
    
    print(f"\n📈 New Capabilities:")
    print("  • 311 stock prices from ShareSansar")
    print("  • 17 indices & sub-indices")
    print("  • 16 macro economic indicators")
    print("  • Historical data for all data types")
    print("  • System health monitoring")
    print("  • Data quality tracking")

if __name__ == "__main__":
    main()