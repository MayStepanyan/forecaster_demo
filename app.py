import streamlit as st
from data.loader import fetch_ohlcv
from forecast.predictor import run_forecast
from charts.candlestick import build_chart
from utils.rate_limit import check_rate_limit, consume_forecast

st.set_page_config(page_title="Kronos Stock Forecaster", page_icon="📈", layout="wide")
st.title("📈 Kronos Stock Forecaster")
st.caption("AI-powered OHLCV forecasting for stocks, ETFs, and indices")

with st.sidebar:
    st.header("Settings")
    interval = st.selectbox("Interval", ["1h", "1d", "1wk"], index=1)
    horizon = st.slider("Forecast candles", 5, 30, 20)
    context = st.slider("Historical context", 50, 512, 200)
    st.divider()
    allowed, remaining = check_rate_limit()
    st.metric("Free forecasts remaining today", remaining)
    st.divider()
    st.markdown(
        "**Example tickers**\n"
        "- Stocks: `AAPL` `TSLA` `NVDA`\n"
        "- ETFs: `SPY` `QQQ` `VTI`\n"
        "- Indices: `^GSPC` `^DJI`"
    )

ticker_input = st.text_input(
    "Enter ticker symbol",
    placeholder="AAPL, SPY, ^GSPC...",
)

run_button = st.button("Generate Forecast", type="primary", disabled=not allowed)

if not allowed:
    st.warning("Daily limit reached (5 forecasts). Come back tomorrow.")

if run_button and ticker_input:
    ticker = ticker_input.strip().upper()

    with st.spinner(f"Fetching {ticker} data..."):
        try:
            df = fetch_ohlcv(ticker, interval=interval)
        except ValueError as e:
            st.error(str(e))
            st.stop()

    with st.spinner("Running Kronos forecast..."):
        try:
            forecast = run_forecast(df, interval=interval, horizon=horizon, context_length=context)
        except Exception as e:
            st.error(f"Forecast failed: {e}")
            st.stop()

    consume_forecast()

    fig = build_chart(df, forecast, ticker=ticker)
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Raw forecast data"):
        st.dataframe(forecast.round(4), use_container_width=True)

    last_close = df["close"].iloc[-1]
    forecast_close = forecast["close"].iloc[-1]
    delta = ((forecast_close - last_close) / last_close) * 100

    col1, col2, col3 = st.columns(3)
    col1.metric("Last close", f"${last_close:.2f}")
    col2.metric(f"Forecast close (+{horizon} candles)", f"${forecast_close:.2f}")
    col3.metric("Projected change", f"{delta:+.2f}%")

    st.caption("⚠️ Not financial advice. Forecasts are probabilistic and for informational purposes only.")
