"""
Test different timeframes for all stocks
"""

from src.data_fetcher import StockDataFetcher
import time

fetcher = StockDataFetcher()
symbols = list(fetcher.stock_symbols.keys())
timeframes = ["1d", "5d", "1mo", "6mo", "1y"]

print("=" * 60)
print("FETCHING DATA FOR ALL TIMEFRAMES")
print("=" * 60)

for symbol in symbols:
    print(f"\n📊 Fetching {symbol}...")
    for period in timeframes:
        data = fetcher.get_historical_data(symbol, period=period)
        print(f"  {period}: {len(data)} rows")
        time.sleep(0.5)  # Small delay to avoid rate limiting

print("\nAll data fetched successfully!")