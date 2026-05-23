import yfinance as yf
import pandas as pd

INTERVAL_MAP = {
    "1h":  "1h",
    "1d":  "1d",
    "1wk": "1wk",
}

PERIOD_MAP = {
    "1h":  "60d",
    "1d":  "2y",
    "1wk": "5y",
}


def fetch_ohlcv(ticker: str, interval: str = "1d") -> pd.DataFrame:
    """
    Fetch OHLCV from Yahoo Finance.
    Returns DataFrame with columns: [open, high, low, close, volume] indexed by timestamp.
    Raises ValueError on unknown ticker or empty result.
    """
    period = PERIOD_MAP.get(interval, "2y")
    data = yf.download(ticker, period=period, interval=interval, progress=False)

    if data.empty:
        raise ValueError(
            f"No data returned for '{ticker}'. "
            "Check the ticker symbol — use ^ prefix for indices (e.g. ^GSPC)."
        )

    df = data[["Open", "High", "Low", "Close", "Volume"]].copy()
    df.columns = ["open", "high", "low", "close", "volume"]
    df.index.name = "timestamp"
    df = df.dropna()

    return df.astype(float)
