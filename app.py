import streamlit as st
from auth_manager import AuthManager
import pages.login as login_page
import pages.register as register_page
import pages.dashboard as dashboard_page

# Set page configuration
st.set_page_config(
    page_title="Personal Finance Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for current page if not set
if "current_page" not in st.session_state:
    st.session_state.current_page = "login"

# Define our app navigation structure
def main():
    # Set up sidebar navigation
    with st.sidebar:
        st.title("Finance Tracker")
        st.image("generated-icon.png", width=80)
        
        # Check if user is logged in
        if "username" in st.session_state:
            st.write(f"Logged in as: {st.session_state.username}")
            
            # Show dashboard button
            if st.button("Dashboard", key="dashboard_btn"):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            # Show logout button
            if st.button("Logout", key="logout_btn"):
                # Clear session state and go back to login
                for key in list(st.session_state.keys()):
                    if key != "current_page":
                        del st.session_state[key]
                
                st.session_state.current_page = "login"
                st.rerun()
        else:
            # Only show login/register buttons if not logged in
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Login", key="login_btn"):
                    st.session_state.current_page = "login"
                    st.rerun()
            
            with col2:
                if st.button("Register", key="register_btn"):
                    st.session_state.current_page = "register"
                    st.rerun()
    
    # Handle page routing
    if "username" in st.session_state:
        # If user is logged in, only show dashboard regardless of current_page
        # This ensures login/register are completely hidden
        dashboard_page.app()
    else:
        # Only if user is not logged in, show login/register pages
        if st.session_state.current_page == "login":
            login_page.app()
        elif st.session_state.current_page == "register":
            register_page.app()
        else:
            # Default to login if an invalid page is somehow set
            st.session_state.current_page = "login"
            st.rerun()

if __name__ == "__main__":
    main()