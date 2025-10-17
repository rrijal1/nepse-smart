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
    apy_annualized: float = 0.0
    apy_since: Optional[datetime] = None

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

# Paper Trading Schemas
class PaperPortfolioBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20, description="Stock symbol")
    quantity: int = Field(..., gt=0, description="Number of shares")
    avg_price: float = Field(..., gt=0, description="Average price per share")
    buy_date: date = Field(..., description="Date of purchase")
    notes: Optional[str] = Field(None, description="Optional notes about the holding")

class PaperPortfolioCreate(PaperPortfolioBase):
    pass

class PaperPortfolioUpdate(BaseModel):
    quantity: Optional[int] = Field(None, gt=0)
    avg_price: Optional[float] = Field(None, gt=0)
    buy_date: Optional[date] = None
    notes: Optional[str] = None

class PaperPortfolioResponse(PaperPortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    invested_amount: float
    current_price: Optional[float] = None
    current_value: Optional[float] = None
    pnl: Optional[float] = None
    pnl_percent: Optional[float] = None

    class Config:
        from_attributes = True

class PaperTransactionBase(BaseModel):
    symbol: str = Field(..., min_length=1, max_length=20)
    transaction_type: str = Field(..., pattern="^(buy|sell)$")
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)
    transaction_date: date
    notes: Optional[str] = None

class PaperTransactionCreate(PaperTransactionBase):
    pass

class PaperTransactionResponse(PaperTransactionBase):
    id: int
    user_id: int
    total_amount: float
    created_at: datetime

    class Config:
        from_attributes = True

# Paper Account and Trade Schemas
class PaperAccountResponse(BaseModel):
    user_id: int
    initial_capital: float
    cash_balance: float
    created_at: datetime
    updated_at: Optional[datetime] = None
    funded_at: Optional[datetime] = None

class PaperAccountInitRequest(BaseModel):
    initial_capital: float

class PaperTradeRequest(BaseModel):
    symbol: str
    quantity: int
    side: str  # 'buy' or 'sell'
    notes: Optional[str] = None

class PaperTradeResponse(BaseModel):
    message: str
    symbol: str
    side: str
    quantity: int
    execution_price: float
    cash_balance: float

class PaperAccountFundingResponse(BaseModel):
    user_id: int
    funded_amount: float
    funded_at: datetime

class PaperApyResponse(BaseModel):
    apy_annualized: float
    since: Optional[datetime] = None
