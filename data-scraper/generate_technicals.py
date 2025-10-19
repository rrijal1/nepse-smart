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

        # RSI (14) using clipped deltas to avoid dtype issues
        delta = group['close'].diff()
        gain = delta.clip(lower=0)
        loss = (-delta).clip(lower=0)
        roll_up = gain.rolling(window=14).mean()
        roll_down = loss.rolling(window=14).mean()
        rs = roll_up / roll_down
        group['rsi_14'] = 100 - (100 / (1 + rs))

        # MACD
        exp1 = group['close'].ewm(span=12, adjust=False).mean()
        exp2 = group['close'].ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        # Store as columns for convenience
        group['macd'] = macd
        group['signal'] = signal

        latest = group.iloc[-1]
        previous = group.iloc[-2] if len(group) > 1 else latest

        # Determine MACD signal with guards for NaN/short series
        macd_signal_state = "neutral"
        try:
            latest_macd_opt = float(latest['macd']) if pd.notna(latest['macd']) else None
            latest_signal_opt = float(latest['signal']) if pd.notna(latest['signal']) else None
            prev_macd_opt = float(previous['macd']) if pd.notna(previous['macd']) else None
            prev_signal_opt = float(previous['signal']) if pd.notna(previous['signal']) else None

            if (
                latest_macd_opt is not None and latest_signal_opt is not None and
                prev_macd_opt is not None and prev_signal_opt is not None
            ):
                latest_macd_val: float = latest_macd_opt
                latest_signal_val: float = latest_signal_opt
                prev_macd_val: float = prev_macd_opt
                prev_signal_val: float = prev_signal_opt

                if latest_macd_val > latest_signal_val and prev_macd_val < prev_signal_val:
                    macd_signal_state = "bullish_crossover"
                elif latest_macd_val < latest_signal_val and prev_macd_val > prev_signal_val:
                    macd_signal_state = "bearish_crossover"
        except Exception:
            macd_signal_state = "neutral"

        # Resolve price preference
        price_val = None
        if isinstance(latest, pd.Series):
            if 'ltp' in latest and pd.notna(latest['ltp']):
                price_val = float(latest['ltp'])
            elif 'close' in latest and pd.notna(latest['close']):
                price_val = float(latest['close'])

        all_technicals[symbol] = {
            "price": price_val,
            "ema_21": latest['ema_21'],
            "ema_50": latest['ema_50'],
            "rsi_14": latest['rsi_14'],
            "macd_signal": macd_signal_state,
            "volume": latest.get('vol') if isinstance(latest, pd.Series) else None,
            "52_week_high": latest.get('52_weeks_high') if isinstance(latest, pd.Series) else None,
            "52_week_low": latest.get('52_weeks_low') if isinstance(latest, pd.Series) else None,
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
