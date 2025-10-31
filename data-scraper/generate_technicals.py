#!/usr/bin/env python3
"""
Generate Technical Indicators from API
- Fetches historical price data from API
- Calculates technical indicators (RSI, MACD) for all stocks
- Saves the indicators to data/technicals directory
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging
import requests
import sys
import os

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from shared_utils import setup_logging

class TechnicalIndicatorsGenerator:
    """Generate technical indicators from API data"""

    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.logger = setup_logging("technical_indicators")

    def fetch_company_list(self) -> list:
        """Fetch list of all companies from API"""
        try:
            response = requests.get(f"{self.api_base_url}/api/company-list")
            response.raise_for_status()
            data = response.json()
            return data.get("companies", [])
        except Exception as e:
            self.logger.error(f"Failed to fetch company list: {e}")
            return []

    def fetch_company_history(self, symbol: str, days: int = 90) -> list:
        """Fetch historical price data for a specific company"""
        try:
            response = requests.get(f"{self.api_base_url}/api/company-history/{symbol}", params={"days": days})
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])
        except Exception as e:
            self.logger.debug(f"Failed to fetch history for {symbol}: {e}")
            return []

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI (Relative Strength Index)"""
        delta = prices.diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)

        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))

        return rsi

    def calculate_macd(self, prices: pd.Series, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> tuple:
        """Calculate MACD (Moving Average Convergence Divergence)"""
        fast_ema = prices.ewm(span=fast_period, adjust=False).mean()
        slow_ema = prices.ewm(span=slow_period, adjust=False).mean()

        macd_line = fast_ema - slow_ema
        signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
        histogram = macd_line - signal_line

        return macd_line, signal_line, histogram

    def calculate_technical_indicators(self, price_data: list) -> dict:
        """Calculate technical indicators for a single stock's price data"""
        if not price_data or len(price_data) < 14:
            return {}

        # Convert to DataFrame
        df = pd.DataFrame(price_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df.set_index('date', inplace=True)

        # Ensure we have close prices
        if 'close' not in df.columns:
            return {}

        close_prices = df['close']

        # Calculate RSI (14)
        rsi_14 = self.calculate_rsi(close_prices, 14)

        # Calculate MACD (12, 26, 9)
        macd_line, signal_line, histogram = self.calculate_macd(close_prices, 12, 26, 9)

        # Get latest values
        latest_rsi = rsi_14.iloc[-1] if len(rsi_14) > 0 and pd.notna(rsi_14.iloc[-1]) else None
        latest_macd = macd_line.iloc[-1] if len(macd_line) > 0 and pd.notna(macd_line.iloc[-1]) else None
        latest_signal = signal_line.iloc[-1] if len(signal_line) > 0 and pd.notna(signal_line.iloc[-1]) else None
        latest_histogram = histogram.iloc[-1] if len(histogram) > 0 and pd.notna(histogram.iloc[-1]) else None

        # Determine MACD signal
        macd_signal = "neutral"
        if len(macd_line) >= 2 and len(signal_line) >= 2:
            prev_macd = macd_line.iloc[-2]
            prev_signal = signal_line.iloc[-2]

            if (pd.notna(latest_macd) and pd.notna(latest_signal) and
                pd.notna(prev_macd) and pd.notna(prev_signal)):
                if latest_macd > latest_signal and prev_macd <= prev_signal:
                    macd_signal = "bullish_crossover"
                elif latest_macd < latest_signal and prev_macd >= prev_signal:
                    macd_signal = "bearish_crossover"

        # Get additional data
        latest_data = df.iloc[-1]
        current_price = latest_data.get('close')
        volume = latest_data.get('volume')

        return {
            "symbol": price_data[0].get('symbol', 'UNKNOWN'),
            "current_price": float(current_price) if pd.notna(current_price) else None,
            "volume": float(volume) if pd.notna(volume) else None,
            "rsi_14": float(latest_rsi) if latest_rsi is not None else None,
            "macd": {
                "line": float(latest_macd) if latest_macd is not None else None,
                "signal": float(latest_signal) if latest_signal is not None else None,
                "histogram": float(latest_histogram) if latest_histogram is not None else None,
                "signal_state": macd_signal
            },
            "data_points": len(price_data),
            "last_updated": datetime.now().isoformat(),
            "indicators_calculated": ["rsi_14", "macd"]
        }

    def generate_all_technicals(self) -> dict:
        """Generate technical indicators for all stocks"""
        self.logger.info("🚀 Starting technical indicators generation from API...")

        # Fetch company list
        companies = self.fetch_company_list()
        if not companies:
            self.logger.error("No companies found, cannot generate technicals")
            return {}

        self.logger.info(f"📊 Found {len(companies)} companies to process")

        all_technicals = {}
        processed_count = 0
        error_count = 0

        for company in companies:
            symbol = company.get('symbol')
            if not symbol:
                continue

            try:
                # Fetch historical data (90 days for better indicator calculation)
                price_history = self.fetch_company_history(symbol, days=90)

                if not price_history or len(price_history) < 14:
                    self.logger.debug(f"⚠️ Insufficient data for {symbol} ({len(price_history)} points)")
                    error_count += 1
                    continue

                # Calculate technical indicators
                technicals = self.calculate_technical_indicators(price_history)

                if technicals:
                    all_technicals[symbol] = technicals
                    processed_count += 1

                    if processed_count % 50 == 0:
                        self.logger.info(f"📈 Processed {processed_count}/{len(companies)} companies...")

            except Exception as e:
                self.logger.error(f"❌ Error processing {symbol}: {e}")
                error_count += 1
                continue

        self.logger.info(f"✅ Generated technical indicators for {processed_count} companies")
        if error_count > 0:
            self.logger.warning(f"⚠️ Failed to process {error_count} companies")

        return all_technicals

    def save_technicals(self, technicals_data: dict, output_dir: str = "data/technicals") -> str:
        """Save technical indicators to JSON file"""
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"technicals_{timestamp}.json"
        filepath = output_path / filename

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(technicals_data, f, indent=2, ensure_ascii=False)

            self.logger.info(f"💾 Saved technical indicators to {filepath}")
            self.logger.info(f"   📊 Total stocks: {len(technicals_data)}")
            self.logger.info(f"   📁 File: {filepath}")

            return str(filepath)

        except Exception as e:
            self.logger.error(f"❌ Failed to save technical indicators: {e}")
            return ""

def main():
    """Main function to generate technical indicators from API"""
    generator = TechnicalIndicatorsGenerator()

    # Generate technical indicators
    technicals = generator.generate_all_technicals()

    if technicals:
        # Save to file
        filepath = generator.save_technicals(technicals)
        if filepath:
            print(f"✅ Technical indicators generated successfully: {filepath}")
        else:
            print("❌ Failed to save technical indicators")
            sys.exit(1)
    else:
        print("❌ No technical indicators generated")
        sys.exit(1)

if __name__ == "__main__":
    main()
