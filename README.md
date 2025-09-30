# NEPSE Smart - Nepal Stock Exchange Trading Platform

A comprehensive stock market analysis and trading platform for the Nepal Stock Exchange (NEPSE), built with a modern Vue 3 and FastAPI architecture.

## 🚀 Quick Start

Get up and running in 2 minutes with Docker.

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Docker Setup (Recommended)

```bash
# 1. Clone the repository
git clone <repository-url>
cd nepse-smart

# 2. Start all services
docker-compose up --build

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
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

| Area          | Technology                                                              |
|---------------|-------------------------------------------------------------------------|
| **Frontend**  | Vue 3, TypeScript, Vite, Tailwind CSS, Axios                            |
| **Backend**   | FastAPI, Python 3.11+, Uvicorn, NepseUnofficialApi                      |
| **Infrastructure** | Docker, Docker Compose, Nginx, Redis                                  |

## ✨ Core Features

- **Live Market Data:** Real-time stock prices, top gainers/losers, and market status.
- **Trading Signals & Alerts:** Automated buy/sell signals and pattern recognition.
- **Technical & Fundamental Analysis:** Advanced charting, stock screening, and valuation tools.
- **Broker Analytics:** Institutional flow tracking and bulk transaction alerts.
- **Advanced Tools:** Custom signal builder, backtesting engine, and portfolio management.
- **Modern UX:** Responsive design, dark/light themes, and real-time notifications.

## 📁 Project Structure

```
nepse-smart/
├── frontend/              # Vue 3 + Tailwind CSS frontend
├── backend/               # FastAPI backend
├── api/                   # NepseUnofficialApi library
├── docker-compose.yml     # Development environment
├── docker-compose.prod.yml # Production environment
└── README.md
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