import streamlit as st


def ensure_state() -> None:
    st.session_state.setdefault("session_id", None)
    st.session_state.setdefault("provider", "gemini")
    st.session_state.setdefault("chat", [])
    st.session_state.setdefault("doc_name", None)

