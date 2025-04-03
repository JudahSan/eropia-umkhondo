import streamlit as st
from auth_manager import AuthManager

def app():
    # Custom CSS for better mobile responsiveness and styling
    st.markdown("""
    <style>
    .block-container {
        max-width: 90%;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Responsive adjustments for mobile */
    @media (max-width: 768px) {
        .block-container {
            max-width: 95%;
            padding: 1rem;
        }
        h1 {
            font-size: 1.8rem !important;
        }
        .stButton>button {
            width: 100%;
            margin-bottom: 10px;
        }
    }
    
    /* Improved button styling */
    .stButton>button {
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    /* Fix padding and margins */
    div.row-widget.stButton {
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Fix form element spacing */
    div.css-1r6slb0.e1tzin5v2 {
        padding: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center content for better appearance
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("Login to Finance Tracker")
        
        auth_manager = AuthManager()
        authenticator, authentication_status, username = auth_manager.setup_auth()
        
        if authentication_status:
            st.success(f"Welcome back, {username}!")
            st.info("Redirecting to dashboard...")
            
            # Store the username in session state for later use
            st.session_state.username = username
            
            # Navigate to the dashboard
            st.session_state.current_page = "dashboard"
            st.rerun()
            
        elif authentication_status is False:
            st.error("Invalid username or password. Please try again.")
        
        st.write("---")
        
        # Make the register button more responsive
        st.write("Don't have an account?")
        
        # Make button fill width on mobile
        if st.button("Register Now", use_container_width=True):
            st.session_state.current_page = "register"
            st.rerun()

if __name__ == "__main__":
    app()