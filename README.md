<div align="center">

# 📈 Real-Time Stock Market Dashboard

**Interactive dashboard for tracking live stock prices with technical indicators**

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-latest-red.svg)](https://streamlit.io)
[![yfinance](https://img.shields.io/badge/Data-yfinance-orange.svg)](https://pypi.org/project/yfinance/)

</div>

---

## Overview

A real-time stock market dashboard built with Streamlit and Yahoo Finance data. Track live prices, analyze trends across multiple timeframes, and apply technical indicators — all in one interactive interface.

**Tracked stocks:** NVDA · AAPL · MSFT · GOOGL · META · AMZN · TSLA

---

## Features

- **Live prices** with change and percentage movement, auto-refreshed every 10–30 seconds
- **Multiple timeframes** — 1D, 1W, 1M, 6M, 1Y
- **Technical indicators** — SMA, EMA, RSI, MACD, Bollinger Bands
- **Interactive candlestick charts** powered by Plotly
- **Portfolio tracking** with custom quantities per stock

---

## Project Structure

```
Stock-Market-Dashboard/
├── src/
│   ├── data_fetcher.py       # Fetch real-time & historical data from yfinance
│   ├── indicators.py          # Technical indicator calculations
│   └── data_processor.py      # Process all stocks with indicators
├── data/
│   ├── raw/                   # Raw stock data (CSV)
│   └── processed/             # Processed data with indicators (23 rows × 22 cols per stock)
├── app/
│   └── dashboard.py           # Streamlit dashboard
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# Clone the repository
git clone https://github.com/SaniruRajapaksha2006/Stock-Market-Dashboard.git
cd Stock-Market-Dashboard

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Fetch stock data
python src/data_fetcher.py

# Process data with indicators
python src/data_processor.py
```

---

## Technology Stack

| Layer | Library |
|-------|---------|
| Data source | yfinance (Yahoo Finance) |
| Data processing | pandas, numpy |
| Technical indicators | ta |
| Visualisation | Plotly |
| Dashboard | Streamlit |

---

## Technical Indicators

The following indicators are calculated and stored for each stock:

- **Trend** — SMA (20, 50), EMA (12, 20, 26)
- **Momentum** — RSI (14)
- **Trend / Momentum** — MACD, MACD Signal, MACD Histogram
- **Volatility** — Bollinger Bands (Upper, Middle, Lower)
- **Volume** — Volume SMA (20)

---

## Sample Output

**Real-time prices**

| Symbol | Name | Price | Change | Change % |
|--------|------|-------|--------|----------|
| NVDA | NVIDIA | $177.02 | +$1.27 | +0.72% |
| AAPL | Apple | $255.10 | −$0.54 | −0.21% |
| TSLA | Tesla | $360.82 | −$20.45 | −5.36% |

*Prices shown are illustrative samples from development testing.*

---

## Build Progress

### ✅ Day 1 — Foundation & Data Collection
- Project structure and virtual environment setup
- `data_fetcher.py` — live prices for 7 stocks via yfinance
- Historical data across all timeframes (1d, 5d, 1mo, 6mo, 1y)
- CSV save/load functionality

### ✅ Day 2 — Technical Indicators & Processing
- `indicators.py` — full indicator suite (SMA, EMA, RSI, MACD, Bollinger Bands)
- `data_processor.py` — batch processing for all 7 stocks
- Processed output: 23 rows × 22 columns per stock, saved to CSV


---

## Author

**R. S. P. S. Uthsara**  
BSc (Hons) Artificial Intelligence and Data Science  
Informatics Institute of Technology (IIT) Sri Lanka / Robert Gordon University, Aberdeen

---

## License
