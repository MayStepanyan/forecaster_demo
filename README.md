# forecaster_demo

Streamlit app for OHLCV price forecasting. Enter a stock, ETF, or index ticker and get a candlestick chart with historical data and a Chronos-generated forecast.

**Model:** [`amazon/chronos-t5-tiny`](https://huggingface.co/amazon/chronos-t5-tiny) — downloads automatically on first run (~300 MB, CPU-only).  
**Data:** yfinance (no API key required).

## Supported tickers

- Stocks: `AAPL`, `TSLA`, `MSFT`, `GOOGL`, `NVDA`
- ETFs: `SPY`, `QQQ`, `VTI`, `GLD`
- Indices: `^GSPC`, `^DJI`, `^IXIC`

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or with Docker:

```bash
docker compose up
# http://localhost:8501
```

## Deploy to Hugging Face Spaces

Add this header to the top of `README.md` and push to a Space:

```yaml
---
title: Stock Forecaster
emoji: 📈
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---
```

> Not financial advice.
