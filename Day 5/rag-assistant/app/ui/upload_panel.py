import streamlit as st

from app.ui.api_client import ApiClient


def render_upload(api: ApiClient) -> None:
    st.subheader("Upload PDF")
    uploaded = st.file_uploader("Choose a text-based PDF", type=["pdf"])
    if uploaded is None:
        return

    if st.button("Process document", type="primary"):
        with st.spinner("Extracting, chunking, embedding, indexing..."):
            try:
                res = api.ingest_pdf(uploaded.getvalue(), uploaded.name)
            except Exception as e:
                st.error(f"Ingest failed: {e}")
                return
        st.session_state["session_id"] = res["session_id"]
        st.session_state["doc_name"] = uploaded.name
        st.session_state["chat"] = []
        st.success(f"Ready. Chunks: {res['chunk_count']}")

