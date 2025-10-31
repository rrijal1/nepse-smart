"""
Portfolio and Watchlist API Endpoints
Handles user portfolio management and watchlist operations
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime
import logging

from backend.database import get_db
from backend.models import Watchlist, Portfolio, Transaction
from backend.schemas import (
    WatchlistCreate, WatchlistUpdate, WatchlistResponse, WatchlistWithHoldings,
    PortfolioCreate, PortfolioUpdate, PortfolioResponse, PortfolioSummary,
    TransactionCreate, TransactionResponse
)
from backend.nepse_data_service import NepseDataService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api", tags=["Portfolio & Watchlist"])

# Initialize data service
nepse_data = NepseDataService(data_path="data")

# Helper function to get current price
def get_current_price(symbol: str) -> Optional[float]:
    """Get current price for a symbol from market data"""
    try:
        prices = nepse_data.get_price_volume()
        for stock in prices:
            if stock.get('symbol') == symbol:
                return stock.get('close')  # Use 'close' field from API
        return None
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None

def get_stock_data(symbol: str) -> dict:
    """Get comprehensive stock data including price, change, volume"""
    try:
        prices = nepse_data.get_price_volume()
        for stock in prices:
            if stock.get('symbol') == symbol:
                return {
                    'ltp': stock.get('close'),  # Use 'close' as LTP
                    'change': None,  # API doesn't provide change data
                    'change_percent': None,  # API doesn't provide percent change
                    'volume': str(stock.get('volume', 'N/A'))
                }
        return {}
    except Exception as e:
        logger.error(f"Error fetching stock data for {symbol}: {e}")
        return {}

# ==================== WATCHLIST ENDPOINTS ====================

@router.get("/watchlist", response_model=List[WatchlistWithHoldings])
def get_watchlist(db: Session = Depends(get_db)):
    """Get all watchlist items with live prices and holdings info"""
    try:
        watchlist_items = db.query(Watchlist).order_by(
            Watchlist.favorite.desc(),
            Watchlist.created_at.desc()
        ).all()
        
        result = []
        for item in watchlist_items:
            # Get live stock data
            stock_data = get_stock_data(item.symbol)
            
            # Get portfolio holdings if any
            portfolio_item = db.query(Portfolio).filter(
                Portfolio.symbol == item.symbol
            ).first()
            
            item_dict = {
                'id': item.id,
                'symbol': item.symbol,
                'added_date': item.added_date,
                'favorite': item.favorite,
                'notes': item.notes,
                'created_at': item.created_at,
                'ltp': stock_data.get('ltp'),
                'change': stock_data.get('change'),
                'change_percent': stock_data.get('change_percent'),
                'volume': stock_data.get('volume'),
                'holdings': portfolio_item.quantity if portfolio_item else None,
                'avg_holding_price': portfolio_item.avg_price if portfolio_item else None
            }
            result.append(item_dict)
        
        return result
    except Exception as e:
        logger.error(f"Error fetching watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/watchlist", response_model=WatchlistResponse, status_code=201)
def add_to_watchlist(
    watchlist_item: WatchlistCreate,
    db: Session = Depends(get_db)
):
    """Add a stock to watchlist"""
    try:
        # Check if already in watchlist
        existing = db.query(Watchlist).filter(
            Watchlist.symbol == watchlist_item.symbol.upper()
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"{watchlist_item.symbol} is already in watchlist"
            )
        
        # Create new watchlist item
        db_item = Watchlist(
            symbol=watchlist_item.symbol.upper(),
            added_date=date.today(),
            favorite=watchlist_item.favorite,
            notes=watchlist_item.notes
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        # Enrich with live data
        stock_data = get_stock_data(db_item.symbol)
        return {**db_item.__dict__, **stock_data}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding to watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/watchlist/{watchlist_id}", response_model=WatchlistResponse)
def update_watchlist_item(
    watchlist_id: int,
    update_data: WatchlistUpdate,
    db: Session = Depends(get_db)
):
    """Update watchlist item (favorite status, notes)"""
    try:
        item = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Watchlist item not found")
        
        # Update fields
        if update_data.favorite is not None:
            item.favorite = update_data.favorite
        if update_data.notes is not None:
            item.notes = update_data.notes
        
        db.commit()
        db.refresh(item)
        
        # Enrich with live data
        stock_data = get_stock_data(item.symbol)
        return {**item.__dict__, **stock_data}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/watchlist/{watchlist_id}", status_code=204)
def remove_from_watchlist(watchlist_id: int, db: Session = Depends(get_db)):
    """Remove a stock from watchlist"""
    try:
        item = db.query(Watchlist).filter(Watchlist.id == watchlist_id).first()
        
        if not item:
            raise HTTPException(status_code=404, detail="Watchlist item not found")
        
        db.delete(item)
        db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing from watchlist: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== PORTFOLIO ENDPOINTS ====================

@router.get("/portfolio", response_model=List[PortfolioResponse])
def get_portfolio(db: Session = Depends(get_db)):
    """Get all portfolio holdings with live prices and P&L"""
    try:
        holdings = db.query(Portfolio).order_by(Portfolio.symbol).all()
        
        result = []
        for holding in holdings:
            current_price = get_current_price(holding.symbol)
            
            item_dict = {
                'id': holding.id,
                'symbol': holding.symbol,
                'quantity': holding.quantity,
                'avg_price': holding.avg_price,
                'buy_date': holding.buy_date,
                'notes': holding.notes,
                'created_at': holding.created_at,
                'invested_amount': holding.invested_amount,
                'current_price': current_price,
                'current_value': holding.quantity * current_price if current_price else None,
                'pnl': (holding.quantity * current_price - holding.invested_amount) if current_price else None,
                'pnl_percent': ((current_price - holding.avg_price) / holding.avg_price * 100) if current_price else None
            }
            result.append(item_dict)
        
        return result
    except Exception as e:
        logger.error(f"Error fetching portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/portfolio", response_model=PortfolioResponse, status_code=201)
def add_to_portfolio(
    portfolio_item: PortfolioCreate,
    db: Session = Depends(get_db)
):
    """Add a new stock holding to portfolio"""
    try:
        # Check if already holding this stock
        existing = db.query(Portfolio).filter(
            Portfolio.symbol == portfolio_item.symbol.upper()
        ).first()
        
        if existing:
            # Update existing holding (average price calculation)
            total_quantity = existing.quantity + portfolio_item.quantity
            total_cost = (existing.quantity * existing.avg_price + 
                         portfolio_item.quantity * portfolio_item.avg_price)
            new_avg_price = total_cost / total_quantity
            
            existing.quantity = total_quantity
            existing.avg_price = new_avg_price
            existing.notes = portfolio_item.notes or existing.notes
            
            db.commit()
            db.refresh(existing)
            
            # Enrich with live data
            current_price = get_current_price(existing.symbol)
            response_data = {
                'id': existing.id,
                'symbol': existing.symbol,
                'quantity': existing.quantity,
                'avg_price': existing.avg_price,
                'buy_date': existing.buy_date,
                'notes': existing.notes,
                'created_at': existing.created_at,
                'invested_amount': existing.invested_amount,
                'current_price': current_price,
                'current_value': existing.quantity * current_price if current_price else None,
                'pnl': (existing.quantity * current_price - existing.invested_amount) if current_price else None,
                'pnl_percent': ((current_price - existing.avg_price) / existing.avg_price * 100) if current_price else None
            }
            return response_data
        
        # Create new holding
        db_item = Portfolio(
            symbol=portfolio_item.symbol.upper(),
            quantity=portfolio_item.quantity,
            avg_price=portfolio_item.avg_price,
            buy_date=portfolio_item.buy_date,
            notes=portfolio_item.notes
        )
        
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        
        # Create transaction record
        transaction = Transaction(
            symbol=db_item.symbol,
            transaction_type='buy',
            quantity=portfolio_item.quantity,
            price=portfolio_item.avg_price,
            transaction_date=portfolio_item.buy_date,
            notes=portfolio_item.notes
        )
        db.add(transaction)
        db.commit()
        
        # Enrich with live data
        current_price = get_current_price(db_item.symbol)
        response_data = {
            'id': db_item.id,
            'symbol': db_item.symbol,
            'quantity': db_item.quantity,
            'avg_price': db_item.avg_price,
            'buy_date': db_item.buy_date,
            'notes': db_item.notes,
            'created_at': db_item.created_at,
            'invested_amount': db_item.invested_amount,
            'current_price': current_price,
            'current_value': db_item.quantity * current_price if current_price else None,
            'pnl': (db_item.quantity * current_price - db_item.invested_amount) if current_price else None,
            'pnl_percent': ((current_price - db_item.avg_price) / db_item.avg_price * 100) if current_price else None
        }
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding to portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/portfolio/{portfolio_id}", response_model=PortfolioResponse)
def update_portfolio_holding(
    portfolio_id: int,
    update_data: PortfolioUpdate,
    db: Session = Depends(get_db)
):
    """Update portfolio holding details"""
    try:
        holding = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        
        if not holding:
            raise HTTPException(status_code=404, detail="Portfolio holding not found")
        
        # Update fields
        if update_data.quantity is not None:
            holding.quantity = update_data.quantity
        if update_data.avg_price is not None:
            holding.avg_price = update_data.avg_price
        if update_data.buy_date is not None:
            holding.buy_date = update_data.buy_date
        if update_data.notes is not None:
            holding.notes = update_data.notes
        
        db.commit()
        db.refresh(holding)
        
        # Enrich with live data
        current_price = get_current_price(holding.symbol)
        response_data = {
            'id': holding.id,
            'symbol': holding.symbol,
            'quantity': holding.quantity,
            'avg_price': holding.avg_price,
            'buy_date': holding.buy_date,
            'notes': holding.notes,
            'created_at': holding.created_at,
            'invested_amount': holding.invested_amount,
            'current_price': current_price,
            'current_value': holding.quantity * current_price if current_price else None,
            'pnl': (holding.quantity * current_price - holding.invested_amount) if current_price else None,
            'pnl_percent': ((current_price - holding.avg_price) / holding.avg_price * 100) if current_price else None
        }
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/portfolio/{portfolio_id}", status_code=204)
def remove_from_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Remove a holding from portfolio"""
    try:
        holding = db.query(Portfolio).filter(Portfolio.id == portfolio_id).first()
        
        if not holding:
            raise HTTPException(status_code=404, detail="Portfolio holding not found")
        
        # Create sell transaction record
        current_price = get_current_price(holding.symbol)
        if current_price:
            transaction = Transaction(
                symbol=holding.symbol,
                transaction_type='sell',
                quantity=holding.quantity,
                price=current_price,
                transaction_date=date.today(),
                notes=f"Removed from portfolio"
            )
            db.add(transaction)
        
        db.delete(holding)
        db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing from portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio/summary", response_model=PortfolioSummary)
def get_portfolio_summary(db: Session = Depends(get_db)):
    """Get portfolio summary with total value, P&L, etc."""
    try:
        holdings = db.query(Portfolio).all()
        
        total_invested = 0.0
        current_value = 0.0
        total_pnl = 0.0
        
        for holding in holdings:
            total_invested += holding.invested_amount
            
            current_price = get_current_price(holding.symbol)
            if current_price:
                holding_value = holding.quantity * current_price
                current_value += holding_value
                total_pnl += (holding_value - holding.invested_amount)
        
        total_pnl_percent = (total_pnl / total_invested * 100) if total_invested > 0 else 0.0
        
        # TODO: Calculate day's P&L by comparing with previous day's prices
        day_pnl = 0.0
        day_pnl_percent = 0.0
        
        return PortfolioSummary(
            total_invested=total_invested,
            current_value=current_value,
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_percent,
            day_pnl=day_pnl,
            day_pnl_percent=day_pnl_percent,
            total_holdings=len(holdings),
            cash_available=0.0  # TODO: Implement cash management
        )
        
    except Exception as e:
        logger.error(f"Error calculating portfolio summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ==================== TRANSACTION ENDPOINTS ====================

@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    symbol: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get transaction history"""
    try:
        query = db.query(Transaction)
        
        if symbol:
            query = query.filter(Transaction.symbol == symbol.upper())
        
        transactions = query.order_by(
            Transaction.transaction_date.desc()
        ).limit(limit).all()
        
        return transactions
        
    except Exception as e:
        logger.error(f"Error fetching transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transactions", response_model=TransactionResponse, status_code=201)
def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Manually add a transaction record"""
    try:
        db_transaction = Transaction(
            symbol=transaction.symbol.upper(),
            transaction_type=transaction.transaction_type,
            quantity=transaction.quantity,
            price=transaction.price,
            transaction_date=transaction.transaction_date,
            notes=transaction.notes
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        return db_transaction
        
    except Exception as e:
        db.rollback()
        logger.error(f"Error adding transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))
