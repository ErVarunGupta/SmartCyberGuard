import streamlit as st
from core.ai_assistant import get_ai_response

def render_chatbot():

    st.header("🤖 AI System Assistant")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 🧠 Display previous messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 💬 User input
    user_input = st.chat_input("Ask about your system...")

    if user_input:
        # Show user message
        with st.chat_message("user"):
            st.markdown(user_input)

        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # 🤖 Get AI response
        with st.spinner("Thinking..."):
            response = get_ai_response(user_input)

        # Show AI response
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })