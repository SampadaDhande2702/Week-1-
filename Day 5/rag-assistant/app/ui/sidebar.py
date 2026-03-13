import streamlit as st

from app.ui.api_client import ApiClient


def render_sidebar(api: ApiClient) -> None:
    st.sidebar.title("RAG-Lite Assistant")

    st.sidebar.caption("Backend")
    try:
        health = api.health()
        st.sidebar.success("API: healthy")
        st.sidebar.json(health["providers"])
    except Exception:
        st.sidebar.warning("API: not reachable")

    st.sidebar.caption("LLM Provider")
    st.session_state["provider"] = st.sidebar.selectbox(
        "Choose provider",
        options=["gemini", "groq", "ollama"],
        index=["gemini", "groq", "ollama"].index(st.session_state.get("provider", "gemini")),
    )

