# NEPSE Smart - Nepal Stock Exchange Trading Platform

A comprehensive stock market analysis and trading platform specifically designed for the Nepal Stock Exchange (NEPSE). Built with modern Vue 3 + FastAPI architecture, it provides retail and institutional investors with advanced tools to make informed trading decisions.

## 🎯 **Current Status: Foundation Ready!**

✅ **Backend**: FastAPI server with NEPSE data integration  
✅ **Frontend**: Vue 3 + Tailwind CSS dashboard  
✅ **API**: Real NEPSE data endpoints working  
✅ **Styling**: NEPSE-themed colors and responsive design  
✅ **Docker**: Complete containerization setup  
✅ **Dependencies**: All updated to latest stable versions  
✅ **Architecture**: Scalable foundation for advanced features

## 🚀 Core Features

### 📈 **Trading Signals & Alerts**

- **Daily, Weekly & Monthly Signals** - Automated buy/sell recommendations
- **Price Action Signals** - Technical pattern recognition and alerts
- **Divergence Analysis** - RSI and MACD divergence detection for trend reversals
- **Mean Reversal Signals** - Counter-trend trading opportunities
- **Candlestick Pattern Recognition** - Japanese candlestick analysis and alerts

### 📊 **Live Market Data** _(Currently Available)_

- **Real-time Stock Prices** - Live price feeds for all NEPSE stocks
- **Market Status Tracking** - Live market open/close monitoring
- **Top Gainers/Losers** - Real-time market movers identification
- **Sector Performance** - Live sector-wise performance tracking
- **Volume Analysis** - Real-time trading volume monitoring

### 🏦 **Broker Analytics**

- **Institutional Flow Tracking** - Monitor smart money movements
- **Bulk Transaction Alerts** - Large transaction notifications
- **Broker Holdings Analysis** - Track institutional positions
- **Circuit Breaker Monitoring** - High volatility stock identification
- **Player Analytics** - Follow major market players

### 🔍 **Fundamental Analysis**

- **Stock Screening** - Filter stocks based on financial metrics
- **Valuation Analysis** - P/E ratios and fair value calculations
- **Dividend Tracking** - Historical dividend yields and patterns
- **Growth Stock Identification** - High-growth company analysis
- **Market Cap Analysis** - Company size categorization

### 📉 **Technical Analysis**

- **Professional Charting** - Advanced TradingView integration
- **Support & Resistance** - Key price level identification
- **Trend Analysis** - Market direction and momentum tracking
- **Technical Indicators** - Moving averages, RSI, MACD, Stochastic
- **Multiple Chart Layouts** - 2, 3, 4, 5, 6 chart configurations

### 🛠️ **Advanced Tools**

- **Custom Signal Builder** - Create personalized trading strategies
- **Backtesting Engine** - Test strategies on historical data
- **Portfolio Management** - Track personal stock holdings
- **52-Week High/Low Tracking** - Price range analysis
- **Consolidation Pattern Detection** - Range-bound stock identification

### 💼 **User Experience**

- **Subscription Packages** - Tiered access to premium features
- **Real-time Notifications** - Custom alerts and signal notifications
- **Favorites & Watchlists** - Personalized stock monitoring
- **Dark/Light Themes** - Customizable user interface
- **Mobile Responsive** - Full functionality across all devices

## 📁 Project Structure

```
nepse-smart/
├── frontend/              # Vue 3 + Tailwind CSS frontend
│   ├── src/
│   │   ├── components/    # Vue components
│   │   ├── views/         # Page views
│   │   └── services/      # API services
│   ├── package.json
│   └── Dockerfile
├── backend/               # FastAPI backend
│   ├── main.py           # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── API/                   # NepseUnofficialApi library
│   ├── nepse/            # Core library package
│   │   ├── NepseLib.py   # Main library
│   │   ├── TokenUtils.py # Authentication utilities
│   │   └── data/         # API endpoints and data
│   ├── pyproject.toml
│   └── README.md
├── docker-compose.yml     # Development environment (hot reload)
├── docker-compose.prod.yml # Production environment (optimized)
└── README.md
```

## 🛠️ Technology Stack

### Frontend

- **Vue 3** with Composition API
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Vite** for fast development
- **Axios** for API communication

### Backend

- **FastAPI** for high-performance API
- **Python 3.11+** runtime
- **NepseUnofficialApi** for NEPSE data access
- **Uvicorn** ASGI server

### Infrastructure

- **Docker** for containerization
- **Docker Compose** for orchestration
- **Nginx** for production serving
- **Redis** for production caching

## 🏃‍♂️ Quick Start (2 minutes)

### Prerequisites

- Docker and Docker Compose (recommended)
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Option 1: Docker Setup (Recommended)

```bash
# Clone and setup
git clone <repository-url>
cd nepse-smart

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development Setup

#### 1. Install Dependencies & Start Backend

```bash
# Install the NEPSE package
cd API && pip3 install -e .

# Install backend dependencies
cd ../backend
pip3 install -r requirements.txt

# Start the API server
python3 main.py
```

**Backend runs on:** http://localhost:8000

#### 2. Start Frontend

```bash
# In a new terminal
cd frontend
npm install
npm run dev
```

**Frontend runs on:** http://localhost:3000

### Production Deployment

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🎯 Target Users

- **Retail Traders** - Individual investors seeking trading signals and market insights
- **Professional Traders** - Advanced analytics and institutional-grade tools
- **Portfolio Managers** - Comprehensive market analysis and client management
- **Financial Advisors** - Data-driven investment recommendations
- **Market Researchers** - In-depth market analysis and trend identification

## 📊 What You'll See _(Current Dashboard)_

- **Market Summary**: Real-time NEPSE market statistics
- **Top Gainers**: Best performing stocks today
- **Top Losers**: Worst performing stocks today
- **Responsive Design**: Works on mobile and desktop
- **NEPSE Colors**: Blue/green/red theme matching NEPSE branding

## 💡 Key Benefits

- **Real-time Decision Making** - Live data and instant alerts
- **Risk Management** - Stop-loss calculations and risk analysis
- **Performance Tracking** - Profit/loss analysis and signal accuracy
- **Market Sentiment Analysis** - Volume and price action insights
- **Comprehensive Coverage** - All NEPSE stocks and sectors in one platform

## 📊 NEPSE Data Integration

This project uses the **NepseUnofficialApi** library to access NEPSE data:

### Key Features

- Deciphers NEPSE authentication keys automatically
- Access to real-time market data
- Company listings and stock information
- Historical data and market summaries
- SSL certificate handling for NEPSE API

### API Usage Example

```python
from nepse import Nepse

nepse = Nepse()
nepse.setTLSVerification(False)  # Handles NEPSE SSL issues

# Get market summary
summary = nepse.getSummary()

# Get company list
companies = nepse.getCompanyList()

# Get live market data
live_data = nepse.getLiveMarket()
```

### CLI Tool

The library includes a powerful CLI tool:

```bash
# Download entire floorsheet to JSON
nepse-cli --get-floorsheet --output-file floor.json

# Download to CSV format
nepse-cli --get-floorsheet --to-csv --output-file floor.csv

# Start local API server
nepse-cli --start-server
```

## 🐳 Docker Configuration

### Development Environment (`docker-compose.yml`)

- **Frontend**: Vue dev server with hot-reload on port 3000
- **Backend**: FastAPI with auto-reload on file changes
- **Volumes**: Source code mounted for live editing
- **Fast startup**: No build steps, direct development

### Production Environment (`docker-compose.prod.yml`)

- **Multi-stage builds** for optimized images
- **Nginx** serving static frontend files
- **Redis** for caching and performance
- **Health checks** and resource limits
- **Optimized**: Smaller images, better performance

## 🔧 Configuration

### Environment Variables

Create `.env` files in respective directories:

**Backend (.env)**

```env
NEPSE_API_BASE_URL=https://www.nepalstock.com.np
REDIS_URL=redis://redis:6379
DEBUG=False
```

**Frontend (.env)**

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 📈 API Endpoints

### Backend FastAPI Endpoints

- `GET /` - Health check
- `GET /api/summary` - Market summary data
- `GET /api/top-gainers` - Top gaining stocks
- `GET /api/top-losers` - Top losing stocks
- `GET /api/nepse-index` - NEPSE index data
- `GET /api/company-list` - All listed companies
- `GET /api/market-status` - Market open/closed status
- `GET /docs` - Interactive API documentation

## � Troubleshooting

**Backend not starting?**

- Make sure you installed the nepse package: `cd API && pip3 install -e .`
- Check if port 8000 is available
- Verify Python 3.11+ is installed

**Frontend not loading data?**

- Check if backend is running on http://localhost:8000
- Check browser console for CORS errors
- Verify Node.js 18+ is installed

**No data showing?**

- This is normal if NEPSE market is closed
- Try during market hours (10 AM - 3 PM Nepal time)
- Check backend logs for API connection issues

**Docker issues?**

- Ensure Docker and Docker Compose are installed and running
- Start Docker Desktop if on macOS/Windows
- Try `docker-compose down` then `docker-compose up --build`
- Check for port conflicts (3000, 8000)
- If Docker daemon not running: `open -a Docker` (macOS) or start Docker service

**Frontend can't connect to backend in Docker?**

- This is automatically handled by Docker service networking
- Frontend uses `http://backend:8000` internally (not localhost)
- External access still uses `http://localhost:3000` and `http://localhost:8000`

## 🏗️ Development Status

**Current Foundation (✅ Completed)**

- Vue 3 + TypeScript + FastAPI architecture
- Real-time NEPSE data integration via NepseUnofficialApi
- Docker containerization for development and production
- Modern responsive UI with NEPSE branding
- Clean, scalable codebase architecture
- Updated dependencies (FastAPI 0.117.1, Vue 3.5.21, Tailwind CSS v4)

## 🗺️ Development Roadmap

### 🔥 **Phase 1: Trading Intelligence** _(Next Priority)_

**Trading Signals & Analytics**

- [ ] Daily/Weekly/Monthly automated buy/sell signals
- [ ] Price action pattern recognition and alerts
- [ ] RSI and MACD divergence analysis
- [ ] Mean reversal signal detection
- [ ] Japanese candlestick pattern recognition

**Advanced Charting**

- [ ] TradingView integration for professional charts
- [ ] Support and resistance level identification
- [ ] Technical indicators (RSI, MACD, Bollinger Bands, Stochastic)
- [ ] Multiple chart layout configurations (2-6 charts)
- [ ] Custom timeframe analysis

### 📊 **Phase 2: Market Intelligence**

**Broker & Institutional Analytics**

- [ ] Institutional flow tracking and smart money movements
- [ ] Bulk transaction alerts and notifications
- [ ] Broker holdings analysis and position tracking
- [ ] Circuit breaker monitoring for high volatility stocks
- [ ] Major market player analytics

**Fundamental Analysis Tools**

- [ ] Advanced stock screening based on financial metrics
- [ ] P/E ratio analysis and fair value calculations
- [ ] Historical dividend tracking and yield patterns
- [ ] Growth stock identification algorithms
- [ ] Market cap categorization and analysis

### �️ **Phase 3: Advanced Platform Features**

**Custom Trading Tools**

- [ ] Custom signal builder for personalized strategies
- [ ] Backtesting engine for strategy validation
- [ ] Portfolio management and tracking system
- [ ] 52-week high/low monitoring
- [ ] Consolidation pattern detection

**Real-time Features**

- [ ] Live WebSocket integration for instant updates
- [ ] Real-time price alerts and notifications
- [ ] Volume spike detection and alerts
- [ ] Market heatmap visualization

### 💰 **Phase 4: Monetization & Scale**

**Subscription Tiers**

- **Basic (Free)**: Market data, basic signals, limited features
- **Premium ($29/month)**: Advanced signals, real-time alerts, charting tools
- **Professional ($99/month)**: Full analytics, custom strategies, API access
- **Enterprise (Custom)**: White-label solutions, institutional features

**Revenue Streams**

- [ ] Subscription-based access to premium features
- [ ] API marketplace for third-party integrations
- [ ] Educational content and trading courses
- [ ] Partnership with brokerages and financial institutions

### 🌐 **Phase 5: Expansion & Innovation**

**Nepal-Specific Integrations**

- [ ] Payment gateway integration (eSewa, Khalti, IME Pay)
- [ ] Nepal financial news sentiment analysis
- [ ] Economic calendar for Nepal market events
- [ ] Sector-specific analysis (Banking, Hydro, Insurance)
- [ ] Multi-language support (Nepali/English)

**AI & Machine Learning**

- [ ] NEPSE stock price prediction models
- [ ] Automated trading suggestion algorithms
- [ ] Risk assessment and portfolio optimization
- [ ] News sentiment analysis for market prediction

**Mobile & Community**

- [ ] Native iOS and Android applications
- [ ] Social trading and community features
- [ ] User discussion forums and expert analysis
- [ ] Push notifications and offline capabilities

---

## 🎯 **Vision Statement**

NEPSE Smart aims to become the **premier trading platform for Nepal Stock Exchange**, providing institutional-grade tools accessible to retail investors. Our goal is to democratize advanced market analytics and empower informed investment decisions through technology.

**From Simple Dashboard → Comprehensive Trading Intelligence Platform**

_For detailed technical roadmap, see `claude.md`. For contribution guidelines, create feature branches and submit pull requests with priority labels (🔥 High/⭐ Medium/💡 Low)._

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **NepseUnofficialApi** - For providing robust NEPSE data access
- **NEPSE** - Nepal Stock Exchange for the data source
- **FastAPI** and **Vue.js** communities for excellent frameworks

## 📞 Support

For support and questions:

- Create an issue in this repository
- Check the API documentation at `/docs` when running the backend
- Review the `claude.md` file for detailed project roadmap

---

**Note**: This project is not affiliated with Nepal Stock Exchange (NEPSE). It uses publicly available data through unofficial APIs for educational and analytical purposes.
