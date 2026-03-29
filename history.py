import streamlit as st
from utils.storage import StorageManager

def main():
    st.title("📊 History")

    # Safety session initialization
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if "username" not in st.session_state:
        st.session_state.username = None

    # Check login
    if not st.session_state.logged_in:
        st.warning("Please login first")
        return

    storage = StorageManager()
    data = storage.get_user_history(st.session_state.username)

    if not data:
        st.info("No history yet")
        return

    # Show history items
    for item in reversed(data):
        st.write("---")
        st.write("🖼 Image:", item["image"])
        st.write("❓ Question:", item["question"])
        st.write("💬 Answer:", item["answer"])

        if item["story"]:
            st.write("📖 Story:", item["story"])
