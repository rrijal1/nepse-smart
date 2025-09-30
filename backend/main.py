import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from dateutil.parser import parse
import asyncio
import json
from starlette.responses import StreamingResponse


# Import the nepse module (installed as package)
try:
    from nepse import Nepse
except ImportError as e:
    print(f"Error importing Nepse: {e}")
    print("Make sure to install the nepse package: cd ../api && pip install -e .")
    sys.exit(1)

app = FastAPI(title="NEPSE Analytics API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NEPSE client
nepse = Nepse()
nepse.setTLSVerification(False)  # Temporary until NEPSE fixes SSL

@app.get("/")
def read_root():
    return {"message": "NEPSE Analytics API is running"}

@app.get("/api/market-status")
def get_market_status():
    """Check if NEPSE market is open"""
    try:
        is_open = nepse.isNepseOpen()
        return {"is_open": is_open}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/summary")
def get_market_summary():
    """Get market summary data"""
    try:
        summary_data = nepse.getSummary()
        return summary_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-gainers")
def get_top_gainers():
    """Get top gaining stocks"""
    try:
        gainers = nepse.getTopGainers()
        return gainers
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-losers")  
def get_top_losers():
    """Get top losing stocks"""
    try:
        losers = nepse.getTopLosers()
        return losers
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/nepse-index")
def get_nepse_index():
    """Get NEPSE index data"""
    try:
        index_data = nepse.getNepseIndex()
        return index_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/company-list")
def get_company_list():
    """Get list of all companies"""
    try:
        companies = nepse.getCompanyList()
        return companies
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/price-volume")
def get_price_volume(): 
    """Get price volume data for all stocks"""
    try:
        pricevolume = nepse.getPriceVolume()
        return pricevolume
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/company-price-volume-history")
def get_company_price_volume_history(symbol: str, start_date: str = None, end_date: str = None):
    """Get price volume history for a specific company"""
    try:
        # Validate and parse dates if provided
        start_date = parse(start_date).date() if start_date else None
        end_date = parse(end_date).date() if end_date else None
        pricevolume = nepse.getCompanyPriceVolumeHistory(symbol, start_date, end_date)
        return pricevolume
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid symbol: {symbol}")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def trending_stocks_generator():
    while True:
        try:
            gainers = nepse.getTopGainers()
            losers = nepse.getTopLosers()
            data = {"gainers": gainers, "losers": losers}
            yield f"data: {json.dumps(data)}\n\n"
            await asyncio.sleep(15)  # Update every 15 seconds
        except Exception as e:
            # Handle exceptions gracefully
            error_data = {"error": str(e)}
            yield f"data: {json.dumps(error_data)}\n\n"
            await asyncio.sleep(15)

@app.get("/api/trending-stocks-sse")
async def trending_stocks_sse():
    """SSE endpoint to stream top gainers and losers."""
    return StreamingResponse(trending_stocks_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)