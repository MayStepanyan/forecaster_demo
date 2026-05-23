import pandas as pd
from datetime import timedelta
from forecast.model import load_predictor

INTERVAL_DELTAS = {
    "1h":  timedelta(hours=1),
    "1d":  timedelta(days=1),
    "1wk": timedelta(weeks=1),
}


def run_forecast(
    df: pd.DataFrame,
    interval: str = "1d",
    horizon: int = 20,
    context_length: int = 200,
) -> pd.DataFrame:
    """
    Run Kronos forecast on historical OHLCV data.

    Args:
        df: Historical OHLCV DataFrame indexed by timestamp
        interval: Candle interval — "1h", "1d", or "1wk"
        horizon: Number of future candles to predict
        context_length: Historical candles fed to model (max 512)

    Returns:
        DataFrame with forecasted OHLCV indexed by future timestamps
    """
    predictor = load_predictor(max_context=context_length)

    history = df.tail(context_length).copy()

    last_ts = history.index[-1]
    delta = INTERVAL_DELTAS[interval]
    future_timestamps = pd.Series([
        last_ts + delta * (i + 1) for i in range(horizon)
    ])

    forecast = predictor.predict(
        df=history[["open", "high", "low", "close", "volume"]],
        x_timestamp=pd.Series(history.index),
        y_timestamp=future_timestamps,
    )

    return forecast
