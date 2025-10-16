"""FastAPI router exposing LangChain-based agent capabilities under the core backend."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agent_service import (
    answer_natural_language_question,
    list_available_stocks,
    perform_stock_analysis,
)

router = APIRouter(prefix="/agent", tags=["Agent"])


class StockRequest(BaseModel):
    stock_symbol: str


class QuestionRequest(BaseModel):
    question: str


@router.get("/stocks")
def get_available_stocks() -> dict:
    """Expose the list of stocks supported by the agent system."""
    return {"available_stocks": list_available_stocks()}


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
