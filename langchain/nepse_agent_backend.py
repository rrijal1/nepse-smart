import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# --- LangChain and Groq Imports ---
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Environment Variable Setup ---
# IMPORTANT: Set your Groq API key in your environment variables before running.
# For example: export GROQ_API_KEY="your_api_key_here"
# If the key is not set, the script will exit with an error.
if "GROQ_API_KEY" not in os.environ:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it to your Groq API key.")

# --- Enhanced Mock Database ---
# In a real app, you would fetch this data from an API or database.
# We mock it here for demonstration with multiple stocks.
MOCK_STOCK_DATA = {
    "NABIL": {
        "fundamentals": {
            "pe_ratio": 18.5,
            "eps": 45.2,
            "debt_to_equity": 0.8,
            "status": "stable",
            "market_cap": 42.5,  # in billions
            "book_value": 520.0,
            "dividend_yield": 8.2
        },
        "technicals": {
            "price": 950.0,
            "ema_21": 935.0,
            "ema_50": 920.0,
            "rsi_14": 65.0,
            "macd_signal": "bullish_crossover",
            "volume": 1250000,
            "52_week_high": 1100.0,
            "52_week_low": 800.0
        },
        "news": [
            "Nepal Rastra Bank holds interest rates steady, citing stable inflation.",
            "Government announces new incentives for the banking sector.",
            "Global economic outlook remains uncertain, affecting investor sentiment.",
            "NABIL Bank reports strong quarterly earnings with 15% growth.",
            "Digital banking adoption accelerates across Nepal's financial sector."
        ]
    },
    "ADBL": {
        "fundamentals": {
            "pe_ratio": 22.1,
            "eps": 38.7,
            "debt_to_equity": 0.9,
            "status": "strong",
            "market_cap": 28.3,
            "book_value": 445.0,
            "dividend_yield": 7.8
        },
        "technicals": {
            "price": 720.0,
            "ema_21": 710.0,
            "ema_50": 695.0,
            "rsi_14": 58.0,
            "macd_signal": "neutral",
            "volume": 980000,
            "52_week_high": 850.0,
            "52_week_low": 620.0
        },
        "news": [
            "Agricultural Development Bank launches new rural finance programs.",
            "Government increases budget allocation for agricultural sector.",
            "Strong monsoon expected to boost agricultural productivity.",
            "ADBL expands digital payment services to rural areas.",
            "Bank's loan portfolio shows healthy growth in agricultural lending."
        ]
    },
    "EBL": {
        "fundamentals": {
            "pe_ratio": 25.8,
            "eps": 42.3,
            "debt_to_equity": 1.1,
            "status": "dwindling",
            "market_cap": 35.7,
            "book_value": 380.0,
            "dividend_yield": 6.5
        },
        "technicals": {
            "price": 680.0,
            "ema_21": 695.0,
            "ema_50": 710.0,
            "rsi_14": 35.0,
            "macd_signal": "bearish_crossover",
            "volume": 1100000,
            "52_week_high": 920.0,
            "52_week_low": 650.0
        },
        "news": [
            "Banking sector faces regulatory pressure over loan quality.",
            "Economic slowdown impacts private banking profitability.",
            "EBL faces challenges in maintaining profit margins.",
            "Competition intensifies in commercial banking sector.",
            "Regulatory authorities tighten oversight on bank operations."
        ]
    }
}

# --- Agent Tools (Specialized Agents) ---

@tool
def technical_analysis_agent(stock_symbol: str) -> str:
    """
    Enhanced technical analysis agent that analyzes multiple technical indicators
    and provides a comprehensive score with detailed reasoning.
    """
    logger.info(f"Running Technical Analysis for {stock_symbol}")
    data = MOCK_STOCK_DATA.get(stock_symbol, {}).get("technicals")
    if not data:
        return "Technical data not found. Score: 0."

    buy_signals = 0
    sell_signals = 0
    signals_detail = []
    
    # Rule 1: Price vs. EMAs (Trend Analysis)
    if data["price"] > data["ema_21"] > data["ema_50"]:
        buy_signals += 2
        signals_detail.append("Strong uptrend: Price above both EMAs")
    elif data["price"] > data["ema_21"]:
        buy_signals += 1
        signals_detail.append("Mild uptrend: Price above 21-day EMA")
    elif data["price"] < data["ema_21"] < data["ema_50"]:
        sell_signals += 2
        signals_detail.append("Strong downtrend: Price below both EMAs")
    else:
        sell_signals += 1
        signals_detail.append("Weak trend: Price below 21-day EMA")
    
    # Rule 2: RSI (Momentum Analysis)
    rsi = data["rsi_14"]
    if rsi > 80:
        sell_signals += 2
        signals_detail.append(f"Severely overbought: RSI {rsi}")
    elif rsi > 70:
        sell_signals += 1
        signals_detail.append(f"Overbought: RSI {rsi}")
    elif rsi < 20:
        buy_signals += 2
        signals_detail.append(f"Severely oversold: RSI {rsi}")
    elif rsi < 30:
        buy_signals += 1
        signals_detail.append(f"Oversold: RSI {rsi}")
    else:
        signals_detail.append(f"Neutral momentum: RSI {rsi}")
        
    # Rule 3: MACD Signal
    macd = data["macd_signal"]
    if "bullish_crossover" in macd:
        buy_signals += 2
        signals_detail.append("Bullish MACD crossover detected")
    elif "bearish_crossover" in macd:
        sell_signals += 2
        signals_detail.append("Bearish MACD crossover detected")
    elif "bullish" in macd:
        buy_signals += 1
        signals_detail.append("MACD in bullish territory")
    elif "bearish" in macd:
        sell_signals += 1
        signals_detail.append("MACD in bearish territory")
    
    # Rule 4: Price Position (Support/Resistance)
    price_range = data["52_week_high"] - data["52_week_low"]
    current_position = (data["price"] - data["52_week_low"]) / price_range
    
    if current_position > 0.8:
        sell_signals += 1
        signals_detail.append("Near 52-week high - potential resistance")
    elif current_position < 0.2:
        buy_signals += 1
        signals_detail.append("Near 52-week low - potential support")
    
    # Rule 5: Volume Analysis (if significantly high)
    avg_volume = 1000000  # Assumed average
    if data["volume"] > avg_volume * 1.5:
        # High volume amplifies signals
        if buy_signals > sell_signals:
            buy_signals += 1
            signals_detail.append("High volume supports bullish sentiment")
        else:
            sell_signals += 1
            signals_detail.append("High volume supports bearish sentiment")

    # Final scoring
    score = buy_signals - sell_signals
    
    # Create detailed summary
    summary = f"Technical Analysis for {stock_symbol}: "
    summary += f"Buy signals: {buy_signals}, Sell signals: {sell_signals}. "
    summary += f"Overall technical score: {score}. "
    summary += f"Key findings: {'; '.join(signals_detail[:3])}."  # Top 3 signals
    
    return summary

@tool
def fundamental_analysis_agent(stock_symbol: str) -> str:
    """
    Enhanced fundamental analysis agent that evaluates multiple financial metrics
    and provides comprehensive scoring with detailed explanations.
    """
    logger.info(f"Running Fundamental Analysis for {stock_symbol}")
    data = MOCK_STOCK_DATA.get(stock_symbol, {}).get("fundamentals")
    if not data:
        return "Fundamental data not found. Score: 0."

    score = 0
    positive_factors = []
    negative_factors = []
    
    # Rule 1: Company Status (Most Important)
    status = data["status"]
    if status == "dwindling":
        score -= 3
        negative_factors.append("Company fundamentals are deteriorating")
        return f"CRITICAL: Fundamental status is 'dwindling'. Major red flag. Score: {score}."
    elif status == "strong":
        score += 2
        positive_factors.append("Strong fundamental position")
    elif status == "stable":
        score += 1
        positive_factors.append("Stable fundamental metrics")
        
    # Rule 2: Valuation Metrics
    pe_ratio = data["pe_ratio"]
    if pe_ratio < 15:
        score += 2
        positive_factors.append(f"Attractive valuation (P/E: {pe_ratio})")
    elif pe_ratio < 20:
        score += 1
        positive_factors.append(f"Reasonable valuation (P/E: {pe_ratio})")
    elif pe_ratio > 25:
        score -= 1
        negative_factors.append(f"High P/E ratio ({pe_ratio})")
    elif pe_ratio > 30:
        score -= 2
        negative_factors.append(f"Very high P/E ratio ({pe_ratio})")
    
    # Rule 3: Profitability
    eps = data["eps"]
    if eps > 50:
        score += 2
        positive_factors.append(f"Strong earnings (EPS: {eps})")
    elif eps > 30:
        score += 1
        positive_factors.append(f"Good earnings (EPS: {eps})")
    elif eps < 20:
        score -= 1
        negative_factors.append(f"Low earnings (EPS: {eps})")
    
    # Rule 4: Financial Health
    debt_to_equity = data["debt_to_equity"]
    if debt_to_equity < 0.5:
        score += 1
        positive_factors.append("Low debt levels")
    elif debt_to_equity > 1.0:
        score -= 1
        negative_factors.append("High debt-to-equity ratio")
    
    # Rule 5: Dividend Yield
    dividend_yield = data.get("dividend_yield", 0)
    if dividend_yield > 8:
        score += 1
        positive_factors.append(f"High dividend yield ({dividend_yield}%)")
    elif dividend_yield > 5:
        positive_factors.append(f"Good dividend yield ({dividend_yield}%)")
    
    # Rule 6: Market Cap considerations
    market_cap = data.get("market_cap", 0)
    if market_cap > 50:
        positive_factors.append("Large-cap stability")
    elif market_cap < 10:
        negative_factors.append("Small-cap volatility risk")
    
    # Create comprehensive summary
    summary = f"Fundamental Analysis for {stock_symbol}: "
    summary += f"Status: {status.upper()}. "
    summary += f"Overall fundamental score: {score}. "
    
    if positive_factors:
        summary += f"Strengths: {'; '.join(positive_factors[:2])}. "
    
    if negative_factors:
        summary += f"Concerns: {'; '.join(negative_factors[:2])}. "
    
    # Add key metrics summary
    summary += f"Key metrics - P/E: {pe_ratio}, EPS: {eps}, D/E: {debt_to_equity}."
    
    return summary

@tool
def macro_news_agent(stock_symbol: str) -> str:
    """
    Enhanced macro-economic and news sentiment analysis agent using LLM.
    Analyzes news sentiment and provides contextual market insights.
    """
    logger.info(f"Running Macro/News Analysis for {stock_symbol}")
    news = MOCK_STOCK_DATA.get(stock_symbol, {}).get("news")
    if not news:
        return "No news found. Score: 0."
    
    try:
        # Use the fast model for sentiment analysis
        llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
        
        prompt = PromptTemplate.from_template(
            """Analyze the sentiment of the following news headlines for {stock_symbol} and the broader Nepalese stock market.

Consider:
1. Direct impact on the specific stock
2. Broader market/sector implications  
3. Economic policy effects
4. Investor sentiment indicators

News Headlines:
{news_items}

Provide:
1. Overall sentiment classification (Strongly Positive, Positive, Neutral, Negative, Strongly Negative)
2. Key factors influencing sentiment
3. Brief impact assessment on {stock_symbol}

Format your response as: "Sentiment: [CLASSIFICATION]. Key factors: [FACTORS]. Impact on {stock_symbol}: [IMPACT]"
"""
        )
        
        chain = prompt | llm
        response = chain.invoke({
            "news_items": "\n".join(f"• {item}" for item in news),
            "stock_symbol": stock_symbol
        })
        
        # Enhanced scoring based on response content
        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, list):
                content = ' '.join(str(item) for item in content)
            else:
                content = str(content)
            response_text = content
        else:
            content = str(response)
            response_text = content
        
        content_lower = content.lower()
        
        score = 0
        if "strongly positive" in content_lower:
            score = 2
        elif "positive" in content_lower:
            score = 1
        elif "strongly negative" in content_lower:
            score = -2
        elif "negative" in content_lower:
            score = -1
        
        return f"Macro/News Analysis for {stock_symbol}: {response_text.strip()}. Overall macro score: {score}."

    except Exception as e:
        logger.error(f"Error in Macro News Agent: {e}")
        # Fallback rule-based analysis
        positive_keywords = ["growth", "incentive", "strong", "expansion", "profit", "increase"]
        negative_keywords = ["decline", "loss", "pressure", "challenge", "slowdown", "uncertainty"]
        
        positive_count = sum(1 for item in news for keyword in positive_keywords if keyword in item.lower())
        negative_count = sum(1 for item in news for keyword in negative_keywords if keyword in item.lower())
        
        score = positive_count - negative_count
        sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
        
        return f"Macro/News Analysis (fallback): {sentiment} sentiment detected. Score: {score}. Key themes from {len(news)} news items analyzed."

# --- Enhanced Multi-Agent Orchestrator ---

class AgentResults:
    """Data class to store agent execution results"""
    def __init__(self):
        self.technical_score = 0
        self.technical_summary = ""
        self.fundamental_score = 0
        self.fundamental_summary = ""
        self.macro_score = 0
        self.macro_summary = ""
        self.overall_score = 0

def parse_agent_output(output: str) -> tuple[int, str]:
    """Extract score and summary from agent output"""
    import re
    
    # Try to extract score from various formats
    score_patterns = [
        r"score:?\s*([+-]?\d+)",
        r"overall.*?score:?\s*([+-]?\d+)",
        r"Score:?\s*([+-]?\d+)"
    ]
    
    score = 0
    for pattern in score_patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            score = int(match.group(1))
            break
    
    return score, output

def run_multi_agent_analysis(stock_symbol: str) -> AgentResults:
    """
    Coordinate the execution of all three specialized agents
    and aggregate their results.
    """
    results = AgentResults()
    
    try:
        # Run technical analysis
        tech_output = technical_analysis_agent.invoke({"stock_symbol": stock_symbol})
        results.technical_score, results.technical_summary = parse_agent_output(tech_output)
        
        # Run fundamental analysis  
        fund_output = fundamental_analysis_agent.invoke({"stock_symbol": stock_symbol})
        results.fundamental_score, results.fundamental_summary = parse_agent_output(fund_output)
        
        # Run macro/news analysis
        macro_output = macro_news_agent.invoke({"stock_symbol": stock_symbol})
        results.macro_score, results.macro_summary = parse_agent_output(macro_output)
        
        # Calculate overall score
        results.overall_score = results.technical_score + results.fundamental_score + results.macro_score
        
        logger.info(f"Multi-agent analysis completed for {stock_symbol}")
        logger.info(f"Scores - Technical: {results.technical_score}, Fundamental: {results.fundamental_score}, Macro: {results.macro_score}, Overall: {results.overall_score}")
        
    except Exception as e:
        logger.error(f"Error in multi-agent analysis: {e}")
        results.technical_summary = "Technical analysis failed"
        results.fundamental_summary = "Fundamental analysis failed"
        results.macro_summary = "Macro analysis failed"
    
    return results

def extract_stock_symbols_from_question(question: str) -> List[str]:
    """Extract stock symbols mentioned in the question"""
    question_upper = question.upper()
    mentioned_stocks = []
    
    for symbol in MOCK_STOCK_DATA.keys():
        if symbol in question_upper:
            mentioned_stocks.append(symbol)
    
    # Also check for company names
    company_names = {
        "NABIL": ["NABIL", "NABIL BANK"],
        "ADBL": ["ADBL", "AGRICULTURAL", "AGRICULTURE"],
        "EBL": ["EBL", "EVEREST", "EVEREST BANK"]
    }
    
    for symbol, names in company_names.items():
        for name in names:
            if name in question_upper and symbol not in mentioned_stocks:
                mentioned_stocks.append(symbol)
                break
    
    return mentioned_stocks

def parse_structured_answer(answer: str, mentioned_stocks: List[str], agent_results: Dict[str, AgentResults]) -> Dict[str, Any]:
    """
    Parse the AI answer into structured components for better UI display
    """
    import re
    
    # Extract sections from the answer
    sections = {
        "quick_answer": "",
        "key_insights": [],
        "recommendation": "",
        "risk_factors": "",
        "stock_metrics": {}
    }
    
    # Try to extract structured sections
    try:
        # Extract Quick Answer
        quick_match = re.search(r'\*\*QUICK ANSWER:\*\*\s*(.*?)(?=\*\*|$)', answer, re.DOTALL | re.IGNORECASE)
        if quick_match:
            sections["quick_answer"] = quick_match.group(1).strip()
        
        # Extract Key Insights
        insights_match = re.search(r'\*\*KEY INSIGHTS:\*\*(.*?)(?=\*\*|$)', answer, re.DOTALL | re.IGNORECASE)
        if insights_match:
            insights_text = insights_match.group(1).strip()
            sections["key_insights"] = [line.strip('• -').strip() for line in insights_text.split('\n') 
                                       if line.strip() and ('•' in line or '-' in line)]
        
        # Extract Recommendation
        rec_match = re.search(r'\*\*RECOMMENDATION:\*\*\s*(.*?)(?=\*\*|$)', answer, re.DOTALL | re.IGNORECASE)
        if rec_match:
            sections["recommendation"] = rec_match.group(1).strip()
        
        # Extract Risk Factors
        risk_match = re.search(r'\*\*RISK FACTORS:\*\*\s*(.*?)(?=\*\*|$)', answer, re.DOTALL | re.IGNORECASE)
        if risk_match:
            sections["risk_factors"] = risk_match.group(1).strip()
    
    except Exception as e:
        logger.warning(f"Could not parse structured answer: {e}")
    
    # Fallback: if no structured content found, create basic structure
    if not sections["quick_answer"]:
        # Take first 2 sentences as quick answer
        sentences = answer.split('. ')
        sections["quick_answer"] = '. '.join(sentences[:2]) + '.' if len(sentences) > 1 else answer[:200] + '...'
    
    # Add stock metrics for mentioned stocks
    for stock in mentioned_stocks:
        if stock in agent_results:
            results = agent_results[stock]
            sections["stock_metrics"][stock] = {
                "overall_score": results.overall_score,
                "technical_score": results.technical_score,
                "fundamental_score": results.fundamental_score,
                "macro_score": results.macro_score,
                "recommendation": get_recommendation_from_score(results.overall_score)
            }
    
    return sections

def get_recommendation_from_score(score: int) -> str:
    """Convert overall score to recommendation"""
    if score >= 5:
        return "BUY"
    elif score >= 2:
        return "HOLD"
    elif score >= -2:
        return "NEUTRAL"
    else:
        return "SELL"

def answer_natural_language_question(question: str) -> Dict[str, Any]:
    """
    Process natural language questions about stocks using multi-agent analysis
    """
    start_time = datetime.now()
    
    try:
        # Extract relevant stock symbols from the question
        mentioned_stocks = extract_stock_symbols_from_question(question)
        
        # If no stocks mentioned, provide general guidance
        if not mentioned_stocks:
            mentioned_stocks = list(MOCK_STOCK_DATA.keys())  # Analyze all stocks
        
        # Gather data for mentioned stocks
        stock_data = {}
        agent_results = {}
        
        for stock in mentioned_stocks:
            if stock in MOCK_STOCK_DATA:
                stock_data[stock] = MOCK_STOCK_DATA[stock]
                agent_results[stock] = run_multi_agent_analysis(stock)
        
        # Use LLM to answer the question with structured output
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        
        # Prepare context for the LLM with structured output requirements
        context = f"""
You are a professional financial analyst for NEPSE (Nepal Stock Exchange). Provide a CONCISE, STRUCTURED response to the user's question.

USER QUESTION: {question}

AVAILABLE STOCK DATA AND ANALYSIS:
"""
        
        for stock, results in agent_results.items():
            context += f"""
{stock}:
- Technical: {results.technical_score}/10 | {results.technical_summary[:100]}...
- Fundamental: {results.fundamental_score}/10 | {results.fundamental_summary[:100]}...  
- Macro: {results.macro_score}/10 | {results.macro_summary[:100]}...
- Overall: {results.overall_score}/10
- Key Data: P/E={stock_data[stock]['fundamentals']['pe_ratio']}, EPS={stock_data[stock]['fundamentals']['eps']}, Price={stock_data[stock]['technicals']['price']}

"""
        
        context += """
RESPONSE FORMAT REQUIRED:
Provide a JSON-like structured response with these sections:

**QUICK ANSWER:** [2-3 sentences directly answering the question]

**KEY INSIGHTS:**
• [Point 1 with specific numbers]
• [Point 2 with specific numbers] 
• [Point 3 with specific numbers]

**RECOMMENDATION:** [Clear BUY/HOLD/SELL with reasoning]

**RISK FACTORS:** [1-2 key risks to consider]

Keep each section CONCISE (max 2-3 lines each). Use specific numbers and data points. Be direct and actionable.
"""
        
        response = llm.invoke(context)
        
        # Handle response content
        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, list):
                answer = ' '.join(str(item) for item in content)
            else:
                answer = str(content)
        else:
            answer = str(response)
        
        # Determine confidence based on data availability
        confidence = "High" if len(mentioned_stocks) <= 2 else "Medium"
        if not any(stock in MOCK_STOCK_DATA for stock in mentioned_stocks):
            confidence = "Low"
        
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Parse the structured response
        parsed_response = parse_structured_answer(answer, mentioned_stocks, agent_results)
        
        return {
            "question": question,
            "answer": answer,  # Keep full answer for fallback
            "structured_response": parsed_response,
            "related_stocks": mentioned_stocks,
            "confidence": confidence,
            "timestamp": datetime.now().isoformat(),
            "processing_time_ms": processing_time
        }
        
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return {
            "question": question,
            "answer": f"I apologize, but I encountered an error while processing your question: {str(e)}. Please try rephrasing your question or contact support if the issue persists.",
            "related_stocks": mentioned_stocks if 'mentioned_stocks' in locals() else [],
            "confidence": "Low",
            "timestamp": datetime.now().isoformat(),
            "processing_time_ms": int((datetime.now() - start_time).total_seconds() * 1000)
        }

def generate_final_recommendation(stock_symbol: str, results: AgentResults) -> str:
    """
    Generate final investment recommendation using LLM synthesis
    """
    try:
        # Use the powerful reasoning model for final synthesis
        llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.1)
        
        synthesis_prompt = f"""
As a senior financial analyst for NEPSE, synthesize the following multi-agent analysis into a comprehensive investment recommendation for {stock_symbol}:

TECHNICAL ANALYSIS (Score: {results.technical_score}):
{results.technical_summary}

FUNDAMENTAL ANALYSIS (Score: {results.fundamental_score}):
{results.fundamental_summary}

MACRO/NEWS ANALYSIS (Score: {results.macro_score}):
{results.macro_summary}

OVERALL SCORE: {results.overall_score}

Provide a well-structured recommendation that includes:
1. Executive Summary (2-3 sentences)
2. Key Strengths and Weaknesses
3. Risk Assessment
4. Investment Recommendation (BUY/HOLD/SELL with conviction level)
5. Price Targets or Key Levels to Watch

End with: "Disclaimer: This is an AI-generated analysis and not financial advice. Always do your own research and consult with qualified financial advisors."

Write in a professional yet accessible tone suitable for both retail and institutional investors.
"""
        
        response = llm.invoke(synthesis_prompt)
        
        # Handle different response formats
        if hasattr(response, 'content'):
            content = response.content
            if isinstance(content, list):
                return ' '.join(str(item) for item in content)
            return str(content)
        else:
            return str(response)
            
    except Exception as e:
        logger.error(f"Error in final recommendation generation: {e}")
        
        # Fallback recommendation logic
        if results.overall_score >= 3:
            recommendation = "BUY - Strong positive signals across multiple dimensions"
        elif results.overall_score >= 1:
            recommendation = "BUY/HOLD - Generally positive outlook with some caution"
        elif results.overall_score >= -1:
            recommendation = "HOLD - Mixed signals, monitor closely"
        elif results.overall_score >= -3:
            recommendation = "SELL/HOLD - Negative signals, consider reducing position"
        else:
            recommendation = "SELL - Multiple negative indicators"
        
        return f"""
INVESTMENT RECOMMENDATION FOR {stock_symbol}:

Overall Score: {results.overall_score}
Recommendation: {recommendation}

Technical Analysis: {results.technical_summary[:100]}...
Fundamental Analysis: {results.fundamental_summary[:100]}...
Macro Analysis: {results.macro_summary[:100]}...

Disclaimer: This is an AI-generated analysis and not financial advice. Always do your own research and consult with qualified financial advisors.
"""

# --- Enhanced FastAPI Application ---

app = FastAPI(
    title="NEPSE Smart Multi-Agent System",
    description="AI-powered stock analysis using specialized agents for technical, fundamental, and macro analysis",
    version="2.0.0"
)

# Configure CORS to allow the Vue.js frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StockRequest(BaseModel):
    stock_symbol: str

class QuestionRequest(BaseModel):
    question: str

class AnalysisResponse(BaseModel):
    stock_symbol: str
    analysis: str
    overall_score: int
    agent_details: Dict[str, Dict[str, Any]]
    timestamp: str
    processing_time_ms: int

class QuestionResponse(BaseModel):
    question: str
    answer: str
    structured_response: Dict[str, Any]
    related_stocks: List[str]
    confidence: str
    timestamp: str  
    processing_time_ms: int

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "NEPSE Smart Multi-Agent System with Q&A",
        "status": "operational",
        "available_stocks": list(MOCK_STOCK_DATA.keys()),
        "agents": ["technical_analysis", "fundamental_analysis", "macro_news"],
        "features": ["stock_analysis", "natural_language_qa"],
        "example_questions": [
            "Is NABIL a good buy for the next 6 months?",
            "Which company has better fundamentals, NABIL or ADBL?",
            "What's the technical outlook for EBL?",
            "Compare the P/E ratios of all available stocks"
        ]
    }

@app.get("/stocks")
async def get_available_stocks():
    """Get list of available stocks for analysis"""
    return {
        "available_stocks": list(MOCK_STOCK_DATA.keys()),
        "total": len(MOCK_STOCK_DATA)
    }

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: StockRequest):
    """
    Perform comprehensive multi-agent analysis of a stock
    """
    start_time = datetime.now()
    stock_symbol = request.stock_symbol.upper()
    
    try:
        # Validate stock symbol
        if stock_symbol not in MOCK_STOCK_DATA:
            available_stocks = ", ".join(MOCK_STOCK_DATA.keys())
            raise HTTPException(
                status_code=404,
                detail=f"Stock symbol '{stock_symbol}' not found. Available stocks: {available_stocks}"
            )

        logger.info(f"Starting multi-agent analysis for {stock_symbol}")
        
        # Run the multi-agent analysis
        results = run_multi_agent_analysis(stock_symbol)
        
        # Generate final recommendation
        final_analysis = generate_final_recommendation(stock_symbol, results)
        
        # Calculate processing time
        processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
        
        # Structure the response
        response_data = {
            "stock_symbol": stock_symbol,
            "analysis": final_analysis,
            "overall_score": results.overall_score,
            "agent_details": {
                "technical_analysis": {
                    "score": results.technical_score,
                    "summary": results.technical_summary
                },
                "fundamental_analysis": {
                    "score": results.fundamental_score,
                    "summary": results.fundamental_summary
                },
                "macro_news_analysis": {
                    "score": results.macro_score,
                    "summary": results.macro_summary
                }
            },
            "timestamp": datetime.now().isoformat(),
            "processing_time_ms": processing_time
        }
        
        logger.info(f"Analysis completed for {stock_symbol} in {processing_time}ms")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error during analysis of {stock_symbol}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred during analysis. Please try again later."
        )

@app.get("/analyze/{stock_symbol}")
async def analyze_stock_get(stock_symbol: str):
    """
    GET endpoint for stock analysis (for easy testing)
    """
    request = StockRequest(stock_symbol=stock_symbol)
    return await analyze_stock(request)

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    """
    Natural language question answering about stocks using multi-agent analysis
    """
    try:
        logger.info(f"Processing question: {request.question}")
        
        # Validate question
        if not request.question.strip():
            raise HTTPException(
                status_code=400,
                detail="Question cannot be empty"
            )
        
        # Process the question
        result = answer_natural_language_question(request.question)
        
        logger.info(f"Question answered in {result['processing_time_ms']}ms")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your question. Please try again later."
        )

@app.get("/ask/{question}")
async def ask_question_get(question: str):
    """
    GET endpoint for asking questions (for easy testing)
    """
    request = QuestionRequest(question=question)
    return await ask_question(request)

"""
NEPSE Smart Multi-Agent Stock Analysis System

This enhanced system features:
- Three specialized AI agents (Technical, Fundamental, Macro/News)
- Sophisticated scoring and analysis algorithms  
- Comprehensive error handling and logging
- RESTful API with detailed responses
- Support for multiple NEPSE stocks

To run this application:

1. Install required packages:
   pip install fastapi uvicorn langchain langchain-groq pydantic

2. Set your Groq API key:
   export GROQ_API_KEY="your_api_key_here"

3. Run the development server:
   uvicorn nepse_agent_backend:app --reload --host 0.0.0.0 --port 8000

4. Open your browser to:
   - API docs: http://localhost:8000/docs
   - Frontend: Open index.html in your browser

Available endpoints:
- GET  /                    - Health check and system info
- GET  /stocks             - List available stocks  
- POST /analyze            - Comprehensive stock analysis
- GET  /analyze/{symbol}   - Quick analysis via GET

Example usage:
curl -X POST "http://localhost:8000/analyze" \
     -H "Content-Type: application/json" \
     -d '{"stock_symbol": "NABIL"}'
"""

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("nepse_agent_backend:app", host="0.0.0.0", port=8000, reload=True)