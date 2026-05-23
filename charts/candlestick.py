import plotly.graph_objects as go
import pandas as pd


def build_chart(
    historical: pd.DataFrame,
    forecast: pd.DataFrame,
    ticker: str,
    n_historical: int = 60,
) -> go.Figure:
    """
    Candlestick chart: historical candles + forecast candles with divider.
    Historical: green/red standard.
    Forecast: blue/purple, semi-transparent.
    """
    hist = historical.tail(n_historical)
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=hist.index,
        open=hist["open"], high=hist["high"],
        low=hist["low"],   close=hist["close"],
        name="Historical",
        increasing_line_color="#26a69a",
        decreasing_line_color="#ef5350",
    ))

    fig.add_trace(go.Candlestick(
        x=forecast.index,
        open=forecast["open"], high=forecast["high"],
        low=forecast["low"],   close=forecast["close"],
        name="Forecast (Kronos)",
        increasing_line_color="#90caf9",
        decreasing_line_color="#ce93d8",
        opacity=0.8,
    ))

    fig.add_vline(
        x=forecast.index[0],
        line_dash="dash",
        line_color="rgba(255,255,255,0.4)",
        annotation_text="Forecast →",
        annotation_position="top right",
    )

    fig.update_layout(
        title=f"{ticker.upper()} — Kronos Forecast",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        xaxis_rangeslider_visible=False,
        height=520,
    )

    return fig
