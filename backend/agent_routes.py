"""FastAPI router exposing LangChain-based agent capabilities under the core backend."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.agent_service import (
    answer_natural_language_question,
    perform_stock_analysis,
)
from backend.nepse_data_service import NepseDataService
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
