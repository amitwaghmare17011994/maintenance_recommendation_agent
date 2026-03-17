import streamlit as st
import requests

API_ANALYZE = "http://127.0.0.1:8000/analyze"
API_CHAT = "http://127.0.0.1:8000/chat"

st.set_page_config(layout="wide")

st.title("Maintenance Recommendation Agent")


if "analyzed" not in st.session_state:
    st.session_state.analyzed = False

if "chat_open" not in st.session_state:
    st.session_state.chat_open = False


# -------------------
# ANALYZE
# -------------------

file = st.file_uploader("Upload PDF", type=["pdf"])

if file is not None:

    if st.button("Analyze"):

        files = {
            "file": (file.name, file, "application/pdf")
        }

        with st.spinner("Processing..."):

            r = requests.post(API_ANALYZE, files=files)

        if r.status_code == 200:

            data = r.json()

            st.session_state.analyzed = True

            st.subheader("Parsed Data")
            st.write(data["parsed"])

            st.subheader("Context")
            st.write(data["context"])

            st.subheader("Recommendation")
            st.write(data["recommendation"])

        else:
            st.error("API error")


# -------------------
# CHAT ICON
# -------------------

if st.session_state.analyzed:

    st.markdown(
        """
        <style>
        .chat-button {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #4CAF50;
            color: white;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 30px;
            text-align: center;
            line-height: 60px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("💬", key="chat_icon"):

        st.session_state.chat_open = not st.session_state.chat_open


# -------------------
# CHAT BOX
# -------------------

if st.session_state.chat_open:

    st.sidebar.title("Chat")

    question = st.sidebar.text_input("Ask")

    if st.sidebar.button("Send"):

        r = requests.post(
            API_CHAT,
            params={"question": question}
        )

        if r.status_code == 200:

            data = r.json()

            st.sidebar.write(data["answer"])

        else:
            st.sidebar.error("API error")