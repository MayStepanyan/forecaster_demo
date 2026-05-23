import streamlit as st
from datetime import date

MAX_FREE_FORECASTS = 5


def check_rate_limit() -> tuple[bool, int]:
    """Returns (allowed, remaining). Resets at midnight."""
    today = str(date.today())

    if "rl_date" not in st.session_state or st.session_state["rl_date"] != today:
        st.session_state["rl_date"] = today
        st.session_state["rl_count"] = 0

    used = st.session_state["rl_count"]
    remaining = MAX_FREE_FORECASTS - used
    return remaining > 0, remaining


def consume_forecast():
    st.session_state["rl_count"] = st.session_state.get("rl_count", 0) + 1
