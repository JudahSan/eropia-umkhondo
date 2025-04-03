import streamlit as st
from auth_manager import AuthManager
import pages.login as login_page
import pages.register as register_page
import pages.dashboard as dashboard_page
import pages.landing as landing_page
import pages.profile as profile_page

# Set page configuration
st.set_page_config(
    page_title="Eropia umkhondo - Money Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for current page if not set
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Define our app navigation structure
def main():
    # Set up sidebar navigation
    with st.sidebar:
        st.title("Eropia umkhondo")
        st.image("generated-icon.png", width=80)
        
        # Check if user is logged in
        if "username" in st.session_state:
            st.write(f"Logged in as: {st.session_state.username}")
            
            # Show dashboard button
            if st.button("Dashboard", key="dashboard_btn"):
                st.session_state.current_page = "dashboard"
                st.rerun()
            
            # Show profile button
            if st.button("Profile", key="profile_btn"):
                st.session_state.current_page = "profile"
                st.rerun()
            
            # Show logout button
            if st.button("Logout", key="logout_btn"):
                # Clear session state and go back to landing
                for key in list(st.session_state.keys()):
                    if key != "current_page":
                        del st.session_state[key]
                
                st.session_state.current_page = "landing"
                st.rerun()
        else:
            # Show home button
            if st.button("Home", key="home_btn"):
                st.session_state.current_page = "landing"
                st.rerun()
                
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
    if st.session_state.current_page == "dashboard":
        # Always show dashboard when that page is selected
        dashboard_page.app()
    elif st.session_state.current_page == "profile" and "username" in st.session_state:
        # Show profile page for logged in users
        profile_page.app()
    elif st.session_state.current_page == "landing":
        # Show landing page regardless of login status
        landing_page.app()
    elif "username" not in st.session_state:
        # Only if user is not logged in, show login/register pages
        if st.session_state.current_page == "login":
            login_page.app()
        elif st.session_state.current_page == "register":
            register_page.app()
        else:
            # Default to landing if an invalid page is somehow set
            st.session_state.current_page = "landing"
            st.rerun()
    else:
        # If user is logged in and tries to access login/register, redirect to dashboard
        dashboard_page.app()

if __name__ == "__main__":
    main()