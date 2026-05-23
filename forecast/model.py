import streamlit as st
from model import Kronos, KronosTokenizer, KronosPredictor  # from Kronos GitHub repo


@st.cache_resource(show_spinner="Loading Kronos model...")
def load_predictor(max_context: int = 512) -> KronosPredictor:
    """Load Kronos-small from Hugging Face Hub. Cached for the session lifetime."""
    tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
    model = Kronos.from_pretrained("NeoQuasar/Kronos-small")
    return KronosPredictor(model, tokenizer, max_context=max_context)
