import os

import streamlit as st

from app.ui.api_client import ApiClient
from app.ui.chat_panel import render_chat
from app.ui.sidebar import render_sidebar
from app.ui.state_manager import ensure_state
from app.ui.upload_panel import render_upload


def main() -> None:
    st.set_page_config(page_title="RAG-Lite Assistant", layout="wide")
    ensure_state()

    api_base = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
    api = ApiClient(api_base)

    render_sidebar(api)

    col1, col2 = st.columns([1, 2])
    with col1:
        render_upload(api)
        if st.session_state.get("doc_name"):
            st.caption(f"Document: {st.session_state['doc_name']}")
            st.caption(f"Session: {st.session_state['session_id']}")

    with col2:
        render_chat(api)


if __name__ == "__main__":
    main()

