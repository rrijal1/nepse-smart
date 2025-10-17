#!/usr/bin/env python3
"""
Generate Technical Indicators
- Calculates technical indicators for all stocks using historical data
- Saves the indicators to a daily file for the AI agent to use
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
import logging

from shared_utils import setup_logging, create_data_filepath, create_historical_filepath

def calculate_technical_indicators(historical_prices_path: Path, output_path: Path, logger: logging.Logger):
    """
    Calculates technical indicators for all stocks from historical data.
    """
    try:
        with open(historical_prices_path, 'r') as f:
            historical_data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Historical prices file not found at {historical_prices_path}")
        return
    except json.JSONDecodeError:
        logger.error(f"Error decoding JSON from {historical_prices_path}")
        return

    if not historical_data:
        logger.warning("Historical data is empty. No indicators will be generated.")
        return

    df = pd.DataFrame(historical_data)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by=['symbol', 'date'])

    all_technicals = {}

    for symbol, group in df.groupby('symbol'):
        group = group.copy()
        group.set_index('date', inplace=True)
        
        # EMA
        group['ema_21'] = group['close'].ewm(span=21, adjust=False).mean()
        group['ema_50'] = group['close'].ewm(span=50, adjust=False).mean()
        
        # RSI
        delta = group['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        group['rsi_14'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = group['close'].ewm(span=12, adjust=False).mean()
        exp2 = group['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        
        latest = group.iloc[-1]
        previous = group.iloc[-2] if len(group) > 1 else latest

        all_technicals[symbol] = {
            "price": latest.get('ltp'),
            "ema_21": latest['ema_21'],
            "ema_50": latest['ema_50'],
            "rsi_14": latest['rsi_14'],
            "macd_signal": "bullish_crossover" if latest['macd'] > latest['signal'] and previous['macd'] < previous['signal'] else "bearish_crossover" if latest['macd'] < latest['signal'] and previous['macd'] > previous['signal'] else "neutral",
            "volume": latest.get('vol'),
            "52_week_high": latest.get('52_weeks_high'),
            "52_week_low": latest.get('52_weeks_low'),
        }

    try:
        with open(output_path, 'w') as f:
            json.dump(all_technicals, f, indent=2)
        logger.info(f"Successfully generated technical indicators for {len(all_technicals)} stocks at {output_path}")
    except IOError as e:
        logger.error(f"Error writing technical indicators to {output_path}: {e}")


def main():
    """Main function to generate technical indicators."""
    logger = setup_logging("generate_technicals")
    
    today_str = datetime.now().strftime('%Y-%m-%d')
    historical_prices_path = Path(create_historical_filepath("prices"))
    output_path = Path(create_data_filepath("technicals", today_str))
    
    calculate_technical_indicators(historical_prices_path, output_path, logger)

if __name__ == "__main__":
    main()
