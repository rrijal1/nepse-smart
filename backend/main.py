import sys
import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/api/market-status")
def get_market_status():
    """Check if NEPSE market is open"""
    try:
        is_open = nepse.isNepseOpen()
        return {"is_open": is_open}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)