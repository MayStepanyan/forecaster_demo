import numpy as np
import pandas as pd
import torch
from datetime import timedelta

from forecast.model import load_pipeline

INTERVAL_DELTAS = {
    "1h":  timedelta(hours=1),
    "1d":  timedelta(days=1),
    "1wk": timedelta(weeks=1),
}

OHLCV_COLS = ["open", "high", "low", "close", "volume"]


def run_forecast(
    df: pd.DataFrame,
    interval: str = "1d",
    horizon: int = 20,
    context_length: int = 200,
) -> pd.DataFrame:
    """
    Run Chronos forecast on historical OHLCV data.

    Forecasts each OHLCV column independently (Chronos is univariate)
    and returns the median prediction across samples.

    Args:
        df: Historical OHLCV DataFrame indexed by timestamp
        interval: Candle interval — "1h", "1d", or "1wk"
        horizon: Number of future candles to predict
        context_length: Historical candles fed to model (max 512)

    Returns:
        DataFrame with forecasted OHLCV indexed by future timestamps
    """
    pipeline = load_pipeline()
    history = df.tail(context_length)

    last_ts = history.index[-1]
    delta = INTERVAL_DELTAS[interval]
    future_index = pd.DatetimeIndex(
        [last_ts + delta * (i + 1) for i in range(horizon)],
        name="timestamp",
    )

    results = {}
    for col in OHLCV_COLS:
        context = torch.tensor(history[col].values, dtype=torch.float32).unsqueeze(0)
        # samples shape: [1, num_samples, horizon]
        samples = pipeline.predict(context, prediction_length=horizon)
        results[col] = np.median(samples[0].numpy(), axis=0)

    return pd.DataFrame(results, index=future_index)
