"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# Watchlist Schemas
class WatchlistBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Stock symbol")
    favorite: bool = Field(default=False, description="Is this stock a favorite")
    notes: Optional[str] = Field(None, description="Optional notes about the stock")

class WatchlistCreate(WatchlistBase):
    pass

class WatchlistUpdate(BaseModel):
    favorite: Optional[bool] = None
    notes: Optional[str] = None

class WatchlistResponse(WatchlistBase):
    id: int
    added_date: date
    created_at: datetime
    
    # Live price data (enriched from API)
    ltp: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[str] = None

    class Config:
        from_attributes = True

# Portfolio Schemas
class PortfolioBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Stock symbol")
    quantity: int = Field(..., gt=0, description="Number of shares")
    avg_price: float = Field(..., gt=0, description="Average price per share")
    buy_date: date = Field(..., description="Date of purchase")
    notes: Optional[str] = Field(None, description="Optional notes about the holding")

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    avg_price: Optional[float] = Field(None, gt=0)
    buy_date: Optional[date] = None
    notes: Optional[str] = None

class PortfolioResponse(PortfolioBase):
    id: int
    created_at: datetime
    invested_amount: float
    
    # Live price data (enriched from API)
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None

    class Config:
        from_attributes = True

# Portfolio Summary Schema
class PortfolioSummary(BaseModel):
    total_invested: float
    current_value: float
    total_pnl: float
    total_pnl_percent: float
    day_pnl: float
    day_pnl_percent: float
    total_holdings: int
    cash_available: float = 0.0

# Transaction Schemas
class TransactionBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    transaction_type: str = Field(..., pattern="^(buy|sell)$")
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    transaction_date: date
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True

# Watchlist with Holdings Info
class WatchlistWithHoldings(WatchlistResponse):
    holdings: Optional[int] = None
    avg_holding_price: Optional[float] = None
