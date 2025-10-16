# NEPSE Smart - Complete Data Scraping & Analysis System

A comprehensive system for scraping, storing, and analyzing Nepal Stock Exchange (NEPSE) data with automated daily collection via GitHub Actions.

## 🚀 Features

### Automated Data Collection

- **Daily Scraping**: Runs automatically at midnight via GitHub Actions
- **Comprehensive Data**: Share prices, floorsheet, market indices
- **Historical Database**: Builds growing database over time
- **Error Handling**: Robust error handling and retry mechanisms

### Data Processing & Analysis

- **Multiple Formats**: JSON and CSV output
- **Real-time API**: FastAPI server for data access
- **Interactive Dashboard**: Streamlit-based visualization
- **Data Validation**: Automated quality checks

### Integration Ready

- **Vue.js Frontend**: Ready for integration with existing frontend
- **REST API**: Standard endpoints for all data types
- **Flexible Export**: Easy data export and processing

## �️ Quick Start

### 1. Setup Data Scraping

```bash
# Install Python dependencies
cd data-scraper
pip install -r requirements.txt

# Test the scraper
python test_scraper.py

# Run manual scrape
python scraper.py
```

### 2. Start the Data API Server

```bash
cd data-scraper
python api.py
```

API will be available at: `http://localhost:8001`

### 3. Launch Interactive Dashboard

```bash
cd data-scraper
streamlit run dashboard.py
```

Dashboard will open in your browser at: `http://localhost:8501`

### Prerequisites

- Python 3.8+
- Docker and Docker Compose (optional)
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Docker Setup (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd nepse-smart

# 2. Install Python dependencies
pip3 install -r requirements.txt

# 3. Start all services (PostgreSQL, backend, frontend)
docker-compose up --build

# 4. Initialize database (first time only)
# In another terminal:
cd backend
python3 init_db.py

# 5. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
# PostgreSQL: localhost:5432
```

### Database Access

To view and manage PostgreSQL data:

````bash
# Method 1: Connect using Docker (Recommended)
docker exec -it nepse-postgres psql -U nepse_user -d nepse_db


**PostgreSQL psql Cheat Sheet:**

```sql
-- Navigation Commands
\dt                          -- List all tables
\d watchlist                 -- Describe watchlist table structure
\l                           -- List all databases
\du                          -- List users
\x                           -- Toggle expanded display (better for wide tables)
\q                           -- Quit psql

-- View Data
SELECT * FROM watchlist;                                    -- View all watchlist items
SELECT * FROM portfolio;                                    -- View all portfolio holdings
SELECT * FROM transactions ORDER BY transaction_date DESC;  -- View recent transactions

-- Add to Watchlist
INSERT INTO watchlist (symbol, added_date, favorite, notes)
VALUES ('NABIL', CURRENT_DATE, true, 'Banking sector leader');

-- Add to Portfolio
INSERT INTO portfolio (symbol, quantity, avg_price, buy_date, notes)
VALUES ('NABIL', 100, 1200.50, '2025-10-15', 'Long-term hold');

-- Update Watchlist (Toggle favorite)
UPDATE watchlist SET favorite = NOT favorite WHERE symbol = 'NABIL';

-- Update Portfolio (Add more shares)
UPDATE portfolio
SET quantity = quantity + 50,
    avg_price = ((avg_price * quantity) + (1250.00 * 50)) / (quantity + 50)
WHERE symbol = 'NABIL';

-- Delete Operations
DELETE FROM watchlist WHERE symbol = 'NABIL';
DELETE FROM portfolio WHERE id = 1;

-- Analytics Queries
SELECT symbol, quantity, avg_price,
       (quantity * avg_price) as invested_amount
FROM portfolio ORDER BY invested_amount DESC;

SELECT COUNT(*) as total_stocks,
       SUM(quantity * avg_price) as total_invested
FROM portfolio;
````

### Quick Portfolio Setup

For setting up just the portfolio management feature:

```bash
# Automated setup
./setup_portfolio.sh

# Or manual setup - see SETUP_PORTFOLIO.md
```

### Local Development

<details>
<summary>Click to expand for local development instructions</summary>

#### 1. Backend Setup

```bash
# Install the NEPSE package
cd api && pip3 install -e .

# Install backend dependencies
cd ../backend
pip3 install -r requirements.txt

# Start the API server
python3 main.py
# Backend runs on http://localhost:8000
```

#### 2. Frontend Setup

```bash
# In a new terminal
cd frontend
npm install
npm run dev
# Frontend runs on http://localhost:3000
```

</details>

## 🛠️ Technology Stack

| Area               | Technology                                   |
| ------------------ | -------------------------------------------- |
| **Frontend**       | Vue 3, TypeScript, Vite, Tailwind CSS, Axios |
| **Backend**        | FastAPI, Python 3.11+, Uvicorn, SQLAlchemy   |
| **Database**       | PostgreSQL 15, psycopg2                      |
| **Infrastructure** | Docker, Docker Compose, Nginx                |

## ✨ Core Features

- **Live Market Data:** Real-time stock prices, top gainers/losers, and market status.
- **Portfolio & Watchlist Management:** Track your holdings, monitor P&L, and manage watchlists with PostgreSQL persistence.
- **Trading Signals & Alerts:** Automated buy/sell signals and pattern recognition.
- **Technical & Fundamental Analysis:** Advanced charting, stock screening, and valuation tools.
- **Broker Analytics:** Institutional flow tracking and bulk transaction alerts.
- **Advanced Tools:** Custom signal builder, backtesting engine, and portfolio management.
- **Modern UX:** Responsive design, dark/light themes, and real-time notifications.

## 📁 Project Structure

```
nepse-smart/
├── frontend/              # Vue 3 + Tailwind CSS frontend
│   └── src/services/      # API service layer
├── backend/               # FastAPI backend
│   ├── models.py          # SQLAlchemy database models
│   ├── schemas.py         # Pydantic schemas
│   ├── database.py        # Database configuration
│   ├── portfolio_routes.py # Portfolio API endpoints
│   └── init_db.py         # Database initialization
├── data/                  # Scraped market data
├── data-scraper/          # Data collection scripts
├── docker-compose.yml     # Development environment
├── docker-compose.prod.yml # Production environment
├── requirements.txt       # Python dependencies
├── setup_portfolio.sh     # Portfolio feature setup script
├── PORTFOLIO_FEATURE.md   # Portfolio feature documentation
└── SETUP_PORTFOLIO.md     # Setup instructions
```

## ⚡ Scalability and Performance

To ensure a responsive and scalable platform, we are adopting a hybrid, phased approach to data delivery.

- **WebSockets:** For high-frequency, real-time data like market depth and live charts.
- **Server-Sent Events (SSE):** For frequent updates like top gainers/losers and news alerts.
- **Standard API (REST):** For on-demand data like historical prices and company profiles.

This hybrid model ensures that NEPSE Smart is both performant and scalable.

## 🗺️ Development Roadmap

This project has a detailed development roadmap that includes trading intelligence, market intelligence, advanced platform features, monetization, and expansion.

For more details, please see the `claude.md` file.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

## 📝 License

This project is licensed under the MIT License.
