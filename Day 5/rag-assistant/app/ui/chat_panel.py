import streamlit as st

from app.ui.api_client import ApiClient


def render_chat(api: ApiClient) -> None:
    st.subheader("Chat")
    session_id = st.session_state.get("session_id")
    if not session_id:
        st.info("Upload a PDF first.")
        return

    for msg in st.session_state.get("chat", []):
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask something about the document…")
    if not prompt:
        return

    st.session_state["chat"].append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            res = api.chat(session_id=session_id, query=prompt, provider=st.session_state.get("provider", "gemini"))
            answer = res["answer"]
            sources = res.get("sources", [])
        except Exception as e:
            answer = f"Error: {e}"
            sources = []

    assistant_msg = answer
    if sources:
        assistant_msg += "\n\n**Sources (top chunks):**\n"
        for s in sources[:3]:
            assistant_msg += f"- chunk {s['chunk_id']} (score {s['score']:.3f})\n"

    st.session_state["chat"].append({"role": "assistant", "content": assistant_msg})
    with st.chat_message("assistant"):
        st.markdown(assistant_msg)

