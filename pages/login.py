import streamlit as st
from auth_manager import AuthManager

def app():
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
    st.write("Don't have an account?")
    
    if st.button("Register Now"):
        st.session_state.current_page = "register"
        st.rerun()

if __name__ == "__main__":
    app()