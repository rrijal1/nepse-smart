"""
Database models for Portfolio and Watchlist management
"""
from sqlalchemy import Integer, String, Float, Date, Boolean, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base
from datetime import date, datetime
from typing import Optional

class Watchlist(Base):
    """
    Watchlist model to track stocks user is monitoring
    """
    __tablename__ = "watchlist"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    added_date: Mapped[date] = mapped_column(Date, default=date.today, nullable=False)
    favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Watchlist(symbol={self.symbol}, favorite={self.favorite})>"


class Portfolio(Base):
    """
    Portfolio model to track user's stock holdings
    """
    __tablename__ = "portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_price: Mapped[float] = mapped_column(Float, nullable=False)
    buy_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<Portfolio(symbol={self.symbol}, quantity={self.quantity}, avg_price={self.avg_price})>"

    @property
    def invested_amount(self) -> float:
        """Calculate total invested amount"""
        return float(self.quantity * self.avg_price)


class Transaction(Base):
    """
    Transaction model to track buy/sell history
    """
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    transaction_type: Mapped[str] = mapped_column(String(10), nullable=False)  # 'buy' or 'sell'
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Transaction(symbol={self.symbol}, type={self.transaction_type}, quantity={self.quantity})>"

    @property
    def total_amount(self) -> float:
        """Calculate total transaction amount"""
        return float(self.quantity * self.price)

class PaperPortfolio(Base):
    """
    Paper trading portfolio model
    """
    __tablename__ = "paper_portfolio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    avg_price: Mapped[float] = mapped_column(Float, nullable=False)
    buy_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<PaperPortfolio(user_id={self.user_id}, symbol={self.symbol}, quantity={self.quantity})>"

    @property
    def invested_amount(self) -> float:
        return float(self.quantity * self.avg_price)

class PaperTransaction(Base):
    """
    Paper trading transaction model
    """
    __tablename__ = "paper_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    transaction_type: Mapped[str] = mapped_column(String(10), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_date: Mapped[date] = mapped_column(Date, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PaperTransaction(user_id={self.user_id}, symbol={self.symbol}, type={self.transaction_type})>"

    @property
    def total_amount(self) -> float:
        return float(self.quantity * self.price)

class PaperAccount(Base):
    """
    Paper trading account model storing virtual cash for a user
    """
    __tablename__ = "paper_accounts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    initial_capital: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    cash_balance: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)

    def __repr__(self):
        return f"<PaperAccount(user_id={self.user_id}, cash_balance={self.cash_balance})>"


class PaperAccountFunding(Base):
    """
    Track when virtual cash was funded into a paper trading account.
    Kept as a separate table to avoid altering existing tables in place.
    """
    __tablename__ = "paper_account_funding"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    funded_amount: Mapped[float] = mapped_column(Float, nullable=False)
    funded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

class HistoricalPriceVolume(Base):
    """
    Historical price/volume data for NEPSE stocks
    """
    __tablename__ = "historical_price_volume"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    business_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    open_price: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    high_price: Mapped[float] = mapped_column(Float, nullable=False)
    low_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    total_trades: Mapped[int] = mapped_column(Integer, nullable=False)
    total_traded_quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    total_traded_value: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        {"schema": "nepse_data"}
    )

    def __repr__(self):
        return f"<HistoricalPriceVolume(symbol={self.symbol}, date={self.business_date}, close={self.close_price})>"
