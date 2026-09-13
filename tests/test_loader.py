from data.loader import fetch_ohlcv
import pytest


def test_fetch_returns_ohlcv_columns():
    df = fetch_ohlcv("AAPL", interval="1d")
    assert set(["open", "high", "low", "close", "volume"]).issubset(df.columns)
    assert not df.empty


def test_fetch_index_etf():
    df = fetch_ohlcv("SPY", interval="1d")
    assert not df.empty


def test_fetch_raises_on_bad_ticker():
    with pytest.raises(ValueError, match="No data returned"):
        fetch_ohlcv("XXXXBADTICKER999", interval="1d")
