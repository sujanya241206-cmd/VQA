import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
#sys.path.append(str(Path(__file__).parent.parent))

from auth import AuthManager

# Page configuration
#st.set_page_config(
#    page_title="Login - VQA Smart Vision",
#    page_icon="🔐",
#    layout="wide"
#)

# Load CSS from main app
def load_css():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #1e1e2e 0%, #2d1b3d 50%, #1a1a2e 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1e2e 0%, #2d1b3d 100%);
    }
    
    .card {
        background: rgba(255, 255, 255, 0.05);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 1rem 0;
    }
    
    .main-header {
        text-align: center;
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    h1, h2, h3 {
        color: #ffffff !important;
    }
    
    p, label, .stMarkdown {
        color: #e0e0e0 !important;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

load_css()

# Initialize auth manager
auth_manager = AuthManager()

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

def login_page():
    st.markdown('<h1 class="main-header">Login</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            st.markdown("### Sign In")
            
            with st.form("login_form"):
                username = st.text_input("Username", key="login_username")
                password = st.text_input("Password", type="password", key="login_password")
                
                submit = st.form_submit_button("Login")
                
                if submit:
                    if not username or not password:
                        st.error("Please fill in all fields")
                    else:
                        success, message = auth_manager.login_user(username, password)
                        
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.username = username
                            st.success(message)
                            st.info("Redirecting to main page...")
                            st.rerun()
                        else:
                            st.error(message)
        
        with tab2:
            st.markdown("### Create Account")
            
            with st.form("register_form"):
                new_username = st.text_input("Username", key="reg_username")
                new_email = st.text_input("Email (optional)", key="reg_email")
                new_password = st.text_input("Password", type="password", key="reg_password")
                confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm")
                
                register = st.form_submit_button("Register")
                
                if register:
                    if not new_username or not new_password:
                        st.error("Please fill in required fields")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        success, message = auth_manager.register_user(
                            new_username, 
                            new_password, 
                            new_email
                        )
                        
                        if success:
                            st.success(message)
                            st.info("You can now login with your credentials")
                        else:
                            st.error(message)
        
        st.markdown('</div>', unsafe_allow_html=True)

def logout_page():
    st.markdown('<h1 class="main-header">Account</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.success(f"Logged in as: **{st.session_state.username}**")
        
        user_info = auth_manager.get_user_info(st.session_state.username)
        
        if user_info:
            st.markdown("### Account Information")
            st.write(f"**Username:** {st.session_state.username}")
            st.write(f"**Email:** {user_info.get('email', 'Not provided')}")
            st.write(f"**Member since:** {user_info.get('created_at', 'Unknown')[:10]}")
            
            if user_info.get('last_login'):
                st.write(f"**Last login:** {user_info['last_login'][:16]}")
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.success("Logged out successfully")
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Main
"""if st.session_state.logged_in:
    logout_page()
else:
    login_page()
login_page()"""