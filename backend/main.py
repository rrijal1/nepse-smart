#!/usr/bin/env python3
"""
Updated FastAPI Backend - Using Our Own Scraped Data
- Replaces unofficial NEPSE API dependency
- Uses comprehensive scraped historical data
- Provides enhanced market data endpoints
- Portfolio and Watchlist management with PostgreSQL
"""

import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
import asyncio
import json
from typing import List, Optional, Dict, Any
import logging

from dotenv import load_dotenv

# Import our new data service
from backend.nepse_data_service import NepseDataService

# Import database initialization
from backend.database import engine, Base
from backend.portfolio_routes import router as portfolio_router
from backend.agent_routes import router as agent_router
from backend.papertrading_routes import router as papertrading_router


# Load environment variables from .env if present (useful in local/dev setups)
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="NEPSE Analytics API - Enhanced", 
    version="2.0.0",
    description="Comprehensive NEPSE market data API using our own scraped data"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include portfolio & watchlist routes
app.include_router(portfolio_router)
app.include_router(papertrading_router)

# Include LangChain agent routes
app.include_router(agent_router, prefix="/api")

# Initialize our data service
nepse_data = NepseDataService(data_path="data")

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables initialized")

    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")

@app.get("/", tags=["System"])
def read_root():
    """API root endpoint"""
    return {
        "message": "NEPSE Analytics API - Enhanced with Own Data",
        "version": "2.0.0",
        "data_source": "Own scraped data",
        "endpoints": {
            "market_data": [
                "/api/market-status",
                "/api/summary", 
                "/api/top-gainers",
                "/api/top-losers",
                "/api/nepse-index",
                "/api/sub-indices",
                "/api/price-volume",
                "/api/company-list",
                "/api/macro-data"
            ],
            "historical": [
                "/api/historical/{data_type}",
                "/api/company-history/{symbol}"
            ],
            "portfolio": [
                "/api/watchlist",
                "/api/portfolio",
                "/api/portfolio/summary",
                "/api/transactions"
            ],
            "system": [
                "/api/system-status",
                "/api/data-freshness"
            ]
        }
    }

# System Endpoints
@app.get("/api/system-status", tags=["System"])
def get_system_status():
    """Get system status and data availability"""
    try:
        status = nepse_data.get_system_status()
        return status
    except Exception as e:
        logger.error(f"System status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data-freshness", tags=["System"])
def get_data_freshness():
    """Check how fresh our data is"""
    try:
        status = nepse_data.get_system_status()
        
        freshness = {}
        for data_type, info in status["data_sources"].items():
            if info["available"] and info["last_update"]:
                try:
                    last_update = datetime.strptime(info["last_update"], "%Y-%m-%d")
                    days_old = (datetime.now() - last_update).days
                    freshness[data_type] = {
                        "last_update": info["last_update"],
                        "days_old": days_old,
                        "status": "fresh" if days_old == 0 else "stale" if days_old > 1 else "recent"
                    }
                except:
                    freshness[data_type] = {"status": "unknown"}
            else:
                freshness[data_type] = {"status": "unavailable"}
        
        return {
            "data_freshness": freshness,
            "checked_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Data freshness error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Market Data Endpoints
@app.get("/api/market-status", tags=["Market Data"])
def get_market_status():
    """Check if NEPSE market is open"""
    try:
        is_open = nepse_data.is_market_open()
        return {
            "is_open": is_open,
            "checked_at": datetime.now().isoformat(),
            "note": "Basic time-based estimation"
        }
    except Exception as e:
        logger.error(f"Market status error: {e}")
        return {"error": str(e), "is_open": False}

@app.get("/api/summary", tags=["Market Data"])
def get_market_summary():
    """Get comprehensive market summary"""
    try:
        summary = nepse_data.get_market_summary()
        return summary
    except Exception as e:
        logger.error(f"Market summary error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top-gainers", tags=["Market Data"])
def get_top_gainers(limit: int = Query(10, ge=1, le=50)):
    """Get top gaining stocks"""
    try:
        gainers = nepse_data.get_top_gainers(limit)
        return {
            "gainers": gainers,
            "count": len(gainers),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Top gainers error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/top-losers", tags=["Market Data"])
def get_top_losers(limit: int = Query(10, ge=1, le=50)):
    """Get top losing stocks"""
    try:
        losers = nepse_data.get_top_losers(limit)
        return {
            "losers": losers,
            "count": len(losers),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Top losers error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/nepse-index", tags=["Market Data"])
def get_nepse_index():
    """Get NEPSE index data"""
    try:
        index_data = nepse_data.get_nepse_index()
        return index_data
    except Exception as e:
        logger.error(f"NEPSE index error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sub-indices", tags=["Market Data"])
def get_sub_indices():
    """Get NEPSE sub-indices data"""
    try:
        sub_indices = nepse_data.get_sub_indices()
        return {
            "sub_indices": sub_indices,
            "count": len(sub_indices),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Sub-indices error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/price-volume", tags=["Market Data"])
def get_price_volume(limit: int = Query(None, ge=1, le=1000)):
    """Get price volume data for all stocks"""
    try:
        price_data = nepse_data.get_price_volume()
        
        if limit:
            price_data = price_data[:limit]
        
        return {
            "stocks": price_data,
            "count": len(price_data),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Price volume error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/company-list", tags=["Market Data"])
def get_company_list():
    """Get list of all companies"""
    try:
        companies = nepse_data.get_company_list()
        return {
            "companies": companies,
            "count": len(companies),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Company list error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/macro-data", tags=["Market Data"])
def get_macro_data():
    """Get macro economic data (forex, banking indicators, interest rates)"""
    try:
        macro_data = nepse_data.get_macro_data()
        return macro_data
    except Exception as e:
        logger.error(f"Macro data error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Historical Data Endpoints
@app.get("/api/historical/{data_type}", tags=["Historical Data"])
def get_historical_data(
    data_type: str,
    days: int = Query(30, ge=1, le=365, description="Number of days of historical data")
):
    """Get historical data for specified type and duration"""
    try:
        valid_types = ['prices', 'indices', 'macro', 'floorsheet']
        if data_type not in valid_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid data type. Must be one of: {valid_types}"
            )
        
        historical_data = nepse_data.get_historical_data(data_type, days)
        
        if not historical_data:
            raise HTTPException(
                status_code=404,
                detail=f"No historical data found for {data_type}"
            )
        
        return {
            "data_type": data_type,
            "data": historical_data,
            "count": len(historical_data),
            "days_requested": days,
            "date_range": {
                "from": historical_data[-1].get('date') if historical_data else None,
                "to": historical_data[0].get('date') if historical_data else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Historical data error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/company-history/{symbol}", tags=["Historical Data"])
def get_company_history(
    symbol: str,
    days: int = Query(30, ge=1, le=365, description="Number of days of price history")
):
    """Get price history for a specific company"""
    try:
        company_history = nepse_data.get_company_price_history(symbol.upper(), days)
        
        if not company_history:
            raise HTTPException(
                status_code=404,
                detail=f"No price history found for {symbol}"
            )
        
        return {
            "symbol": symbol.upper(),
            "data": company_history,
            "count": len(company_history),
            "days_requested": days,
            "date_range": {
                "from": company_history[-1].get('date') if company_history else None,
                "to": company_history[0].get('date') if company_history else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Company history error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/historical-prices", tags=["Historical Data"])
def get_historical_prices(symbol: Optional[str] = Query(None, description="Filter by stock symbol")):
    """Get historical prices data, optionally filtered by symbol"""
    try:
        # Load historical prices data
        filepath = Path("data/historical/historical_prices.json")
        if not filepath.exists():
            raise HTTPException(status_code=404, detail="Historical prices data not found")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            all_data = json.load(f)
        
        if symbol:
            # Filter by symbol
            symbol_upper = symbol.upper()
            filtered_data = [item for item in all_data if item.get('symbol') == symbol_upper]
            
            if not filtered_data:
                raise HTTPException(
                    status_code=404,
                    detail=f"No historical data found for symbol {symbol}"
                )
            
            return {
                "symbol": symbol_upper,
                "data": filtered_data,
                "count": len(filtered_data),
                "filtered": True
            }
        else:
            # Return all data
            return {
                "data": all_data,
                "count": len(all_data),
                "filtered": False
            }
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Historical prices error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Search and Filter Endpoints
@app.get("/api/search-stocks", tags=["Search"])
def search_stocks(
    query: str = Query(..., min_length=1, description="Search query for stock symbols or names"),
    limit: int = Query(20, ge=1, le=100)
):
    """Search stocks by symbol or name"""
    try:
        companies = nepse_data.get_company_list()
        
        # Filter companies based on query
        query_lower = query.lower()
        matching_companies = [
            company for company in companies
            if (query_lower in company.get('symbol', '').lower() or 
                query_lower in company.get('name', '').lower())
        ]
        
        return {
            "query": query,
            "results": matching_companies[:limit],
            "count": len(matching_companies),
            "total_available": len(companies)
        }
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Data Quality Endpoints
@app.get("/api/data-quality", tags=["System"])
def get_data_quality():
    """Get data quality metrics"""
    try:
        quality_report = {
            "data_sources": {},
            "quality_score": 0,
            "last_checked": datetime.now().isoformat()
        }
        
        # Check each data source
        data_types = ['prices', 'indices', 'macro']
        total_score = 0
        
        for data_type in data_types:
            data = nepse_data.get_daily_data(data_type)
            
            if data:
                record_count = len(data)
                # Simple quality metrics
                has_symbols = sum(1 for record in data if record.get('symbol') or record.get('index_name'))
                has_dates = sum(1 for record in data if record.get('date'))
                
                completeness = (has_symbols + has_dates) / (2 * record_count) if record_count > 0 else 0
                
                quality_report["data_sources"][data_type] = {
                    "available": True,
                    "record_count": record_count,
                    "completeness": completeness,
                    "quality_score": min(completeness * 100, 100)
                }
                
                total_score += completeness
            else:
                quality_report["data_sources"][data_type] = {
                    "available": False,
                    "quality_score": 0
                }
        
        quality_report["quality_score"] = (total_score / len(data_types)) * 100
        
        return quality_report
        
    except Exception as e:
        logger.error(f"Data quality error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "data_source": "own_scraped_data"
    }

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Enhanced NEPSE Analytics API...")
    print("📊 Using our own scraped data instead of unofficial API")
    print("🌐 API Documentation: http://localhost:8000/docs")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)