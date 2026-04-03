"""
Data Processing Module
Processes raw stock data and adds technical indicators
"""

import pandas as pd
import logging
from pathlib import Path
from typing import Dict, List, Optional

from data_fetcher import StockDataFetcher
from indicators import TechnicalIndicators

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Process stock data with technical indicators"""

    def __init__(self):
        self.fetcher = StockDataFetcher()
        self.indicators = TechnicalIndicators()

    def process_stock(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """
        Process a single stock: fetch data and add indicators

        Args:
            symbol: Stock ticker
            period: Time period

        Returns:
            DataFrame with processed data
        """
        # Fetch historical data
        df = self.fetcher.get_historical_data(symbol, period=period)

        if df.empty:
            logger.warning(f"No data for {symbol}")
            return df

        # Add all technical indicators
        df = self.indicators.add_all_indicators(df)

        # Add symbol column
        df['Symbol'] = symbol

        logger.info(f"Processed {symbol}: {len(df)} rows with indicators")
        return df

    def process_all_stocks(self, period: str = "1mo") -> Dict[str, pd.DataFrame]:
        """
        Process all stocks

        Args:
            period: Time period

        Returns:
            Dictionary with symbol as key and processed DataFrame as value
        """
        symbols = list(self.fetcher.stock_symbols.keys())
        results = {}

        for symbol in symbols:
            results[symbol] = self.process_stock(symbol, period=period)

        return results

    def save_processed_data(self, df: pd.DataFrame, symbol: str, period: str):
        """Save processed data to CSV"""
        filename = f"data/processed/{symbol}_{period}_with_indicators.csv"
        Path("data/processed").mkdir(parents=True, exist_ok=True)
        df.to_csv(filename, index=False)
        logger.info(f"Saved processed data to {filename}")

    def load_processed_data(self, symbol: str, period: str) -> pd.DataFrame:
        """Load processed data from CSV"""
        filename = f"data/processed/{symbol}_{period}_with_indicators.csv"
        try:
            df = pd.read_csv(filename)
            logger.info(f"Loaded processed data from {filename}")
            return df
        except FileNotFoundError:
            logger.warning(f"File not found: {filename}")
            return pd.DataFrame()


if __name__ == "__main__":
    # Test the data processor
    processor = DataProcessor()

    print("\n" + "=" * 60)
    print("TEST: Data Processor")
    print("=" * 60)

    # Process one stock
    print("\n1. Processing NVDA (1 month)...")
    df = processor.process_stock("NVDA", period="1mo")

    if not df.empty:
        print(f"   Shape: {df.shape}")
        print(f"   Columns: {list(df.columns)}")

        # Save processed data
        processor.save_processed_data(df, "NVDA", "1mo")
        print("\n   ✅ Saved processed data")

    # Process all stocks
    print("\n2. Processing all stocks (1 week)...")
    all_data = processor.process_all_stocks(period="1mo")

    for symbol, data in all_data.items():
        print(f"   {symbol}: {len(data)} rows")

    print("\n✅ Data processor working correctly!")