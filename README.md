# NEPSE Smart - Nepal Stock Exchange Analytics Platform

A modern, containerized analytics platform for Nepal Stock Exchange (NEPSE) data built with Vue 3 + FastAPI, leveraging the powerful NepseUnofficialApi library.

## 🎯 **Status: Simple Dashboard Ready!**

✅ **Backend**: FastAPI server with NEPSE data integration  
✅ **Frontend**: Vue 3 + Tailwind CSS dashboard  
✅ **API**: Real NEPSE data endpoints working  
✅ **Styling**: NEPSE-themed colors and responsive design  
✅ **Docker**: Complete containerization setup  
✅ **Dependencies**: All updated to latest stable versions

## 🚀 Features

- **Real-time NEPSE Data**: Live market data, stock prices, and market summary
- **Modern UI**: Vue 3 + TypeScript + Tailwind CSS responsive interface
- **Fast API**: Python FastAPI backend with robust data processing
- **Containerized**: Complete Docker setup for development and production
- **NEPSE Integration**: Built on the proven NepseUnofficialApi library
- **Clean Architecture**: Streamlined codebase following best practices
- **Live Dashboard**: Market summary, top gainers/losers, responsive design

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

## 📊 What You'll See

- **Market Summary**: Real-time NEPSE market statistics
- **Top Gainers**: Best performing stocks today
- **Top Losers**: Worst performing stocks today
- **Responsive Design**: Works on mobile and desktop
- **NEPSE Colors**: Blue/green/red theme matching NEPSE branding

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

## �🚦 Development Status

This project follows an iterative development approach:

✅ **Completed**

- Basic Vue 3 + FastAPI setup
- NEPSE API integration
- Docker containerization
- Clean project structure
- Real-time data display
- Updated dependencies (Flask 3.1.2, FastAPI 0.117.1, pywasm 2.2.1)

## � Future Roadmap & Ideas

### 🔥 High Priority Features

**API Platform & Monetization**

- [ ] Public APIs for NEPSE market data integration
- [ ] API marketplace with usage-based pricing
- [ ] Third-party integration for capital firms and investment companies

**Trading Competition Platform**

- [ ] Virtual trading system using real NEPSE data
- [ ] Time-bound competitions with cash prizes
- [ ] Leaderboards and performance tracking

**Advanced Analytics Dashboard**

- [ ] Custom dashboard builder for Nepal stock analysis
- [ ] Institutional-grade analysis tools
- [ ] Advanced charting with TradingView integration

### 📊 Data Visualization & Analytics

**Real-time Market Features**

- [ ] Live WebSocket integration for stock updates
- [ ] Interactive candlestick charts for individual NEPSE stocks
- [ ] Market heatmap visualization
- [ ] Technical indicators (RSI, MACD, Bollinger Bands)
- [ ] Volume analysis and spike alerts

**Portfolio Management**

- [ ] Personal NEPSE portfolio tracker with NPR calculations
- [ ] Profit/loss tracking and asset allocation charts
- [ ] Performance comparison with NEPSE index
- [ ] Investment goal tracking in Nepali rupees

### 🔔 Subscription-Based Notifications

**Basic Plan**

- [ ] Daily NEPSE market summary (email)
- [ ] Weekly portfolio performance reports

**Premium Plan**

- [ ] Custom price alerts for NEPSE stocks
- [ ] Real-time email/SMS notifications
- [ ] Volume spike alerts and market notifications

**Enterprise Plan**

- [ ] AI-powered trading signals for NEPSE
- [ ] Unusual market activity alerts
- [ ] Earnings and dividend notifications for Nepal companies

### 🤖 AI & Machine Learning

- [ ] NEPSE stock price prediction models
- [ ] Sentiment analysis from Nepal financial news
- [ ] Pattern recognition in NEPSE charts
- [ ] Risk assessment algorithms for Nepal market
- [ ] Automated trading suggestions

### 📱 Mobile & Cross-Platform

- [ ] iOS and Android native apps
- [ ] React Native development
- [ ] Push notifications and biometric authentication
- [ ] Offline data sync and home screen widgets

### 🔐 Security & User Management

- [ ] User authentication with social login
- [ ] Role-based access control
- [ ] Two-factor authentication
- [ ] API rate limiting and data encryption

### 🌐 Nepal-Specific Integrations

- [ ] NEPSE official API integration
- [ ] Nepal financial news API integration
- [ ] Payment gateways (eSewa, Khalti, etc.)
- [ ] Economic calendar for Nepal
- [ ] Sector analysis (Banking, Hydro, Insurance)

### 📈 Advanced Features

**Technical Improvements**

- [ ] Progressive Web App (PWA) features
- [ ] Multi-language support (Nepali/English)
- [ ] Dark/light theme toggle
- [ ] Offline data access with caching

**Reporting & Export**

- [ ] CSV/Excel export functionality
- [ ] PDF report generation
- [ ] Automated daily/weekly reports
- [ ] Print-friendly views

**Community Features**

- [ ] User discussion forums for NEPSE
- [ ] Stock rating/review system
- [ ] Social trading features
- [ ] Expert analysis sharing platform

### 💰 Subscription Model

**Basic (Free)**

- Basic NEPSE data and daily summaries
- Limited portfolio tracking

**Premium (Monthly/Yearly)**

- Real-time data and alerts
- Advanced charting tools
- Email/SMS notifications and data export

**Enterprise (Custom Pricing)**

- API access and custom analytics
- Priority support and white-label solutions

---

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
