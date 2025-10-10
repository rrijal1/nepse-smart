import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from dateutil.parser import parse
import asyncio
import json
from starlette.responses import StreamingResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

# Import NEPSE Smart agent routes
try:
    from agent_routes import router as agent_router
    NEPSE_AGENTS_AVAILABLE = True
    print("✅ NEPSE Smart agents enabled")
except ImportError as e:
    print(f"Warning: NEPSE agent routes not available: {e}")
    NEPSE_AGENTS_AVAILABLE = False


# Import the nepse module (installed as package)
try:
    from nepse import Nepse
    NEPSE_MODULE_AVAILABLE = True
    print("✅ NEPSE module loaded successfully")
except ImportError as e:
    print(f"Warning: NEPSE module not available: {e}")
    print("Using mock data for development - install nepse package for real data")
    NEPSE_MODULE_AVAILABLE = False
    # Create mock Nepse class for development
    class Nepse:
        def setTLSVerification(self, value): pass
        def isNepseOpen(self): return True
        def getSummary(self): return {"status": "mock_data"}
        def getTopGainers(self): return []
        def getTopLosers(self): return []
        def getNepseIndex(self): return {"value": 2000}
        def getCompanyList(self): return []
        def getPriceVolume(self): return []
        def getCompanyPriceVolumeHistory(self, symbol, start=None, end=None): return []

app = FastAPI(title="NEPSE Analytics API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include NEPSE Smart agent routes
if NEPSE_AGENTS_AVAILABLE:
    app.include_router(agent_router)  # Use tags from agent_routes.py
    print("✅ NEPSE Smart agents enabled")
else:
    print("⚠️ NEPSE Smart agents disabled - check agent imports")

# Initialize NEPSE client
nepse = Nepse()
nepse.setTLSVerification(False)  # Temporary until NEPSE fixes SSL

@app.get("/", tags=["System"])
def read_root():
    return {"message": "NEPSE Analytics API is running"}

@app.get("/api/market-status", tags=["Market Data"])
def get_market_status():
    """Check if NEPSE market is open"""
    try:
        is_open = nepse.isNepseOpen()
        return {"is_open": is_open}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/summary", tags=["Market Data"])
def get_market_summary():
    """Get market summary data"""
    try:
        summary_data = nepse.getSummary()
        return summary_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-gainers", tags=["Market Data"])
def get_top_gainers():
    """Get top gaining stocks"""
    try:
        gainers = nepse.getTopGainers()
        return gainers
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/top-losers", tags=["Market Data"])
def get_top_losers():
    """Get top losing stocks"""
    try:
        losers = nepse.getTopLosers()
        return losers
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/nepse-index", tags=["Market Data"])
def get_nepse_index():
    """Get NEPSE index data"""
    try:
        index_data = nepse.getNepseIndex()
        return index_data
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/company-list", tags=["Market Data"])
def get_company_list():
    """Get list of all companies"""
    try:
        companies = nepse.getCompanyList()
        return companies
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/price-volume", tags=["Market Data"])
def get_price_volume(): 
    """Get price volume data for all stocks"""
    try:
        pricevolume = nepse.getPriceVolume()
        return pricevolume
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/company-price-volume-history", tags=["Market Data"])
def get_company_price_volume_history(symbol: str, start_date: str | None = None, end_date: str | None = None):
    """Get price volume history for a specific company"""
    try:
        # Validate and parse dates if provided
        start_parsed = parse(start_date).date() if start_date else None
        end_parsed = parse(end_date).date() if end_date else None
        pricevolume = nepse.getCompanyPriceVolumeHistory(symbol, start_parsed, end_parsed)
        return pricevolume
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid symbol: {symbol}")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def trending_stocks_generator():
    last_data = None
    error_count = 0
    
    while True:
        try:
            gainers = nepse.getTopGainers()
            losers = nepse.getTopLosers()
            current_data = {"gainers": gainers, "losers": losers, "timestamp": asyncio.get_event_loop().time()}
            
            # Only send data if it has changed or if it's the first time
            if last_data is None or current_data != last_data:
                yield f"data: {json.dumps(current_data)}\n\n"
                last_data = current_data
                error_count = 0  # Reset error count on successful fetch
                print(f"SSE: Sent updated data - {len(gainers) if gainers else 0} gainers, {len(losers) if losers else 0} losers")
            else:
                # Send heartbeat to keep connection alive
                yield f"event: heartbeat\ndata: {json.dumps({'status': 'alive'})}\n\n"
                
            await asyncio.sleep(12)  # Reduced to 12 seconds for better real-time feel
            
        except Exception as e:
            error_count += 1
            print(f"SSE Error (attempt {error_count}): {e}")
            
            # Send error data
            error_data = {"error": str(e), "retry_after": min(5 * error_count, 30)}
            yield f"data: {json.dumps(error_data)}\n\n"
            
            # Exponential backoff on errors
            await asyncio.sleep(min(5 * error_count, 30))

@app.get("/api/trending-stocks-sse", tags=["Real-time Streaming"])
async def trending_stocks_sse():
    """SSE endpoint to stream top gainers and losers."""
    return StreamingResponse(
        trending_stocks_generator(), 
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )

@app.websocket("/ws/trending-stocks")
async def websocket_trending_stocks(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket client connected")
    
    try:
        # Send the first message immediately
        try:
            gainers = nepse.getTopGainers()
            losers = nepse.getTopLosers()
            data = {
                "gainers": gainers, 
                "losers": losers,
                "timestamp": asyncio.get_event_loop().time()
            }
            await websocket.send_json(data)
            print("Initial data sent to WebSocket client")
        except Exception as e:
            error_data = {"error": f"Failed to fetch initial data: {str(e)}"}
            await websocket.send_json(error_data)

        while True:
            await asyncio.sleep(10)  # Reduced to 10 seconds for more real-time feel
            try:
                gainers = nepse.getTopGainers()
                losers = nepse.getTopLosers()
                data = {
                    "gainers": gainers, 
                    "losers": losers,
                    "timestamp": asyncio.get_event_loop().time()
                }
                await websocket.send_json(data)
                print(f"Updated data sent: {len(gainers) if gainers else 0} gainers, {len(losers) if losers else 0} losers")
            except Exception as e:
                print(f"Error fetching trending stocks: {e}")
                error_data = {"error": f"Failed to fetch data: {str(e)}"}
                await websocket.send_json(error_data)
                
    except WebSocketDisconnect:
        print("WebSocket client disconnected")
    except Exception as e:
        print(f"Unexpected WebSocket error: {e}")
        try:
            await websocket.close()
        except:
            pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)