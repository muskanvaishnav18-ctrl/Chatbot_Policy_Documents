import streamlit as st

# Page layout
st.set_page_config(page_title="Chatbot", layout="wide")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for chat history
with st.sidebar:
    st.header("Chat History")
    if st.session_state.history:
        for i, chat in enumerate(st.session_state.history):
            st.write(f"**You:** {chat['user']}")
            st.write(f"**Bot:** {chat['bot']}")
    else:
        st.write("No history yet.")

# Main area
st.title("Chatbot Policy Documets")
st.write("How can I help you in this area?")
# User input
user_input = st.text_input("", placeholder="Ask your question...")

if st.button("Send") and user_input:
    # Placeholder for bot response (replace with LLM later)
    bot_response = f"Echo: {user_input}"
    
    # Save to history
    st.session_state.history.append({"user": user_input, "bot": bot_response})

    # Show latest response
    st.write(f"**Bot:** {bot_response}")

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption("By messaging ChatGPT, you agree to our Terms and have read our Privacy Policy and its Korea addendum.")
# Clear history button in sidebar
with st.sidebar:
    if st.button("Clear History"):
        st.session_state.history = []