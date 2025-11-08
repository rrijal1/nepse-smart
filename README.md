# NEPSE Smart - Complete Stock Market Data Platform

[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://docker.com)
[![Python](https://img.shields.io/badge/python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://python.org)
[![Vue.js](https://img.shields.io/badge/vuejs-%2335495e.svg?style=flat&logo=vuedotjs&logoColor=%234FC08D)](https://vuejs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/postgresql-%23316192.svg?style=flat&logo=postgresql&logoColor=white)](https://postgresql.org)

A comprehensive, production-ready platform for scraping, analyzing, and trading Nepal Stock Exchange (NEPSE) data with automated daily collection, real-time APIs, and advanced analytics.

## ✨ Features

### 📊 **Data Collection & Management**

- **Automated Daily Scraping** - Runs at midnight via GitHub Actions
- **Comprehensive Market Data** - Prices, floorsheet, indices, exchange rates, banking indicators, short-term rates
- **Dual Storage System** - PostgreSQL + JSON (GitHub-friendly)
- **Historical Database** - Complete market history with bulk collection (113K+ records)
- **Data Aggregation** - Consolidated analytics for backtesting
- **Smart Cleanup** - Manual JSON file cleanup to keep repository lean (PostgreSQL data permanent)

### 🎯 **Trading & Analysis**

- **Paper Trading** - Virtual Rs. 50L account with live market execution
- **Portfolio Management** - Track holdings, P&L, and watchlists
- **AI Agent** - Natural language Q&A and per-symbol analysis
- **Technical Indicators** - RSI, MACD signals, and comprehensive technical analysis
- **Real-time APIs** - FastAPI backend with comprehensive endpoints
- **Advanced Search** - Filter stocks by technical indicators and fundamentals

### 🏗️ **Developer Experience**

- **Docker Ready** - One-command setup with docker-compose
- **Graceful Degradation** - Works with or without database
- **GitHub Integration** - Automated CI/CD workflows
- **Modern Stack** - Vue 3, FastAPI, PostgreSQL, TypeScript
- **API Documentation** - Auto-generated Swagger/OpenAPI docs

## ✅ System Status

**🟢 FULLY OPERATIONAL** - All features implemented and tested

- **Database**: PostgreSQL with comprehensive market data
  - 55,442+ historical price-volume records (OHLCV data for all stocks)
  - Complete market indices, floorsheet, and macroeconomic data
  - Portfolio and paper trading data with full transaction history
- **API Endpoints**: All documented endpoints functional with comprehensive error handling
- **Data Management**: Migration, manual cleanup, and quality monitoring (PostgreSQL data permanent)
- **Dual Storage**: JSON (GitHub) + PostgreSQL (performance) with seamless sync
- **Technical Indicators**: RSI, MACD, and signal generation fully operational
- **AI Agent**: Natural language analysis and Q&A capabilities
- **Docker**: Optimized containers with Python 3.11 and uv package manager
- **Testing**: All core functionality verified and production-ready

## 🚀 Quick Start

### Option 1: Docker Setup (Recommended)

```bash
# 1. Clone and setup
git clone <repository-url>
cd nepse-smart

# 2. Start all services
docker-compose up --build

# 3. Initialize database (first time only)
docker-compose exec backend python3 init_db.py

# 4. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt
cd data-scraper && pip install -r requirements.txt

# 2. Start PostgreSQL (optional)
docker-compose up -d postgres

# 3. Initialize database (if using PostgreSQL)
cd backend && python init_db.py

# 4. Start services
# Backend (Terminal 1)
cd backend && python main.py

# Frontend (Terminal 2)
cd frontend && npm install && npm run dev

# Data collection (Terminal 3)
cd data-scraper && python production_main.py --scraper all
```

### Option 3: Portfolio Only Setup

```bash
# Quick portfolio setup (database + basic features)
./setup_portfolio.sh
```

## 📊 Data Collection

### Automated Scraping

```bash
cd data-scraper

# Run all scrapers
python production_main.py --scraper all

# Individual scrapers
python production_main.py --scraper official_api    # Security lists, market data
python production_main.py --scraper prices          # Stock prices
python production_main.py --scraper macro           # Economic indicators
```

### On-Demand Migration

```bash
# Via API
curl -X POST http://localhost:8000/api/data/migrate

# Or via data manager
cd data-scraper
python -c "from data_manager import DataManager; dm = DataManager(); print(dm.migrate_json_to_postgres())"
```

### Manual JSON File Cleanup

To clean up old JSON files in `data/daily/` directory (keeping PostgreSQL data intact):

```bash
# Using the safe cleanup script (recommended)
python scripts/cleanup_json.py 30

# Or directly via data manager
cd data-scraper
python -c "
from data_manager import DataManager
dm = DataManager()
result = dm.cleanup_old_data(keep_days=30)
print(f'Cleanup completed: {result}')
"
```

**Note**: This only removes JSON files older than 30 days. PostgreSQL data is never automatically deleted and remains permanent.

### Data Sources

| Data Type                | Source         | Frequency | Storage           | Status                                            |
| ------------------------ | -------------- | --------- | ----------------- | ------------------------------------------------- |
| **Stock Prices**         | ShareSansar    | Daily     | JSON + PostgreSQL | ✅ 55,442+ records (JSON: 30 days, DB: permanent) |
| **Market Indices**       | NEPSE Official | Daily     | JSON + PostgreSQL | ✅ Active                                         |
| **Floorsheet**           | NEPSE Official | Daily     | JSON + PostgreSQL | ✅ Active                                         |
| **Company Lists**        | NEPSE Official | Daily     | JSON (lookup)     | ✅ Active                                         |
| **Macro Data**           | NRB            | Daily     | JSON + PostgreSQL | ✅ Active                                         |
| **Technical Indicators** | Generated      | Daily     | JSON              | ✅ Active                                         |
| **Historical OHLCV**     | NEPSE Official | On-demand | PostgreSQL        | ✅ Migrated                                       |

### Data Architecture

The system uses a **three-tier data storage strategy**:

#### 1️⃣ **Primary: PostgreSQL Database** (Source of Truth)

- All historical market data (prices, floorsheet, indices, macro)
- Queried by backend for all historical data requests
- Complete trading history since 2024 (55,442+ records)
- Never automatically deleted - permanent storage

#### 2️⃣ **Secondary: Active JSON Files** (Recent + Fallback)

- `data/daily/` - Last 7 business days of market data
- `data/lookup/` - Last 7 business days of reference data
- Used as fallback when database unavailable
- **Tracked in Git** for immediate deployment readiness
- Automatically archived after 7 days

#### 3️⃣ **Tertiary: Archive** (Backup Only)

- `data/archive/` - Historical JSON files organized by year/month
- **NOT queried by the application**
- **NOT tracked in Git** (excluded via `.gitignore`)
- Kept for disaster recovery and auditing
- Can be used to restore PostgreSQL if needed
- See `data/archive/README.md` for details

**Data Flow:**

```
GitHub Actions Scraper
    ↓
Saves to data/daily/ (JSON) ← Backend fallback
    ↓
Saves to PostgreSQL ← Backend primary
    ↓
After 7 days: Archived to data/archive/ (backup only)
```

## 🔌 API Reference

### Market Data Endpoints

```
GET /api/summary              # Market overview
GET /api/top-gainers          # Top gaining stocks
GET /api/top-losers           # Top losing stocks
GET /api/nepse-index          # NEPSE index data
GET /api/sub-indices          # Sector indices
GET /api/price-volume         # Current prices & volume
GET /api/company-list         # All listed companies
GET /api/macro-data           # Economic indicators
GET /api/market-status        # Market open/closed status
```

### Historical Data

```
GET /api/historical/{data_type}?days=30    # Historical data (prices/indices/macro/floorsheet)
GET /api/company-history/{symbol}?days=30  # Individual stock history
```

### Technical Indicators

```
GET /api/technicals/{symbol}           # Technicals for specific stock
GET /api/technicals/all                # Technicals for all stocks
GET /api/signals/rsi                   # RSI signals (oversold/overbought)
GET /api/signals/macd                  # MACD crossover signals
GET /api/technicals/search             # Search technicals with filters
```

### Portfolio Management

```
GET    /api/watchlist                  # Get watchlist
POST   /api/watchlist                  # Add to watchlist
PATCH  /api/watchlist/{id}             # Update watchlist item
DELETE /api/watchlist/{id}             # Remove from watchlist

GET    /api/portfolio                  # Get portfolio holdings
POST   /api/portfolio                  # Add holding
PUT    /api/portfolio/{id}             # Update holding
DELETE /api/portfolio/{id}             # Remove holding

GET    /api/portfolio/summary          # Portfolio summary with P&L
GET    /api/transactions               # Transaction history
POST   /api/transactions               # Record transaction
```

### Paper Trading

```
GET  /api/paper-trading/account            # Account status
POST /api/paper-trading/account/init       # Initialize account
POST /api/paper-trading/account/fund       # Fund account (Rs. 50L)
POST /api/paper-trading/account/reset      # Reset account
POST /api/paper-trading/trade              # Execute trade
GET  /api/paper-trading/portfolio          # Virtual holdings
POST /api/paper-trading/portfolio          # Add virtual holding
PUT  /api/paper-trading/portfolio/{id}     # Update virtual holding
DELETE /api/paper-trading/portfolio/{id}   # Remove virtual holding
GET  /api/paper-trading/portfolio/summary  # Virtual P&L summary
GET  /api/paper-trading/transactions       # Virtual trade history
POST /api/paper-trading/transactions       # Record virtual transaction
```

### AI Agent

```
POST /api/analyze     # Analyze specific stock
POST /api/ask         # Natural language Q&A
```

### Data Management

```
GET  /api/data/summary              # Storage statistics
POST /api/data/migrate              # JSON → PostgreSQL migration
GET  /api/system-status             # System health
GET  /api/data-freshness            # Data age check
GET  /api/data-quality              # Data quality metrics
```

### Search & System

```
GET /api/search-stocks        # Search stocks by symbol/name
GET /health                   # Health check endpoint
GET /                         # API root with endpoint overview
```

## 🗄️ Database Access

### PostgreSQL Connection

```bash
# Docker container access
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db

# Direct connection (if psql installed locally)
psql postgresql://nepse_user:nepse_password@localhost:5432/nepse_db
```

### Database Schema & Tables

The database contains **8 tables** across **2 schemas**:

#### 📈 Market Data Schema (`nepse_data`)

- `historical_price_volume` - Historical OHLCV data (55,442+ records)

#### 💼 Portfolio Schema (`public`)

- `watchlist` - Stock watchlist
- `portfolio` - Portfolio holdings
- `transactions` - Transaction history
- `paper_accounts` - Paper trading accounts
- `paper_portfolio` - Virtual holdings
- `paper_transactions` - Paper trading history
- `paper_account_funding` - Account funding records

### Common Database Queries

```bash
# List all tables
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db -c "SELECT schemaname, tablename FROM pg_tables WHERE schemaname IN ('public', 'nepse_data') ORDER BY schemaname, tablename;"

# View table structure
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db -c "\d nepse_data.historical_price_volume"

# Count records in historical data
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db -c "SELECT COUNT(*) FROM nepse_data.historical_price_volume;"

# Sample historical data
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db -c "SELECT symbol, business_date, close_price FROM nepse_data.historical_price_volume LIMIT 5;"

# Recent market data
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db -c "SELECT symbol, business_date, close_price FROM nepse_data.historical_price_volume WHERE business_date >= CURRENT_DATE - INTERVAL '7 days' ORDER BY business_date DESC LIMIT 10;"
```

### CSV Export

```bash
# Export all historical data to CSV (sorted by date descending)
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.historical_price_volume ORDER BY business_date DESC, symbol) TO STDOUT WITH CSV HEADER;" > historical_data_export.csv

# Export specific stock data (e.g., NABIL)
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.historical_price_volume WHERE symbol = 'NABIL' ORDER BY business_date DESC) TO STDOUT WITH CSV HEADER;" > nabil_historical.csv

# Export recent data (last 30 days)
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.historical_price_volume WHERE business_date >= CURRENT_DATE - INTERVAL '30 days' ORDER BY business_date DESC) TO STDOUT WITH CSV HEADER;" > recent_data_30_days.csv

# Export portfolio data
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM portfolio) TO STDOUT WITH CSV HEADER;" > portfolio_export.csv

# Export paper trading transactions
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_transactions ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > paper_trading_history.csv

# Bulk export all tables to CSV files
mkdir -p csv_exports
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM nepse_data.historical_price_volume ORDER BY business_date DESC, symbol) TO STDOUT WITH CSV HEADER;" > csv_exports/historical_price_volume.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM watchlist ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/watchlist.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM portfolio ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/portfolio.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM transactions ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/transactions.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_accounts ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_accounts.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_portfolio ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_portfolio.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_transactions ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_transactions.csv
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT * FROM paper_account_funding ORDER BY created_at DESC) TO STDOUT WITH CSV HEADER;" > csv_exports/paper_account_funding.csv

# Export table inventory (names only)
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT schemaname || '.' || tablename as full_table_name, schemaname, tablename FROM pg_tables WHERE schemaname IN ('public', 'nepse_data') ORDER BY schemaname, tablename) TO STDOUT WITH CSV HEADER;" > csv_exports/table_names_only.csv

# Export detailed table inventory (with metadata)
docker exec nepse-postgres psql -U nepse_user -d nepse_db -c "COPY (SELECT schemaname, tablename, tableowner, hasindexes, hasrules, hastriggers, rowsecurity FROM pg_tables WHERE schemaname IN ('public', 'nepse_data') ORDER BY schemaname, tablename) TO STDOUT WITH CSV HEADER;" > csv_exports/all_tables_inventory.csv
```

## 🏗️ Project Structure

```
nepse-smart/
├── 📁 backend/                  # FastAPI backend
│   ├── main.py                 # FastAPI application & market data endpoints
│   ├── models.py               # SQLAlchemy models
│   ├── schemas.py              # Pydantic schemas
│   ├── database.py             # Database configuration
│   ├── portfolio_routes.py     # Portfolio & watchlist endpoints
│   ├── papertrading_routes.py  # Paper trading endpoints
│   ├── agent_routes.py         # AI agent endpoints
│   ├── data_manager.py         # Data management utilities
│   ├── nepse_data_service.py   # Market data service
│   └── init_db.py              # Database initialization
├── 📁 data-scraper/            # Data collection system
│   ├── production_main.py      # Main orchestrator
│   ├── nepse_official_data_fetcher.py  # Official API scraper
│   ├── data_manager.py         # Dual storage manager
│   ├── generate_technicals.py  # Technical indicators generator
│   ├── shared_utils.py         # Common utilities
│   ├── logs/                   # Scraping logs
│   └── requirements.txt        # Scraper dependencies
├── 📁 frontend/                # Vue 3 + TypeScript frontend
│   ├── src/
│   │   ├── components/         # Reusable Vue components
│   │   ├── views/              # Page components
│   │   ├── services/           # API service layer
│   │   └── stores/             # Pinia state management
│   ├── package.json
│   └── vite.config.ts
├── 📁 data/                    # Scraped data storage
│   ├── daily/                  # Daily JSON files (last 30 days)
│   ├── lookup/                 # Reference data (companies, sectors)
│   └── technicals/             # Technical indicators data
├── 📁 csv_exports/             # CSV export files
│   ├── all_tables_inventory.csv
│   ├── banking_indicators.csv
│   ├── exchange_rates.csv
│   ├── floorsheet.csv
│   ├── historical_price_volume.csv
│   ├── market_indices.csv
│   ├── paper_account_funding.csv
│   ├── paper_accounts.csv
│   ├── paper_portfolio.csv
│   ├── paper_transactions.csv
│   ├── portfolio.csv
│   ├── short_term_rates.csv
│   ├── table_names_only.csv
│   ├── transactions.csv
│   └── watchlist.csv
├── 📁 scripts/                 # Utility scripts
├── 📁 .github/workflows/       # GitHub Actions
│   ├── data-collection.yml     # Daily scraping
│   ├── parallel-scraping.yml   # Parallel execution
│   └── reusable-scraper.yml    # Reusable workflow
├── 📁 api/                     # Legacy NEPSE API package
├── 📁 nepse-smart/             # Python virtual environment
├── docker-compose.yml          # Development environment
├── docker-compose.prod.yml     # Production environment
├── Dockerfile                  # Backend container
├── Dockerfile.backend          # Alternative backend container
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🛠️ Technology Stack

| Component              | Technology                            | Purpose                           |
| ---------------------- | ------------------------------------- | --------------------------------- |
| **Frontend**           | Vue 3, TypeScript, Vite, Tailwind CSS | Modern reactive UI                |
| **Backend**            | FastAPI, Python 3.11, Uvicorn         | High-performance API              |
| **Database**           | PostgreSQL 15                         | Persistent data storage           |
| **Package Management** | uv                                    | Fast Python dependency management |
| **Data Collection**    | Python, BeautifulSoup, Requests       | Web scraping                      |
| **Containerization**   | Docker, Docker Compose                | Deployment & development          |
| **CI/CD**              | GitHub Actions                        | Automated workflows               |
| **API Documentation**  | Swagger/OpenAPI                       | Interactive API docs              |

## 📈 Usage Examples

### Basic Data Access

```python
import requests

# Get market summary
response = requests.get("http://localhost:8000/api/summary")
data = response.json()

# Get specific stock data
response = requests.get("http://localhost:8000/api/company-history/NABIL?days=30")
nabil_data = response.json()
```

### Portfolio Management

```python
# Add stock to watchlist
requests.post("http://localhost:8000/api/watchlist", json={
    "symbol": "NABIL",
    "favorite": True,
    "notes": "Banking sector leader"
})

# Add to portfolio
requests.post("http://localhost:8000/api/portfolio", json={
    "symbol": "NABIL",
    "quantity": 100,
    "avg_price": 1200.50,
    "buy_date": "2025-10-30"
})
```

### Paper Trading

```bash
# Fund account
curl -X POST http://localhost:8000/api/paper-trading/account/fund

# Execute trade
curl -X POST http://localhost:8000/api/paper-trading/trade \
  -H "Content-Type: application/json" \
  -d '{"symbol":"NABIL","side":"buy","quantity":10}'
```

## 🔧 Development

### Prerequisites

- **Python 3.11** (3.11.0 or higher)
- **Node.js 18+**
- **Docker & Docker Compose**
- **Git**
- **uv** (optional, for faster Python package management)

### Local Development Setup

```bash
# 1. Clone repository
git clone <repository-url>
cd nepse-smart

# 2. Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r ../requirements.txt
python main.py

# 3. Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# 4. Data collection (new terminal)
cd data-scraper
pip install -r requirements.txt
python production_main.py --scraper official_api
```

### Testing

```bash
# Run data scraper tests
cd data-scraper
python -m pytest

# Test API endpoints
curl http://localhost:8000/health

# Test database connection
docker exec nepse-postgres pg_isready -U nepse_user -d nepse_db
```

## � Deployment

### Production Docker Deployment

```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up --build -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Scale services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3
```

### Environment Variables

```bash
# .env file
DATABASE_URL=postgresql://user:password@host:5432/db
VITE_API_BASE_URL=https://api.yourdomain.com
SECRET_KEY=your-secret-key-here
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** changes: `git commit -m 'Add amazing feature'`
4. **Push** to branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Write tests for new features
- Update documentation
- Ensure Docker compatibility

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NEPSE** for providing market data
- **ShareSansar** for stock price data
- **NRB** for economic indicators
- **FastAPI** and **Vue.js** communities

---

**Built with ❤️ for the Nepali investment community**
