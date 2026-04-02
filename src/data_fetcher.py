"""
Stock Data Fetcher Module
Fetches real-time and historical stock data using yfinance
"""

import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StockDataFetcher:
    """Fetch stock data from Yahoo Finance"""

    def __init__(self):
        self.stock_symbols = {
            "NVDA": "NVIDIA Corporation",
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc.",
            "META": "Meta Platforms Inc.",
            "AMZN": "Amazon.com Inc.",
            "TSLA": "Tesla Inc."
        }

    def get_stock_info(self, symbol: str) -> Dict:
        """
        Get current stock information

        Args:
            symbol: Stock ticker symbol

        Returns:
            Dictionary with current stock info
        """
        try:
            stock = yf.Ticker(symbol)
            info = stock.info

            return {
                "symbol": symbol,
                "name": self.stock_symbols.get(symbol, info.get('longName', symbol)),
                "current_price": info.get('currentPrice', info.get('regularMarketPrice', 0)),
                "day_change": info.get('regularMarketChange', 0),
                "day_change_percent": info.get('regularMarketChangePercent', 0),
                "volume": info.get('regularMarketVolume', 0),
                "avg_volume": info.get('averageVolume', 0),
                "market_cap": info.get('marketCap', 0),
                "pe_ratio": info.get('trailingPE', 0),
                "dividend_yield": info.get('dividendYield', 0),
                "day_high": info.get('dayHigh', 0),
                "day_low": info.get('dayLow', 0),
                "fifty_two_week_high": info.get('fiftyTwoWeekHigh', 0),
                "fifty_two_week_low": info.get('fiftyTwoWeekLow', 0),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {e}")
            return None

    def get_historical_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """
        Get historical stock data

        Args:
            symbol: Stock ticker symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)

        Returns:
            DataFrame with historical data
        """
        try:
            stock = yf.Ticker(symbol)
            data = stock.history(period=period)

            if data.empty:
                logger.warning(f"No data found for {symbol}")
                return pd.DataFrame()

            # Reset index to make Date a column
            data = data.reset_index()
            data['Symbol'] = symbol

            logger.info(f"Fetched {len(data)} rows for {symbol} ({period})")
            return data

        except Exception as e:
            logger.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()

    def get_multiple_stocks(self, symbols: List[str], period: str = "1mo") -> Dict[str, pd.DataFrame]:
        """
        Get historical data for multiple stocks

        Args:
            symbols: List of stock tickers
            period: Time period

        Returns:
            Dictionary with symbol as key and DataFrame as value
        """
        results = {}
        for symbol in symbols:
            results[symbol] = self.get_historical_data(symbol, period)
        return results

    def get_realtime_prices(self, symbols: List[str]) -> pd.DataFrame:
        """
        Get real-time prices for multiple stocks

        Args:
            symbols: List of stock tickers

        Returns:
            DataFrame with real-time prices
        """
        realtime_data = []
        for symbol in symbols:
            info = self.get_stock_info(symbol)
            if info:
                realtime_data.append(info)

        return pd.DataFrame(realtime_data)

    def save_to_csv(self, data: pd.DataFrame, symbol: str, period: str):
        #Save data to CSV file
        filename = f"data/raw/{symbol}_{period}.csv"
        data.to_csv(filename, index=False)
        logger.info(f"Saved data to {filename}")

    def load_from_csv(self, symbol: str, period: str) -> pd.DataFrame:
        #Load data from CSV file
        filename = f"data/raw/{symbol}_{period}.csv"
        try:
            data = pd.read_csv(filename)
            logger.info(f"Loaded data from {filename}")
            return data
        except FileNotFoundError:
            logger.warning(f"File not found: {filename}")
            return pd.DataFrame()


if __name__ == "__main__":
    # Test the data fetcher
    fetcher = StockDataFetcher()

    # Test 1: Get current info for all stocks
    print("\n" + "=" * 60)
    print("TEST 1: Real-time stock info")
    print("=" * 60)

    symbols = list(fetcher.stock_symbols.keys())
    realtime_df = fetcher.get_realtime_prices(symbols)
    print(realtime_df.to_string())

    # Test 2: Get historical data for one stock
    print("\n" + "=" * 60)
    print("TEST 2: Historical data for NVDA (1 month)")
    print("=" * 60)

    historical = fetcher.get_historical_data("NVDA", period="1mo")
    print(f"Shape: {historical.shape}")
    print(historical.head())

    # Test 3: Save and load data
    print("\n" + "=" * 60)
    print("TEST 3: Save and load data")
    print("=" * 60)

    fetcher.save_to_csv(historical, "NVDA", "1mo")
    loaded = fetcher.load_from_csv("NVDA", "1mo")
    print(f"Loaded {len(loaded)} rows")

    print("\nData fetcher working correctly!")