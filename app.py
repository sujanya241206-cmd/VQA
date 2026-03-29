import streamlit as st
from login import login_page, logout_page
import vqa
import history
from vqa import predict_answer, generate_story

def main():
    if st.session_state.get("logged_in"):
        default_index=2
    else:
        default_index=0
    # Sidebar
    menu = st.sidebar.radio(
        "Navigation",
        ["Home", "Login", "VQA", "History", "Logout"],
        index=default_index
    )

    # HOME
    if menu == "Home":
        st.title("Welcome to VQA Smart Vision")
        st.write("""
        - Visual Question Answering
        - AI Story Generation
        - Analytics Dashboard
        """)

    # LOGIN
    elif menu == "Login":
        login_page()

    # VQA
    elif menu == "VQA":
        vqa.main()

    # HISTORY
    elif menu == "History":
        history.main()

    # LOGOUT
    elif menu == "Logout":
        logout_page()

if __name__ == "__main__":
    main()