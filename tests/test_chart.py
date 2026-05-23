from charts.candlestick import build_chart


def test_chart_has_two_candlestick_traces(sample_ohlcv_df, sample_forecast_df):
    fig = build_chart(sample_ohlcv_df, sample_forecast_df, ticker="AAPL")
    traces = [t for t in fig.data if t.type == "candlestick"]
    assert len(traces) == 2


def test_chart_title_contains_ticker(sample_ohlcv_df, sample_forecast_df):
    fig = build_chart(sample_ohlcv_df, sample_forecast_df, ticker="AAPL")
    assert "AAPL" in fig.layout.title.text
