import torch
import streamlit as st
from chronos import ChronosPipeline


@st.cache_resource(show_spinner="Loading Chronos model...")
def load_pipeline() -> ChronosPipeline:
    """Load amazon/chronos-t5-tiny from Hugging Face Hub. Cached for the session lifetime."""
    return ChronosPipeline.from_pretrained(
        "amazon/chronos-t5-tiny",
        device_map="cpu",
        torch_dtype=torch.float32,
    )
