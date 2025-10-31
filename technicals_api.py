#!/usr/bin/env python3
"""
Technical Indicators API Server
- Serves technical indicators data from generated JSON files
- Provides REST API endpoints for RSI and MACD data
- Automatically uses the latest generated technicals file
"""

import json
import os
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional, Dict, Any
import uvicorn
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TechnicalIndicatorsAPI:
    """API server for technical indicators data"""

    def __init__(self, technicals_dir: str = "data/technicals"):
        self.technicals_dir = Path(technicals_dir)
        self.technicals_dir.mkdir(parents=True, exist_ok=True)
        self._technicals_data = None
        self._last_loaded = None

    def get_latest_technicals_file(self) -> Optional[Path]:
        """Find the most recent technicals JSON file"""
        if not self.technicals_dir.exists():
            return None

        # Find all technicals JSON files
        technicals_files = list(self.technicals_dir.glob("technicals_*.json"))

        if not technicals_files:
            return None

        # Sort by modification time (newest first)
        technicals_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
        return technicals_files[0]

    def load_technicals_data(self, force_reload: bool = False) -> Dict[str, Any]:
        """Load technical indicators data from the latest file"""
        latest_file = self.get_latest_technicals_file()

        if not latest_file:
            logger.warning("No technicals files found")
            return {}

        # Check if we need to reload
        if not force_reload and self._last_loaded and latest_file == self._last_loaded:
            return self._technicals_data or {}

        try:
            logger.info(f"Loading technicals data from: {latest_file}")
            with open(latest_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._technicals_data = data
            self._last_loaded = latest_file

            logger.info(f"✅ Loaded technicals data for {len(data)} stocks")
            return data

        except Exception as e:
            logger.error(f"❌ Failed to load technicals data: {e}")
            return {}

    def get_technicals_for_symbol(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get technical indicators for a specific symbol"""
        data = self.load_technicals_data()
        return data.get(symbol.upper())

    def get_all_technicals(self) -> Dict[str, Any]:
        """Get all technical indicators data"""
        return self.load_technicals_data()

    def get_rsi_signals(self, oversold_threshold: float = 30, overbought_threshold: float = 70) -> Dict[str, Any]:
        """Get RSI signals (oversold/overbought)"""
        data = self.load_technicals_data()
        oversold = []
        overbought = []

        for symbol, technicals in data.items():
            rsi = technicals.get('rsi_14')
            if rsi is not None:
                signal_data = {
                    "symbol": symbol,
                    "rsi_14": rsi,
                    "current_price": technicals.get('current_price'),
                    "volume": technicals.get('volume')
                }

                if rsi <= oversold_threshold:
                    oversold.append(signal_data)
                elif rsi >= overbought_threshold:
                    overbought.append(signal_data)

        return {
            "oversold": sorted(oversold, key=lambda x: x['rsi_14']),
            "overbought": sorted(overbought, key=lambda x: x['rsi_14'], reverse=True),
            "thresholds": {
                "oversold": oversold_threshold,
                "overbought": overbought_threshold
            }
        }

    def get_macd_signals(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get MACD signals (crossovers)"""
        data = self.load_technicals_data()
        bullish_crossovers = []
        bearish_crossovers = []

        for symbol, technicals in data.items():
            macd_data = technicals.get('macd', {})
            signal_state = macd_data.get('signal_state')

            if signal_state == 'bullish_crossover':
                bullish_crossovers.append({
                    "symbol": symbol,
                    "signal": "bullish_crossover",
                    "macd_line": macd_data.get('line'),
                    "signal_line": macd_data.get('signal'),
                    "histogram": macd_data.get('histogram'),
                    "current_price": technicals.get('current_price'),
                    "volume": technicals.get('volume')
                })
            elif signal_state == 'bearish_crossover':
                bearish_crossovers.append({
                    "symbol": symbol,
                    "signal": "bearish_crossover",
                    "macd_line": macd_data.get('line'),
                    "signal_line": macd_data.get('signal'),
                    "histogram": macd_data.get('histogram'),
                    "current_price": technicals.get('current_price'),
                    "volume": technicals.get('volume')
                })

        return {
            "bullish_crossovers": bullish_crossovers,
            "bearish_crossovers": bearish_crossovers
        }

# Initialize API
app = FastAPI(
    title="Technical Indicators API",
    version="1.0.0",
    description="API for accessing technical indicators (RSI, MACD) data"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize technicals API
technicals_api = TechnicalIndicatorsAPI()

@app.get("/", tags=["System"])
def read_root():
    """API root endpoint"""
    latest_file = technicals_api.get_latest_technicals_file()
    data_count = len(technicals_api.get_all_technicals())

    return {
        "message": "Technical Indicators API",
        "version": "1.0.0",
        "data_source": latest_file.name if latest_file else "No data available",
        "total_stocks": data_count,
        "endpoints": {
            "technicals": [
                "/api/technicals/{symbol}",
                "/api/technicals/all",
                "/api/signals/rsi",
                "/api/signals/macd"
            ]
        }
    }

@app.get("/api/technicals/{symbol}", tags=["Technical Indicators"])
def get_symbol_technicals(symbol: str):
    """Get technical indicators for a specific stock symbol"""
    technicals = technicals_api.get_technicals_for_symbol(symbol)

    if not technicals:
        raise HTTPException(
            status_code=404,
            detail=f"No technical data found for symbol: {symbol}"
        )

    return {
        "symbol": symbol.upper(),
        "technicals": technicals,
        "last_updated": technicals.get('last_updated')
    }

@app.get("/api/technicals/all", tags=["Technical Indicators"])
def get_all_technicals_data():
    """Get technical indicators for all stocks"""
    data = technicals_api.get_all_technicals()

    return {
        "data": data,
        "count": len(data),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/signals/rsi", tags=["Signals"])
def get_rsi_signals(
    oversold: float = Query(30.0, ge=0, le=50, description="Oversold threshold"),
    overbought: float = Query(70.0, ge=50, le=100, description="Overbought threshold")
):
    """Get RSI signals (oversold/overbought stocks)"""
    signals = technicals_api.get_rsi_signals(oversold, overbought)

    return {
        "signals": signals,
        "oversold_count": len(signals["oversold"]),
        "overbought_count": len(signals["overbought"]),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/signals/macd", tags=["Signals"])
def get_macd_signals():
    """Get MACD crossover signals"""
    signals = technicals_api.get_macd_signals()

    return {
        "signals": signals,
        "bullish_count": len(signals["bullish_crossovers"]),
        "bearish_count": len(signals["bearish_crossovers"]),
        "last_updated": datetime.now().isoformat()
    }

@app.get("/api/technicals/search", tags=["Technical Indicators"])
def search_technicals(
    rsi_min: Optional[float] = Query(None, ge=0, le=100, description="Minimum RSI value"),
    rsi_max: Optional[float] = Query(None, ge=0, le=100, description="Maximum RSI value"),
    macd_signal: Optional[str] = Query(None, description="MACD signal state (bullish_crossover, bearish_crossover, neutral)"),
    limit: int = Query(50, ge=1, le=500, description="Maximum results to return")
):
    """Search technical indicators with filters"""
    all_data = technicals_api.get_all_technicals()
    results = []

    for symbol, technicals in all_data.items():
        # Apply RSI filter
        if rsi_min is not None and (technicals.get('rsi_14') is None or technicals['rsi_14'] < rsi_min):
            continue
        if rsi_max is not None and (technicals.get('rsi_14') is None or technicals['rsi_14'] > rsi_max):
            continue

        # Apply MACD signal filter
        if macd_signal:
            macd_data = technicals.get('macd', {})
            if macd_data.get('signal_state') != macd_signal:
                continue

        results.append({
            "symbol": symbol,
            "technicals": technicals
        })

        if len(results) >= limit:
            break

    return {
        "results": results,
        "count": len(results),
        "filters_applied": {
            "rsi_min": rsi_min,
            "rsi_max": rsi_max,
            "macd_signal": macd_signal
        },
        "last_updated": datetime.now().isoformat()
    }

@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint"""
    latest_file = technicals_api.get_latest_technicals_file()
    data_count = len(technicals_api.get_all_technicals())

    return {
        "status": "healthy" if data_count > 0 else "no_data",
        "timestamp": datetime.now().isoformat(),
        "data_available": data_count > 0,
        "total_stocks": data_count,
        "latest_file": latest_file.name if latest_file else None
    }

if __name__ == "__main__":
    print("🚀 Starting Technical Indicators API...")
    print("📊 API Documentation: http://localhost:8001/docs")
    print("🔄 Auto-loads latest technicals data from data/technicals/")

    uvicorn.run(app, host="0.0.0.0", port=8001)