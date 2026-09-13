from forecast.predictor import run_forecast


def test_forecast_correct_horizon(sample_ohlcv_df):
    forecast = run_forecast(sample_ohlcv_df, interval="1d", horizon=10)
    assert len(forecast) == 10


def test_forecast_columns_present(sample_ohlcv_df):
    forecast = run_forecast(sample_ohlcv_df, interval="1d", horizon=5)
    for col in ["open", "high", "low", "close"]:
        assert col in forecast.columns


def test_forecast_timestamps_future(sample_ohlcv_df):
    forecast = run_forecast(sample_ohlcv_df, interval="1d", horizon=5)
    assert forecast.index[0] > sample_ohlcv_df.index[-1]
