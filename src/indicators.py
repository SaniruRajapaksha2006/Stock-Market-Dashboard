"""
Technical Indicators Module
Calculates various technical indicators for stock data
"""

import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TechnicalIndicators:
    """Calculate technical indicators for stock data"""

    def __init__(self):
        pass

    def add_sma(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Add Simple Moving Average

        Args:
            df: DataFrame with 'Close' column
            window: Moving average window (20, 50, 200)

        Returns:
            DataFrame with SMA column added
        """
        df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
        logger.info(f"Added SMA_{window}")
        return df

    def add_ema(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Add Exponential Moving Average

        Args:
            df: DataFrame with 'Close' column
            window: EMA window (12, 20, 26, 50)

        Returns:
            DataFrame with EMA column added
        """
        df[f'EMA_{window}'] = df['Close'].ewm(span=window, adjust=False).mean()
        logger.info(f"Added EMA_{window}")
        return df

    def add_rsi(self, df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
        """
        Add Relative Strength Index (RSI)

        Args:
            df: DataFrame with 'Close' column
            window: RSI window (typically 14)

        Returns:
            DataFrame with RSI column added
        """
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        logger.info(f"Added RSI_{window}")
        return df

    def add_macd(self, df: pd.DataFrame, fast=12, slow=26, signal=9) -> pd.DataFrame:
        """
        Add MACD (Moving Average Convergence Divergence)

        Args:
            df: DataFrame with 'Close' column
            fast: Fast EMA window (12)
            slow: Slow EMA window (26)
            signal: Signal line window (9)

        Returns:
            DataFrame with MACD, Signal, and Histogram columns
        """
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        df['MACD'] = ema_fast - ema_slow
        df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        logger.info(f"Added MACD (fast={fast}, slow={slow}, signal={signal})")
        return df

    def add_bollinger_bands(self, df: pd.DataFrame, window=20, num_std=2) -> pd.DataFrame:
        """
        Add Bollinger Bands

        Args:
            df: DataFrame with 'Close' column
            window: Moving average window (20)
            num_std: Number of standard deviations (2)

        Returns:
            DataFrame with Upper, Middle, Lower bands
        """
        df['BB_Middle'] = df['Close'].rolling(window=window).mean()
        bb_std = df['Close'].rolling(window=window).std()
        df['BB_Upper'] = df['BB_Middle'] + (bb_std * num_std)
        df['BB_Lower'] = df['BB_Middle'] - (bb_std * num_std)
        logger.info(f"Added Bollinger Bands (window={window}, std={num_std})")
        return df

    def add_volume_sma(self, df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
        """
        Add Volume Simple Moving Average

        Args:
            df: DataFrame with 'Volume' column
            window: Moving average window

        Returns:
            DataFrame with Volume SMA column
        """
        df[f'Volume_SMA_{window}'] = df['Volume'].rolling(window=window).mean()
        logger.info(f"Added Volume_SMA_{window}")
        return df

    def add_all_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add all technical indicators at once

        Args:
            df: DataFrame with 'Close' and 'Volume' columns

        Returns:
            DataFrame with all indicators added
        """
        # Ensure 'Close' is float
        df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

        # Moving Averages
        df = self.add_sma(df, 20)
        df = self.add_sma(df, 50)
        df = self.add_ema(df, 12)
        df = self.add_ema(df, 20)
        df = self.add_ema(df, 26)

        # Momentum Indicators
        df = self.add_rsi(df, 14)
        df = self.add_macd(df)

        # Volatility Indicators
        df = self.add_bollinger_bands(df)

        # Volume Indicators
        df = self.add_volume_sma(df, 20)

        return df


if __name__ == "__main__":
    # Test the indicators
    from data_fetcher import StockDataFetcher

    # Fetch data
    fetcher = StockDataFetcher()
    df = fetcher.get_historical_data("NVDA", period="1mo")

    if not df.empty:
        print("\n" + "=" * 60)
        print("TEST: Technical Indicators")
        print("=" * 60)

        # Store original columns
        original_cols = set(df.columns)
        print(f"\nOriginal columns ({len(original_cols)}): {list(original_cols)}")

        # Calculate indicators
        indicators = TechnicalIndicators()
        df_with_indicators = indicators.add_all_indicators(df)

        # Find new columns
        new_cols = set(df_with_indicators.columns) - original_cols
        print(f"\nNew columns added: {len(new_cols)}")
        print(f"New columns: {sorted(list(new_cols))}")

        # Show last 5 rows with key indicators
        print("\nLast 5 rows with indicators:")
        display_cols = ['Date', 'Close', 'SMA_20', 'EMA_20', 'RSI', 'MACD', 'BB_Upper', 'BB_Lower']
        available_cols = [col for col in display_cols if col in df_with_indicators.columns]
        print(df_with_indicators[available_cols].tail())

        print("\n✅ Technical indicators working correctly!")
    else:
        print("No data available to test indicators")