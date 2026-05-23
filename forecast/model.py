import os
import sys
import streamlit as st


def _ensure_kronos_on_path() -> None:
    """
    Kronos has no setup.py/pyproject.toml so pip install git+... does not register
    its 'model' package. Add the repo root to sys.path so 'from model import ...' works.

    Set KRONOS_PATH=/path/to/Kronos in your shell (or .env) to point at the clone.
    """
    kronos_path = os.environ.get("KRONOS_PATH", "")
    if kronos_path and kronos_path not in sys.path:
        sys.path.insert(0, kronos_path)
        return

    # Try common fallback locations relative to this file
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        os.path.join(here, "..", "Kronos"),       # sibling of project root
        os.path.join(here, "..", "..", "Kronos"),  # one level up
        os.path.expanduser("~/Kronos"),
    ]
    for path in candidates:
        path = os.path.normpath(path)
        if os.path.isdir(os.path.join(path, "model")) and path not in sys.path:
            sys.path.insert(0, path)
            return

    raise ImportError(
        "Cannot locate the Kronos repo. "
        "Clone it with:\n\n"
        "  git clone https://github.com/Leegoo-dev/Kronos.git\n\n"
        "Then set the KRONOS_PATH environment variable to its location:\n\n"
        "  export KRONOS_PATH=/path/to/Kronos"
    )


_ensure_kronos_on_path()

from model import Kronos, KronosTokenizer, KronosPredictor  # noqa: E402


@st.cache_resource(show_spinner="Loading Kronos model...")
def load_predictor(max_context: int = 512) -> KronosPredictor:
    """Load Kronos-small from Hugging Face Hub. Cached for the session lifetime."""
    tokenizer = KronosTokenizer.from_pretrained("NeoQuasar/Kronos-Tokenizer-base")
    model = Kronos.from_pretrained("NeoQuasar/Kronos-small")
    return KronosPredictor(model, tokenizer, max_context=max_context)
