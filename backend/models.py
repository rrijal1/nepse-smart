"""
Database models for Portfolio and Watchlist management
"""
from sqlalchemy import Integer, String, Float, Date, Boolean, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base
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
