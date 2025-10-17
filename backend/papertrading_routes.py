"""
Paper Trading API Endpoints
Handles paper trading portfolio management and transactions
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
import logging

from backend.database import get_db
from backend.models import PaperPortfolio, PaperTransaction, PaperAccount, PaperAccountFunding
from backend.schemas import (
    PaperPortfolioCreate, PaperPortfolioUpdate, PaperPortfolioResponse,
    PaperTransactionCreate, PaperTransactionResponse
)
from backend.schemas import PortfolioSummary, PaperAccountResponse, PaperAccountInitRequest, PaperTradeRequest, PaperTradeResponse, PaperAccountFundingResponse, PaperApyResponse
from backend.nepse_data_service import NepseDataService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/paper-trading", tags=["Paper Trading"])

# Initialize data service
nepse_data = NepseDataService(data_path="data")

# Helper function to get current price
def get_current_price(symbol: str) -> Optional[float]:
    """Get current price for a symbol from market data"""
    try:
        prices = nepse_data.get_price_volume()
        for stock in prices:
            if stock.get('symbol') == symbol:
                return stock.get('ltp') or stock.get('close_price')
        return None
    except Exception as e:
        logger.error(f"Error fetching price for {symbol}: {e}")
        return None

def _get_or_create_account(db: Session, user_id: int = 1) -> PaperAccount:
    """Simple user scoping placeholder: defaults to user_id=1."""
    acct = db.query(PaperAccount).filter(PaperAccount.user_id == user_id).first()
    if not acct:
        # Start at zero until user opts in
        acct = PaperAccount(user_id=user_id, initial_capital=0.0, cash_balance=0.0)
        db.add(acct)
        db.commit()
        db.refresh(acct)
    return acct

@router.get("/account", response_model=PaperAccountResponse)
def get_paper_account(db: Session = Depends(get_db)):
    acct = _get_or_create_account(db)
    funded = db.query(PaperAccountFunding).filter(PaperAccountFunding.user_id == acct.user_id).order_by(PaperAccountFunding.funded_at.asc()).first()
    # Backfill funding record if account has balance but no funding entry (migration-safe)
    if not funded and acct.initial_capital > 0:
        funding = PaperAccountFunding(user_id=acct.user_id, funded_amount=acct.initial_capital)
        db.add(funding)
        db.commit()
        db.refresh(funding)
        funded = funding
    return PaperAccountResponse(
        user_id=acct.user_id,
        initial_capital=acct.initial_capital,
        cash_balance=acct.cash_balance,
        created_at=acct.created_at,
        updated_at=acct.updated_at,
        funded_at=funded.funded_at if funded else None,
    )

@router.post("/account/init", response_model=PaperAccountResponse)
def init_paper_account(payload: PaperAccountInitRequest, db: Session = Depends(get_db)):
    """One-time setup of initial capital if account is new (MVP: overwrite allowed)."""
    acct = _get_or_create_account(db)
    acct.initial_capital = float(payload.initial_capital)
    acct.cash_balance = float(payload.initial_capital)
    db.commit()
    db.refresh(acct)
    # Record funding event
    funding = PaperAccountFunding(user_id=acct.user_id, funded_amount=acct.initial_capital)
    db.add(funding)
    db.commit()
    return PaperAccountResponse(
        user_id=acct.user_id,
        initial_capital=acct.initial_capital,
        cash_balance=acct.cash_balance,
        created_at=acct.created_at,
        updated_at=acct.updated_at,
        funded_at=funding.funded_at,
    )

@router.post("/account/fund", response_model=PaperAccountFundingResponse)
def fund_paper_account(db: Session = Depends(get_db)):
    """CTA: Fund the paper account with 10 lakhs if balance is zero."""
    acct = _get_or_create_account(db)
    if acct.cash_balance > 0 or acct.initial_capital > 0:
        raise HTTPException(status_code=400, detail="Account already funded")
    acct.initial_capital = 5_000_000.0
    acct.cash_balance = 5_000_000.0
    db.commit()
    db.refresh(acct)
    funding = PaperAccountFunding(user_id=acct.user_id, funded_amount=acct.initial_capital)
    db.add(funding)
    db.commit()
    db.refresh(funding)
    return PaperAccountFundingResponse(user_id=acct.user_id, funded_amount=funding.funded_amount, funded_at=funding.funded_at)

@router.post("/account/reset", response_model=PaperAccountResponse)
def reset_paper_account(db: Session = Depends(get_db)):
    """Reset paper account to zero and clear paper holdings/transactions/funding."""
    acct = _get_or_create_account(db)
    # Clear portfolio and transactions
    db.query(PaperTransaction).delete()
    db.query(PaperPortfolio).delete()
    db.query(PaperAccountFunding).filter(PaperAccountFunding.user_id == acct.user_id).delete()
    # Zero balances
    acct.initial_capital = 0.0
    acct.cash_balance = 0.0
    db.commit()
    db.refresh(acct)
    return PaperAccountResponse(
        user_id=acct.user_id,
        initial_capital=acct.initial_capital,
        cash_balance=acct.cash_balance,
        created_at=acct.created_at,
        updated_at=acct.updated_at,
        funded_at=None,
    )

@router.post("/trade", response_model=PaperTradeResponse)
def paper_trade(req: PaperTradeRequest, db: Session = Depends(get_db)):
    """Execute a paper trade at current market price (virtual cash only)."""
    symbol = req.symbol.upper()
    if req.side not in {"buy", "sell"}:
        raise HTTPException(status_code=400, detail="side must be 'buy' or 'sell'")

    price = get_current_price(symbol)
    if price is None:
        raise HTTPException(status_code=400, detail=f"No market price available for {symbol}")

    acct = _get_or_create_account(db)
    qty = int(req.quantity)
    if qty <= 0:
        raise HTTPException(status_code=400, detail="quantity must be > 0")

    if req.side == "buy":
        cost = qty * price
        if acct.cash_balance < cost:
            raise HTTPException(status_code=400, detail="Insufficient virtual cash")

        # Upsert holding
        holding = db.query(PaperPortfolio).filter(PaperPortfolio.symbol == symbol).first()
        if holding:
            total_qty = holding.quantity + qty
            total_cost = holding.avg_price * holding.quantity + cost
            holding.quantity = total_qty
            holding.avg_price = total_cost / total_qty
        else:
            holding = PaperPortfolio(
                symbol=symbol,
                quantity=qty,
                avg_price=price,
                buy_date=date.today(),
                notes=req.notes or None,
            )
            db.add(holding)

        acct.cash_balance -= cost

        # Record transaction
        tx = PaperTransaction(
            symbol=symbol,
            transaction_type='buy',
            quantity=qty,
            price=price,
            transaction_date=date.today(),
            notes=req.notes or None,
        )
        db.add(tx)

    else:  # sell
        holding = db.query(PaperPortfolio).filter(PaperPortfolio.symbol == symbol).first()
        if not holding or holding.quantity < qty:
            raise HTTPException(status_code=400, detail="Not enough shares to sell")
        proceeds = qty * price
        holding.quantity -= qty
        if holding.quantity == 0:
            db.delete(holding)
        acct.cash_balance += proceeds

        tx = PaperTransaction(
            symbol=symbol,
            transaction_type='sell',
            quantity=qty,
            price=price,
            transaction_date=date.today(),
            notes=req.notes or None,
        )
        db.add(tx)

    db.commit()
    db.refresh(acct)
    return PaperTradeResponse(
        message="Executed",
        symbol=symbol,
        side=req.side,
        quantity=qty,
        execution_price=price,
        cash_balance=acct.cash_balance,
    )

@router.get("/portfolio/summary", response_model=PortfolioSummary)
def get_paper_portfolio_summary(db: Session = Depends(get_db)):
    """Get paper portfolio summary with total value, P&L, etc."""
    try:
        holdings = db.query(PaperPortfolio).all()
        acct = _get_or_create_account(db)

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

        # Optional APY: if funded_at exists, estimate annualized return from cash+current_value vs initial
        funded = db.query(PaperAccountFunding).filter(PaperAccountFunding.user_id == acct.user_id).order_by(PaperAccountFunding.funded_at.asc()).first()
        apy_annualized = 0.0
        apy_since = None
        if funded and funded.funded_at and acct.initial_capital > 0:
            total_equity = acct.cash_balance + current_value
            pnl_since = total_equity - acct.initial_capital
            days = max((date.today() - funded.funded_at.date()).days, 1)
            # Simple annualized return approximation
            daily_return = pnl_since / acct.initial_capital / days
            apy_annualized = daily_return * 365 * 100
            apy_since = funded.funded_at

        return PortfolioSummary(
            total_invested=total_invested,
            current_value=current_value,
            total_pnl=total_pnl,
            total_pnl_percent=total_pnl_percent,
            day_pnl=day_pnl,
            day_pnl_percent=day_pnl_percent,
            total_holdings=len(holdings),
            cash_available=acct.cash_balance,
            apy_annualized=apy_annualized,
            apy_since=apy_since,
        )
    except Exception as e:
        logger.error(f"Error calculating paper portfolio summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/portfolio", response_model=List[PaperPortfolioResponse])
def get_paper_portfolio(db: Session = Depends(get_db)):
    """Get all paper portfolio holdings with live prices and P&L"""
    try:
        holdings = db.query(PaperPortfolio).order_by(PaperPortfolio.symbol).all()
        
        result = []
        for holding in holdings:
            current_price = get_current_price(holding.symbol)
            
            item_dict = {
                'id': holding.id,
                'user_id': holding.user_id,
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
        logger.error(f"Error fetching paper portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/portfolio", response_model=PaperPortfolioResponse, status_code=201)
def add_to_paper_portfolio(
    portfolio_item: PaperPortfolioCreate,
    db: Session = Depends(get_db)
):
    """Add a new stock holding to paper portfolio"""
    try:
        # Check if already holding this stock
        existing = db.query(PaperPortfolio).filter(
            PaperPortfolio.symbol == portfolio_item.symbol.upper()
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
            db_item = existing
        else:
            # Create new holding
            db_item = PaperPortfolio(
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
        transaction = PaperTransaction(
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
            'user_id': db_item.user_id,
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
        logger.error(f"Error adding to paper portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/portfolio/{portfolio_id}", response_model=PaperPortfolioResponse)
def update_paper_portfolio_holding(
    portfolio_id: int,
    update_data: PaperPortfolioUpdate,
    db: Session = Depends(get_db)
):
    """Update paper portfolio holding details"""
    try:
        holding = db.query(PaperPortfolio).filter(PaperPortfolio.id == portfolio_id).first()
        
        if not holding:
            raise HTTPException(status_code=404, detail="Paper portfolio holding not found")
        
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
            'user_id': holding.user_id,
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
        logger.error(f"Error updating paper portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/portfolio/{portfolio_id}", status_code=204)
def remove_from_paper_portfolio(portfolio_id: int, db: Session = Depends(get_db)):
    """Remove a holding from paper portfolio"""
    try:
        holding = db.query(PaperPortfolio).filter(PaperPortfolio.id == portfolio_id).first()
        
        if not holding:
            raise HTTPException(status_code=404, detail="Paper portfolio holding not found")
        
        # Create sell transaction record
        current_price = get_current_price(holding.symbol)
        if current_price:
            transaction = PaperTransaction(
                symbol=holding.symbol,
                transaction_type='sell',
                quantity=holding.quantity,
                price=current_price,
                transaction_date=date.today(),
                notes=f"Removed from paper portfolio"
            )
            db.add(transaction)
        
        db.delete(holding)
        db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error removing from paper portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/transactions", response_model=List[PaperTransactionResponse])
def get_paper_transactions(
    symbol: Optional[str] = None,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get paper transaction history"""
    try:
        query = db.query(PaperTransaction)
        
        if symbol:
            query = query.filter(PaperTransaction.symbol == symbol.upper())
        
        transactions = query.order_by(
            PaperTransaction.transaction_date.desc()
        ).limit(limit).all()
        
        return transactions
        
    except Exception as e:
        logger.error(f"Error fetching paper transactions: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transactions", response_model=PaperTransactionResponse, status_code=201)
def add_paper_transaction(
    transaction: PaperTransactionCreate,
    db: Session = Depends(get_db)
):
    """Manually add a paper transaction record"""
    try:
        db_transaction = PaperTransaction(
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
        logger.error(f"Error adding paper transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))