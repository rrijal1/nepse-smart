"""FastAPI router exposing LangChain-based agent capabilities under the core backend."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agent_service import (
    answer_natural_language_question,
    perform_stock_analysis,
)
from nepse_data_service import NepseDataService
from pathlib import Path
import json
from datetime import datetime

router = APIRouter(prefix="/agent", tags=["Agent"])

# Resolve absolute data path to avoid CWD differences (e.g., /app vs /app/backend)
_DATA_DIR = str((Path("/app") / "data").resolve())

def _symbols_from_prices_fallback(data_dir: str) -> list[str]:
    """Read latest *_prices.json directly and extract symbols (fallback path)."""
    try:
        daily = Path(data_dir) / "daily"
        files = sorted(daily.glob("*_prices.json"), key=lambda p: p.name, reverse=True)
        if not files:
            return []
        with open(files[0], "r", encoding="utf-8") as f:
            data = json.load(f)
        symbols = sorted({str(item.get("symbol")) for item in data if item.get("symbol")})
        return symbols
    except Exception:
        return []

def _read_agent_metrics(data_dir: str) -> dict:
    daily = Path(data_dir) / "daily"
    # try today's file first
    today = datetime.now().strftime("%Y-%m-%d")
    candidates = [daily / f"{today}_agent_metrics.json"]
    # fallback: any *_agent_metrics.json (latest)
    candidates += sorted(daily.glob("*_agent_metrics.json"), key=lambda p: p.name, reverse=True)
    for path in candidates:
        if path.exists():
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                continue
    return {}


class StockRequest(BaseModel):
    stock_symbol: str


class QuestionRequest(BaseModel):
    question: str


@router.get("/stocks")
def get_available_stocks() -> dict:
    """Expose the list of currently active stocks (symbols only)."""
    # Fresh service instance to avoid stale cache between reloads
    svc = NepseDataService(data_path=_DATA_DIR)
    companies = svc.get_company_list() or []
    if not companies:
        # Fallback: read directly from today's prices
        symbols = _symbols_from_prices_fallback(_DATA_DIR)
    else:
        symbols = sorted([str(c.get("symbol")) for c in companies if c.get("symbol")])
    if not symbols:
        symbols = _symbols_from_prices_fallback(_DATA_DIR)
    # Fallback to mock if empty
    if not symbols:
        symbols = ["NABIL", "ADBL", "EBL"]
    return {"available_stocks": symbols}


@router.get("/metrics")
def get_agent_metrics() -> dict:
    """Return the pre-generated per-symbol agent metrics from daily file."""
    data = _read_agent_metrics(_DATA_DIR)
    return {"count": len(data), "data": data}


@router.get("/metrics/{symbol}")
def get_agent_metrics_for_symbol(symbol: str) -> dict:
    """Return metrics for a single symbol from the daily file, 404 if missing."""
    data = _read_agent_metrics(_DATA_DIR)
    sym = symbol.upper()
    if sym not in data:
        raise HTTPException(status_code=404, detail=f"No metrics found for {sym}")
    return {"symbol": sym, "data": data[sym]}


@router.post("/analyze")
def analyze_stock(request: StockRequest) -> dict:
    """Run multi-agent analysis for the requested stock."""
    if not request.stock_symbol:
        raise HTTPException(status_code=400, detail="Stock symbol is required")
    return perform_stock_analysis(request.stock_symbol)


@router.post("/ask")
def ask_question(request: QuestionRequest) -> dict:
    """Answer a natural language question about NEPSE stocks."""
    if not request.question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    return answer_natural_language_question(request.question)
