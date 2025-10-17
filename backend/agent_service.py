"""Services for LangChain-powered multi-agent analysis exposed via the core FastAPI app."""

from __future__ import annotations

import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Tuple, Optional

from fastapi import HTTPException
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from backend.nepse_data_service import NepseDataService
from pathlib import Path
import json

logger = logging.getLogger(__name__)
_data_service: Optional[NepseDataService] = None
_DATA_PATH = str((Path("/app") / "data").resolve())

# --- Helper objects ------------------------------------------------------------

class AgentResults:
    """Container for multi-agent execution results."""

    def __init__(self) -> None:
        self.technical_score = 0
        self.technical_summary = ""
        self.fundamental_score = 0
        self.fundamental_summary = ""
        self.macro_score = 0
        self.macro_summary = ""
        self.overall_score = 0

# --- Internal utilities --------------------------------------------------------

def _ensure_groq_key() -> None:
    """Raise an HTTPException if the GROQ API key is missing."""
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY is not configured. Please set it in your environment.",
        )


def _create_llm(model: str, temperature: float = 0.0) -> ChatGroq:
    """Create a ChatGroq client ensuring the API key is available."""
    _ensure_groq_key()
    return ChatGroq(model=model, temperature=temperature)


def _ensure_data_service() -> NepseDataService:
    global _data_service
    if _data_service is None:
        _data_service = NepseDataService(data_path=_DATA_PATH)
    return _data_service

def _get_active_symbols() -> List[str]:
    svc = _ensure_data_service()
    companies = svc.get_company_list() or []
    return sorted([str(c.get("symbol")) for c in companies if c.get("symbol")])


def _get_data_for_symbol(symbol: str) -> Dict[str, Any]:
    """Fetch and combine data needed for analysis for a given stock symbol."""
    svc = _ensure_data_service()

    # 1) Latest price record
    prices: List[Dict[str, Any]] = svc.get_daily_data('prices') or []
    price_record: Optional[Dict[str, Any]] = next(
        (item for item in prices if isinstance(item, dict) and item.get("symbol") == symbol),
        None,
    )
    if not price_record:
        return {}

    # 2) Technicals: try to load from daily technicals (list) else derive light-weight placeholders
    technicals_list: List[Dict[str, Any]] = svc.get_daily_data('technicals') or []
    technicals: Dict[str, Any] = {}
    if isinstance(technicals_list, list):
        technicals = next(
            (t for t in technicals_list if isinstance(t, dict) and t.get("symbol") == symbol),
            {},
        )
    if not technicals:
        # Derive minimal technicals deterministically from available price info
        price = price_record.get('ltp') or price_record.get('close_price') or price_record.get('price') or 0.0
        diff_pct = price_record.get('diff_percent') or 0.0
        # Simple EMA approximations and RSI in [25, 75] based on price and diff
        ema_21 = round(price * (1 - 0.01 * (1 if diff_pct < 0 else -1)), 2) if price else None
        ema_50 = round(price * 0.97, 2) if price else None
        rsi_14 = max(25, min(75, 50 + int(diff_pct))) if isinstance(diff_pct, (int, float)) else 50
        technicals = {
            "symbol": symbol,
            "price": price,
            "ema_21": ema_21,
            "ema_50": ema_50,
            "rsi_14": rsi_14,
            "volume": price_record.get('volume'),
            "52_week_high": round(price * 1.2, 2) if price else None,
            "52_week_low": round(price * 0.8, 2) if price else None,
            "macd_signal": "bullish" if diff_pct and diff_pct > 0 else "bearish",
        }

    # 3) Fundamentals (mocked for now but seeded from price record when possible)
    logger.warning("Fundamental data is currently mocked. Replace with a real data source when available.")
    fundamentals: Dict[str, Any] = {
        "pe_ratio": price_record.get('pe_ratio') or 18.5,
        "eps": price_record.get('eps') or 45.2,
        "debt_to_equity": 0.8,
        "status": "stable",
        "market_cap": price_record.get('market_cap') or 42.5,
        "book_value": price_record.get('book_value') or 520.0,
        "dividend_yield": price_record.get('dividend_yield') or 8.2,
    }

    # 4) Macro/news context (very light)
    news: List[str] = []
    try:
        index_info = svc.get_nepse_index().get('nepse_index') or {}
        if index_info:
            news.append(f"NEPSE Index is currently at {index_info.get('current_value', 'N/A')}")
    except Exception:
        pass
    try:
        macro_data = svc.get_macro_data()
        fx = macro_data.get('forex_rates')
        if isinstance(fx, list) and fx:
            # Try to surface USD rate if present
            usd = next((item for item in fx if str(item.get('currency', '')).upper() == 'USD'), None)
            if usd:
                # 'rates' structure may vary; just indicate availability
                news.append("USD forex rate updated in latest macro snapshot")
    except Exception:
        pass

    return {"fundamentals": fundamentals, "technicals": technicals, "news": news}






# --- Agent implementations -----------------------------------------------------

def technical_analysis_agent(stock_symbol: str) -> str:
    """Perform rule-based technical analysis for the given stock."""
    logger.info("Running Technical Analysis for %s", stock_symbol)
    data = _get_data_for_symbol(stock_symbol).get("technicals")
    
    if not data:
        return "Technical data not found. Score: 0."

    buy_signals = 0
    sell_signals = 0
    signals_detail: List[str] = []

    # Rule 1: Trend via EMAs
    if data.get("price") and data.get("ema_21") and data.get("ema_50") and data["price"] > data["ema_21"] > data["ema_50"]:
        buy_signals += 2
        signals_detail.append("Strong uptrend: Price above both EMAs")
    elif data.get("price") and data.get("ema_21") and data["price"] > data["ema_21"]:
        buy_signals += 1
        signals_detail.append("Mild uptrend: Price above 21-day EMA")
    elif data.get("price") and data.get("ema_21") and data.get("ema_50") and data["price"] < data["ema_21"] < data["ema_50"]:
        sell_signals += 2
        signals_detail.append("Strong downtrend: Price below both EMAs")
    else:
        sell_signals += 1
        signals_detail.append("Weak trend: Price below 21-day EMA")

    # Rule 2: RSI
    rsi = data.get("rsi_14")
    if rsi:
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

    # Rule 3: MACD
    macd = data.get("macd_signal")
    if macd:
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

    # Rule 4: Price position within 52-week range
    if data.get("52_week_high") and data.get("52_week_low"):
        price_range = data["52_week_high"] - data["52_week_low"]
        if price_range > 0:
            current_position = (data["price"] - data["52_week_low"]) / price_range
            if current_position > 0.8:
                sell_signals += 1
                signals_detail.append("Near 52-week high - potential resistance")
            elif current_position < 0.2:
                buy_signals += 1
                signals_detail.append("Near 52-week low - potential support")

    # Rule 5: Volume influence
    avg_volume = 1_000_000
    if data.get("volume") and data["volume"] > avg_volume * 1.5:
        if buy_signals > sell_signals:
            buy_signals += 1
            signals_detail.append("High volume supports bullish sentiment")
        else:
            sell_signals += 1
            signals_detail.append("High volume supports bearish sentiment")

    score = buy_signals - sell_signals
    summary = (
        f"Technical Analysis for {stock_symbol}: "
        f"Buy signals: {buy_signals}, Sell signals: {sell_signals}. "
        f"Overall technical score: {score}. "
        f"Key findings: {'; '.join(signals_detail[:3])}."
    )
    return summary


def fundamental_analysis_agent(stock_symbol: str) -> str:


    """Perform rule-based fundamental analysis for the given stock."""


    logger.info("Running Fundamental Analysis for %s", stock_symbol)


    data = _get_data_for_symbol(stock_symbol).get("fundamentals")


    


    if not data:


        return "Fundamental data not found. Score: 0."





    score = 0


    positive_factors: List[str] = []


    negative_factors: List[str] = []





    status = data.get("status", "stable")


    if status == "dwindling":


        score -= 3


        negative_factors.append("Company fundamentals are deteriorating")


        return (


            f"CRITICAL: Fundamental status is 'dwindling'. Major red flag. Score: {score}."


        )


    if status == "strong":


        score += 2


        positive_factors.append("Strong fundamental position")


    elif status == "stable":


        score += 1


        positive_factors.append("Stable fundamental metrics")





    pe_ratio = data.get("pe_ratio")


    if pe_ratio:


        if pe_ratio < 15:


            score += 2


            positive_factors.append(f"Attractive valuation (P/E: {pe_ratio})")


        elif pe_ratio < 20:


            score += 1


            positive_factors.append(f"Reasonable valuation (P/E: {pe_ratio})")


        elif pe_ratio > 30:


            score -= 2


            negative_factors.append(f"Very high P/E ratio ({pe_ratio})")


        elif pe_ratio > 25:


            score -= 1


            negative_factors.append(f"High P/E ratio ({pe_ratio})")





    eps = data.get("eps")


    if eps:


        if eps > 50:


            score += 2


            positive_factors.append(f"Strong earnings (EPS: {eps})")


        elif eps > 30:


            score += 1


            positive_factors.append(f"Good earnings (EPS: {eps})")


        elif eps < 20:


            score -= 1


            negative_factors.append(f"Low earnings (EPS: {eps})")





    debt_to_equity = data.get("debt_to_equity")


    if debt_to_equity:


        if debt_to_equity < 0.5:


            score += 1


            positive_factors.append("Low debt levels")


        elif debt_to_equity > 1.0:


            score -= 1


            negative_factors.append("High debt-to-equity ratio")





    dividend_yield = data.get("dividend_yield", 0)


    if dividend_yield:


        if dividend_yield > 8:


            score += 1


            positive_factors.append(f"High dividend yield ({dividend_yield}%)")


        elif dividend_yield > 5:


            positive_factors.append(f"Good dividend yield ({dividend_yield}%)")





    market_cap = data.get("market_cap", 0)


    if market_cap:


        if market_cap > 50:


            positive_factors.append("Large-cap stability")


        elif market_cap < 10:


            negative_factors.append("Small-cap volatility risk")





    summary = (


        f"Fundamental Analysis for {stock_symbol}: "


        f"Status: {status.upper()}. "


        f"Overall fundamental score: {score}. "


    )





    if positive_factors:


        summary += f"Strengths: {'; '.join(positive_factors[:2])}. "


    if negative_factors:


        summary += f"Concerns: {'; '.join(negative_factors[:2])}. "





    summary += (


        f"Key metrics - P/E: {pe_ratio}, EPS: {eps}, D/E: {debt_to_equity}."


    )


    return summary








def macro_news_agent(stock_symbol: str) -> str:


    """Analyze macro/news sentiment for the stock using an LLM (with fallback)."""


    logger.info("Running Macro/News Analysis for %s", stock_symbol)


    news = _get_data_for_symbol(stock_symbol).get("news")


    


    if not news:


        return "No news found. Score: 0."





    try:


        llm = _create_llm(model="llama-3.1-8b-instant", temperature=0.0)


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


        response = chain.invoke(


            {


                "news_items": "\n".join(f"• {item}" for item in news),


                "stock_symbol": stock_symbol,


            }


        )


        if hasattr(response, "content"):


            content = response.content


            if isinstance(content, list):


                content = " ".join(str(item) for item in content)


            else:


                content = str(content)


        else:


            content = str(response)





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





        return (


            f"Macro/News Analysis for {stock_symbol}: {content.strip()}. "


            f"Overall macro score: {score}."


        )





    except HTTPException:


        raise


    except Exception as exc:  # pragma: no cover - fallback path


        logger.error("Error in Macro News Agent: %s", exc)


        positive_keywords = [


            "growth",


            "incentive",


            "strong",


            "expansion",


            "profit",


            "increase",


        ]


        negative_keywords = [


            "decline",


            "loss",


            "pressure",


            "challenge",


            "slowdown",


            "uncertainty",


        ]


        positive_count = sum(


            1


            for item in news


            for keyword in positive_keywords


            if keyword in item.lower()


        )


        negative_count = sum(


            1


            for item in news


            for keyword in negative_keywords


            if keyword in item.lower()


        )


        score = positive_count - negative_count


        sentiment = "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"


        return (


            "Macro/News Analysis (fallback): "


            f"{sentiment} sentiment detected. Score: {score}. "


            f"Key themes from {len(news)} news items analyzed."


        )


# --- Orchestration utilities ---------------------------------------------------

def parse_agent_output(output: str) -> Tuple[int, str]:
    """Extract score and the original summary from an agent output."""
    score_patterns = [
        r"score:?\s*([+-]?\d+)",
        r"overall.*?score:?\s*([+-]?\d+)",
        r"Score:?\s*([+-]?\d+)",
    ]
    for pattern in score_patterns:
        match = re.search(pattern, output, re.IGNORECASE)
        if match:
            try:
                score = int(match.group(1))
                return score, output
            except ValueError:
                continue
    return 0, output


def run_multi_agent_analysis(stock_symbol: str) -> AgentResults:
    """Execute all agents for the provided stock symbol."""
    results = AgentResults()

    try:
        tech_output = technical_analysis_agent(stock_symbol)
        (
            results.technical_score,
            results.technical_summary,
        ) = parse_agent_output(tech_output)

        fund_output = fundamental_analysis_agent(stock_symbol)
        (
            results.fundamental_score,
            results.fundamental_summary,
        ) = parse_agent_output(fund_output)

        macro_output = macro_news_agent(stock_symbol)
        (results.macro_score, results.macro_summary) = parse_agent_output(macro_output)

        results.overall_score = (
            results.technical_score
            + results.fundamental_score
            + results.macro_score
        )
        logger.info(
            "Multi-agent analysis completed for %s", stock_symbol
        )
        logger.info(
            "Scores - Technical: %s, Fundamental: %s, Macro: %s, Overall: %s",
            results.technical_score,
            results.fundamental_score,
            results.macro_score,
            results.overall_score,
        )
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Error in multi-agent analysis: %s", exc)
        results.technical_summary = "Technical analysis failed"
        results.fundamental_summary = "Fundamental analysis failed"
        results.macro_summary = "Macro analysis failed"
    return results

def extract_stock_symbols_from_question(question: str) -> List[str]:
    """Extract known stock symbols or names mentioned in a free-form question."""
    question_upper = question.upper()
    mentioned_stocks: List[str] = []

    # Use active symbols when available
    active_symbols = set(_get_active_symbols() or [])
    if not active_symbols:
        # Fallback to a default list if no active symbols are found
        active_symbols = ["NABIL", "ADBL", "EBL"]

    for symbol in active_symbols:
        if symbol in question_upper:
            mentioned_stocks.append(symbol)

    # Try mapping by company_name from prices
    svc = _ensure_data_service()
    prices = svc.get_daily_data("prices") or []
    for rec in prices:
        sym = rec.get("symbol")
        name = str(rec.get("company_name", "")).upper()
        if not sym or not name:
            continue
        if name in question_upper and sym not in mentioned_stocks:
            mentioned_stocks.append(sym)
    return mentioned_stocks


def get_recommendation_from_score(score: int) -> str:
    if score >= 5:
        return "BUY"
    if score >= 2:
        return "HOLD"
    if score >= -2:
        return "NEUTRAL"
    return "SELL"


def parse_structured_answer(
    answer: str,
    mentioned_stocks: List[str],
    agent_results: Dict[str, AgentResults],
) -> Dict[str, Any]:
    """Parse the LLM answer into structured sections for UI display."""
    sections: Dict[str, Any] = {
        "quick_answer": "",
        "key_insights": [],
        "recommendation": "",
        "risk_factors": "",
        "stock_metrics": {},
    }

    try:
        quick_match = re.search(
            r"\*\*QUICK ANSWER:\*\*\s*(.*?)(?=\*\*|$)",
            answer,
            re.DOTALL | re.IGNORECASE,
        )
        if quick_match:
            sections["quick_answer"] = quick_match.group(1).strip()

        insights_match = re.search(
            r"\*\*KEY INSIGHTS:\*\*(.*?)(?=\*\*|$)",
            answer,
            re.DOTALL | re.IGNORECASE,
        )
        if insights_match:
            insights_text = insights_match.group(1).strip()
            sections["key_insights"] = [
                line.strip("• -").strip()
                for line in insights_text.split("\n")
                if line.strip() and ("•" in line or "-" in line)
            ]

        rec_match = re.search(
            r"\*\*RECOMMENDATION:\*\*\s*(.*?)(?=\*\*|$)",
            answer,
            re.DOTALL | re.IGNORECASE,
        )
        if rec_match:
            sections["recommendation"] = rec_match.group(1).strip()

        risk_match = re.search(
            r"\*\*RISK FACTORS:\*\*\s*(.*?)(?=\*\*|$)",
            answer,
            re.DOTALL | re.IGNORECASE,
        )
        if risk_match:
            sections["risk_factors"] = risk_match.group(1).strip()

    except Exception as exc:  # pragma: no cover - defensive parsing
        logger.warning("Could not parse structured answer: %s", exc)

    if not sections["quick_answer"]:
        sentences = [s for s in answer.split(". ") if s]
        if sentences:
            sections["quick_answer"] = ". ".join(sentences[:2]) + "."
        else:
            sections["quick_answer"] = answer[:200] + "..."

    for stock in mentioned_stocks:
        if stock in agent_results:
            results = agent_results[stock]
            sections["stock_metrics"][stock] = {
                "overall_score": results.overall_score,
                "technical_score": results.technical_score,
                "fundamental_score": results.fundamental_score,
                "macro_score": results.macro_score,
                "recommendation": get_recommendation_from_score(
                    results.overall_score
                ),
            }
    return sections


# --- Public API ----------------------------------------------------------------

def perform_stock_analysis(stock_symbol: str) -> Dict[str, Any]:
    """Run the full agent pipeline for a single stock."""
    stock_symbol = stock_symbol.upper()
    active = set(_get_active_symbols() or [])
    if active and stock_symbol not in active:
        raise HTTPException(status_code=404, detail=f"Unknown or inactive symbol: {stock_symbol}")

    start_time = datetime.now()
    results = run_multi_agent_analysis(stock_symbol)

    try:
        llm_response = generate_final_recommendation(stock_symbol, results)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        logger.error("Failed to generate final recommendation: %s", exc)
        llm_response = (
            "Investment recommendation currently unavailable due to an error."
        )

    processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
    return {
        "stock_symbol": stock_symbol,
        "analysis": llm_response,
        "overall_score": results.overall_score,
        "agent_details": {
            "technical_analysis": {
                "score": results.technical_score,
                "summary": results.technical_summary,
            },
            "fundamental_analysis": {
                "score": results.fundamental_score,
                "summary": results.fundamental_summary,
            },
            "macro_news_analysis": {
                "score": results.macro_score,
                "summary": results.macro_summary,
            },
        },
        "timestamp": datetime.now().isoformat(),
        "processing_time_ms": processing_time,
    }



def answer_natural_language_question(question: str) -> Dict[str, Any]:
    """Answer a natural language question using the multi-agent pipeline."""
    question = question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    start_time = datetime.now()
    mentioned_stocks = extract_stock_symbols_from_question(question)

    # Filter to active symbols if available; otherwise keep what was found
    active = set(_get_active_symbols() or [])
    if active:
        mentioned_stocks = [s for s in mentioned_stocks if s in active]

    # If still empty, pick a small representative set (prefer a few active ones)
    if not mentioned_stocks:
        if active:
            mentioned_stocks = list(sorted(active))[:3]
        else:
            # Fallback to a default list if no active symbols are found
            mentioned_stocks = ["NABIL", "ADBL", "EBL"]

    stock_data: Dict[str, Dict[str, Any]] = {}
    agent_results: Dict[str, AgentResults] = {}

    for stock in mentioned_stocks:
        stock_data[stock] = _get_data_for_symbol(stock)
        agent_results[stock] = run_multi_agent_analysis(stock)

    try:
        llm = _create_llm(model="llama-3.3-70b-versatile", temperature=0.1)
    except HTTPException:
        raise

    context = """
You are a professional financial analyst for NEPSE (Nepal Stock Exchange). Provide a CONCISE, STRUCTURED response to the user's question.

USER QUESTION: {question}

AVAILABLE STOCK DATA AND ANALYSIS:
"""
    for stock, results in agent_results.items():
        fundamentals = stock_data[stock].get("fundamentals", {})
        technicals = stock_data[stock].get("technicals", {})
        context += (
            f"\n{stock}:\n"
            f"- Technical: {results.technical_score}/10 | {results.technical_summary[:140]}...\n"
            f"- Fundamental: {results.fundamental_score}/10 | {results.fundamental_summary[:140]}...\n"
            f"- Macro: {results.macro_score}/10 | {results.macro_summary[:140]}...\n"
            f"- Overall: {results.overall_score}/10\n"
            f"- Key Data: P/E={fundamentals.get('pe_ratio')}, EPS={fundamentals.get('eps')}, Price={technicals.get('price')}, RSI={technicals.get('rsi_14')}\n"
        )

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

    try:
        response = llm.invoke(context.format(question=question))
        if hasattr(response, "content"):
            content = response.content
            if isinstance(content, list):
                answer = " ".join(str(item) for item in content)
            else:
                answer = str(content)
        else:
            answer = str(response)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        logger.error("Error answering question: %s", exc)
        answer = (
            "I encountered an error while processing your question. "
            "Please try again later."
        )

    parsed_response = parse_structured_answer(answer, mentioned_stocks, agent_results)
    confidence = "High" if len(mentioned_stocks) <= 2 else "Medium"

    processing_time = int((datetime.now() - start_time).total_seconds() * 1000)
    return {
        "question": question,
        "answer": answer,
        "structured_response": parsed_response,
        "related_stocks": mentioned_stocks,
        "confidence": confidence,
        "timestamp": datetime.now().isoformat(),
        "processing_time_ms": processing_time,
    }


def generate_final_recommendation(stock_symbol: str, results: AgentResults) -> str:
    """Generate a synthesis report for the analyzed stock using an LLM."""
    try:
        llm = _create_llm(model="llama-3.3-70b-versatile", temperature=0.1)
    except HTTPException:
        raise

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
    try:
        response = llm.invoke(synthesis_prompt)
        if hasattr(response, "content"):
            content = response.content
            if isinstance(content, list):
                return " ".join(str(item) for item in content)
            return str(content)
        return str(response)
    except HTTPException:
        raise
    except Exception as exc:  # pragma: no cover
        logger.error("Error in final recommendation generation: %s", exc)
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
        return (
            f"INVESTMENT RECOMMENDATION FOR {stock_symbol}:\n\n"
            f"Overall Score: {results.overall_score}\n"
            f"Recommendation: {recommendation}\n\n"
            f"Technical Analysis: {results.technical_summary[:100]}...\n"
            f"Fundamental Analysis: {results.fundamental_summary[:100]}...\n"
            f"Macro Analysis: {results.macro_summary[:100]}...\n\n"
            "Disclaimer: This is an AI-generated analysis and not financial advice. "
            "Always do your own research and consult with qualified financial advisors."
        )



