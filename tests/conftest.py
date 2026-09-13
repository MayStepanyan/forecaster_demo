import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


@pytest.fixture
def sample_ohlcv_df():
    dates = pd.date_range(end=datetime.today(), periods=100, freq="D")
    np.random.seed(42)
    close = 150 + np.cumsum(np.random.randn(100))
    return pd.DataFrame({
        "open":   close - np.random.uniform(0, 2, 100),
        "high":   close + np.random.uniform(0, 3, 100),
        "low":    close - np.random.uniform(0, 3, 100),
        "close":  close,
        "volume": np.random.randint(1_000_000, 10_000_000, 100).astype(float),
    }, index=pd.Index(dates, name="timestamp"))


@pytest.fixture
def sample_forecast_df(sample_ohlcv_df):
    last = sample_ohlcv_df.index[-1]
    dates = pd.date_range(start=last + timedelta(days=1), periods=10, freq="D")
    close = sample_ohlcv_df["close"].iloc[-1] + np.cumsum(np.random.randn(10))
    return pd.DataFrame({
        "open":  close - 1,
        "high":  close + 2,
        "low":   close - 2,
        "close": close,
    }, index=pd.Index(dates, name="timestamp"))
