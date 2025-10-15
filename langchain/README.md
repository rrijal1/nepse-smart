# NEPSE Smart Multi-Agent System

An enhanced AI-powered stock analysis system for the Nepal Stock Exchange (NEPSE) using sophisticated multi-agent architecture.

## 🚀 Features

### Multi-Agent Architecture

- **Technical Analysis Agent**: Advanced technical indicator analysis with multiple timeframes
- **Fundamental Analysis Agent**: Comprehensive financial metrics evaluation
- **Macro/News Analysis Agent**: AI-powered sentiment analysis of market news
- **Orchestrator System**: Intelligent coordination and synthesis of agent results

### Enhanced Capabilities

- **Multiple Stock Support**: Analysis for NABIL, ADBL, EBL and easily extensible
- **Sophisticated Scoring**: Multi-dimensional scoring system with detailed breakdowns
- **Real-time Processing**: Fast analysis with processing time tracking
- **Error Handling**: Robust error handling with fallback mechanisms
- **Logging**: Comprehensive logging for debugging and monitoring

## 📁 File Structure

```
langchain/
├── nepse_agent_backend.py    # Enhanced FastAPI backend with multi-agent system
├── index.html               # Complete frontend with Vue.js integration
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This documentation
```

## 🛠️ Installation & Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

### 3. Run the Backend

```bash
# Development mode with auto-reload
uvicorn nepse_agent_backend:app --reload --host 0.0.0.0 --port 8000

# Or simply run the Python file
python nepse_agent_backend.py
```

### 4. Open Frontend

- Open `index.html` in your browser to access the complete multi-agent interface

## 🔧 API Endpoints

### GET `/`

Health check and system information

### GET `/stocks`

List all available stocks for analysis

### POST `/analyze`

Comprehensive stock analysis

```json
{
  "stock_symbol": "NABIL"
}
```

### GET `/analyze/{stock_symbol}`

Quick analysis via GET request

## 📊 Multi-Agent System Workflow

1. **Input Validation**: Verify stock symbol exists in database
2. **Technical Agent**: Analyzes price trends, RSI, MACD, volume, support/resistance
3. **Fundamental Agent**: Evaluates P/E ratio, EPS, debt levels, dividend yield, market cap
4. **Macro/News Agent**: Processes news sentiment using LLM analysis
5. **Orchestration**: Aggregates scores and generates final recommendation
6. **Synthesis**: Creates comprehensive investment analysis using advanced LLM

## 🎯 Improvements Made

### Backend Enhancements

- ✅ **Expanded Mock Data**: Added ADBL and EBL with comprehensive metrics
- ✅ **Enhanced Technical Analysis**: Multi-factor scoring with trend, momentum, and volume analysis
- ✅ **Sophisticated Fundamental Analysis**: Comprehensive financial health evaluation
- ✅ **Improved News Analysis**: Better LLM integration with fallback mechanisms
- ✅ **Robust Error Handling**: Graceful failure handling and detailed logging
- ✅ **Performance Tracking**: Processing time measurement and optimization
- ✅ **Structured Responses**: Detailed JSON responses with agent breakdowns

### Frontend Improvements

- ✅ **Proper File Structure**: Separated HTML and Vue.js components
- ✅ **Enhanced UI**: Better visual design with agent status indicators
- ✅ **Real-time Feedback**: Loading states and progress indicators
- ✅ **Agent Visualization**: Individual agent results display
- ✅ **Score Visualization**: Color-coded overall scoring system
- ✅ **Error Handling**: User-friendly error messages and retry mechanisms

### System Architecture

- ✅ **Modular Design**: Separated concerns with clear agent boundaries
- ✅ **Scalable Structure**: Easy to add new agents or stocks
- ✅ **Configuration Management**: Environment-based configuration
- ✅ **Documentation**: Comprehensive code documentation and examples

## 🔮 Available Stock Analysis

| Symbol | Company                       | Status                                    |
| ------ | ----------------------------- | ----------------------------------------- |
| NABIL  | Nabil Bank                    | Stable fundamentals, good technical setup |
| ADBL   | Agricultural Development Bank | Strong fundamentals, moderate technical   |
| EBL    | Everest Bank                  | Dwindling fundamentals, bearish technical |

## 🚨 Important Notes

- **Demo System**: Uses mock data for demonstration purposes
- **Educational Use**: Not intended for actual investment decisions
- **API Keys**: Requires valid Groq API key for news analysis
- **Rate Limits**: Be mindful of API rate limits in production use

## 🤝 Contributing

To add new stocks or improve the system:

1. **Add Stock Data**: Extend `MOCK_STOCK_DATA` in the backend
2. **Enhance Agents**: Improve scoring algorithms in agent functions
3. **UI Improvements**: Enhance frontend components and visualizations
4. **Integration**: Connect to real market data APIs

## 📄 License

This project is for educational purposes. Please ensure compliance with relevant financial regulations when using in production environments.

---

**Disclaimer**: This is an AI-generated analysis system and not financial advice. Always conduct your own research and consult with qualified financial advisors before making investment decisions.
